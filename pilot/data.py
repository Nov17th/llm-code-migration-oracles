"""Load the 164 HumanEval-X tasks, pairing each Python function with its Java counterpart."""
import gzip
import hashlib
import json
import os
import urllib.request
from dataclasses import dataclass

URL = 'https://raw.githubusercontent.com/THUDM/CodeGeeX/main/codegeex/benchmark/humaneval-x/{0}/data/humaneval_{0}.jsonl.gz'
SHA256 = {
    'python': '5752fb122efddb0e9b47c77907ae6ce9a15aac4dea14e44c46032c831e6b987a',
    'java': '276f36db2eb7aeb864f36a19a2f4e1bb2460fb6e22ff100f0b5bedabe3799967',
}


@dataclass
class Task:
    task_id: str
    python_code: str     # the function to translate, without its docstring
    java_signature: str  # imports, class Solution and the method signature
    java_imports: str
    java_reference: str  # signature + canonical solution
    java_body: str       # canonical solution only
    java_test: str       # class Main, which calls the method and checks the results


def _load(lang, data_dir):
    path = os.path.join(data_dir, 'humaneval_%s.jsonl.gz' % lang)
    if not os.path.exists(path):
        os.makedirs(data_dir, exist_ok=True)
        urllib.request.urlretrieve(URL.format(lang), path)
    with open(path, 'rb') as f:
        if hashlib.sha256(f.read()).hexdigest() != SHA256[lang]:
            raise RuntimeError('Unexpected content in ' + path)
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return [json.loads(line) for line in f]


def load_tasks(data_dir='data', limit=None):
    tasks = []
    for p, j in zip(_load('python', data_dir), _load('java', data_dir)):
        n = p['task_id'].split('/')[1]
        assert j['task_id'] == 'Java/' + n
        tasks.append(Task(
            task_id='HumanEval/' + n,
            python_code=p['declaration'] + p['canonical_solution'],
            java_signature=j['declaration'].rstrip() + '\n',
            java_imports=''.join(l + '\n' for l in j['declaration'].splitlines() if l.startswith('import ')),
            java_reference=j['declaration'] + j['canonical_solution'],
            java_body=j['canonical_solution'],
            java_test=j['test'],
        ))
    return tasks[:limit] if limit else tasks
