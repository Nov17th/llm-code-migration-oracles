"""Talking to the models: the two prompts, the Ollama client, and parsing the answers."""
import hashlib
import json
import os
import re
import urllib.request

TRANSLATE_SYSTEM = 'You are an expert software engineer who translates code between programming languages.'
TRANSLATE_PROMPT = """Translate the following Python function into Java.

Python:
```python
{python}
```

The Java code must use exactly this class and method signature:
```java
{signature}```

Return the complete Java class, including the import lines, in a single ```java code block. Do not add a main method or any explanation."""

JUDGE_SYSTEM = 'You are an expert software engineer who reviews code translations.'
JUDGE_PROMPT = """Below is a Python function and a Java translation of it. Decide whether the Java method is functionally equivalent to the Python function: for every valid input, it must return the same result.

Python:
```python
{python}
```

Java:
```java
{java}
```

Answer with a single word on the first line, YES or NO, and then give a one-sentence reason."""

SEED = 1234


def translate_messages(task):
    return [{'role': 'system', 'content': TRANSLATE_SYSTEM},
            {'role': 'user', 'content': TRANSLATE_PROMPT.format(python=task.python_code.rstrip(), signature=task.java_signature)}]


def judge_messages(task, java_code):
    return [{'role': 'system', 'content': JUDGE_SYSTEM},
            {'role': 'user', 'content': JUDGE_PROMPT.format(python=task.python_code.rstrip(), java=java_code.rstrip())}]


def prompt_hashes():
    h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:16]
    return {'translate': h(TRANSLATE_SYSTEM + TRANSLATE_PROMPT), 'judge': h(JUDGE_SYSTEM + JUDGE_PROMPT)}


class Ollama:
    """A model served by Ollama, queried with greedy decoding (temperature 0) and a fixed seed."""

    def __init__(self, model):
        self.model = model
        self.host = 'http://' + os.environ.get('OLLAMA_HOST', '127.0.0.1:11434').replace('http://', '')

    def _call(self, path, payload=None):
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(self.host + path, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read().decode())

    def chat(self, messages, max_tokens):
        options = {'temperature': 0, 'seed': SEED, 'num_ctx': 4096, 'num_predict': max_tokens}
        out = self._call('/api/chat', {'model': self.model, 'messages': messages, 'stream': False, 'options': options})
        return out['message']['content']

    def info(self):
        models = {m['name']: m for m in self._call('/api/tags')['models']}
        return {'model': self.model, 'digest': models.get(self.model, {}).get('digest'),
                'ollama': self._call('/api/version')['version'], 'temperature': 0, 'seed': SEED}


def extract_java(answer):
    """The first ```java block (else the first code block, else the whole answer), without package lines."""
    blocks = re.findall(r'```[ \t]*(\w*)[ \t]*\n(.*?)```', answer or '', re.S)
    java = [body for lang, body in blocks if lang.lower() == 'java']
    code = java[0] if java else (blocks[0][1] if blocks else answer or '')
    return '\n'.join(l for l in code.splitlines() if not re.match(r'\s*package\s+[\w.]+\s*;', l)).strip() + '\n'


def parse_verdict(answer):
    """YES or NO from the first non-empty line; else the first YES or NO anywhere; else UNPARSED."""
    text = (answer or '').strip()
    first_line = next((l for l in text.splitlines() if re.sub(r'[^A-Za-z]', '', l)), '')
    first_word = re.sub(r'[^A-Za-z ]', ' ', first_line).split()
    if first_word and first_word[0].upper() in ('YES', 'NO'):
        return first_word[0].upper()
    m = re.search(r'\b(YES|NO)\b', text.upper())
    return m.group(1) if m else 'UNPARSED'
