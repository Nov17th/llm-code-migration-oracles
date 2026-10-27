"""The stages of a run. Each stage appends one JSON line per item to a file in the output folder and skips
items already there, so an interrupted run continues where it stopped."""
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

from llm import extract_java, translate_messages
from oracles import compile_check, judge, similarity, test_check


def read_jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def _todo(items, path, key):
    done = {r[key] for r in read_jsonl(path)}
    return [it for it in items if it[key] not in done]


def _save_each(path, items, work, workers=1):
    """Apply work(item) to each item (in parallel threads if workers > 1) and append item + result to path."""
    with ThreadPoolExecutor(max_workers=workers) as pool, open(path, 'a', encoding='utf-8') as f:
        for i, (it, res) in enumerate(zip(items, pool.map(work, items)), 1):
            f.write(json.dumps(dict(it, **res), ensure_ascii=False) + '\n')
            f.flush()
            if i % 20 == 0 or i == len(items):
                print('  %d/%d' % (i, len(items)), flush=True)


def _static_oracles(task, code):
    return dict(compile_check(task, code), **dict(test_check(task, code), **similarity(task, code)))


def translate(model, tasks, out):
    """Stage 1: one translation per task."""
    path = os.path.join(out, 'translations.jsonl')
    items = _todo([{'task_id': t.task_id} for t in tasks], path, 'task_id')
    by_id = {t.task_id: t for t in tasks}

    def work(it):
        start = time.time()
        answer = model.chat(translate_messages(by_id[it['task_id']]), max_tokens=1024)
        return {'answer': answer, 'java_code': extract_java(answer), 'seconds': round(time.time() - start, 1)}

    print('Translating %d tasks with %s' % (len(items), model.model))
    _save_each(path, items, work)


def check(tasks, out, workers):
    """Stage 2: compilation (O-b), tests (O-c) and CodeBLEU (O-a) for every translation."""
    path = os.path.join(out, 'oracles.jsonl')
    code = {r['task_id']: r['java_code'] for r in read_jsonl(os.path.join(out, 'translations.jsonl'))}
    by_id = {t.task_id: t for t in tasks}
    items = _todo([{'task_id': i} for i in by_id if i in code], path, 'task_id')
    print('Compile, tests and CodeBLEU for %d translations' % len(items))
    _save_each(path, items, lambda it: _static_oracles(by_id[it['task_id']], code[it['task_id']]), workers)


def judge_all(model, tasks, out):
    """Stage 3: the LLM judge (O-h) on every translation."""
    path = os.path.join(out, 'judgments.jsonl')
    code = {r['task_id']: r['java_code'] for r in read_jsonl(os.path.join(out, 'translations.jsonl'))}
    by_id = {t.task_id: t for t in tasks}
    items = _todo([{'task_id': i} for i in by_id if i in code], path, 'task_id')
    print('Judging %d translations with %s' % (len(items), model.model))
    _save_each(path, items, lambda it: judge(model, by_id[it['task_id']], code[it['task_id']]))


MUTATIONS = [  # one mutant per group: the first rule that applies, at its first position
    ('relational', [(' < ', ' <= '), (' <= ', ' < '), (' > ', ' >= '), (' >= ', ' > '), (' == ', ' != '), (' != ', ' == ')]),
    ('arithmetic', [(' + ', ' - '), (' - ', ' + '), (' * ', ' + ')]),
    ('boolean', [('return true', 'return false'), ('return false', 'return true')]),
    ('constant', [('= 0;', '= 1;')]),
]


def mutants(task):
    signature = task.java_reference[:-len(task.java_body)]
    out = []
    for group, rules in MUTATIONS:
        for old, new in rules:
            if old in task.java_body:
                out.append({'mutant_id': task.task_id + '#' + group, 'task_id': task.task_id, 'change': old.strip() + ' -> ' + new.strip(),
                            'java_code': signature + task.java_body.replace(old, new, 1)})
                break
    return out


def selfcheck(tasks, out, workers):
    """Stage 0: check the harness on known answers.
    - Reference solutions must compile, pass the tests and score CodeBLEU 1.0.
    - Wrapped in a ```java block as a model would answer, they must come out of the extraction unchanged.
    - Mutants of the references show how many wrong programs the tests catch."""
    os.makedirs(os.path.join(out, 'selfcheck'), exist_ok=True)
    by_id = {t.task_id: t for t in tasks}

    def reference(it):
        ref = by_id[it['task_id']].java_reference
        extracted = extract_java('Here is the code:\n```java\n%s\n```' % ref) == ref.strip() + '\n'
        return dict(_static_oracles(by_id[it['task_id']], ref), extraction_ok=extracted)

    path = os.path.join(out, 'selfcheck', 'reference.jsonl')
    items = _todo([{'task_id': t.task_id} for t in tasks], path, 'task_id')
    print('Reference solutions: %d' % len(items))
    _save_each(path, items, reference, workers)

    path = os.path.join(out, 'selfcheck', 'mutants.jsonl')
    items = _todo([m for t in tasks for m in mutants(t)], path, 'mutant_id')
    print('Mutants: %d' % len(items))
    _save_each(path, items, lambda m: dict(compile_check(by_id[m['task_id']], m['java_code']),
                                           **test_check(by_id[m['task_id']], m['java_code'])), workers)


def controls(model, tasks, out):
    """Stage 4: the judge on known answers: each reference solution (equivalent) and one mutant per task that
    the tests reject (not equivalent)."""
    by_id = {t.task_id: t for t in tasks}
    rejected = {}
    for m in read_jsonl(os.path.join(out, 'selfcheck', 'mutants.jsonl')):
        if m['task_id'] in by_id and m['compiles'] and m['tests'] != 'pass':
            rejected.setdefault(m['task_id'], m)
    items = [{'control_id': t.task_id + '#reference', 'task_id': t.task_id, 'kind': 'reference'} for t in tasks]
    items += [{'control_id': m['mutant_id'], 'task_id': m['task_id'], 'kind': 'mutant'} for m in rejected.values()]
    code = {it['control_id']: by_id[it['task_id']].java_reference for it in items if it['kind'] == 'reference'}
    code.update({m['mutant_id']: m['java_code'] for m in rejected.values()})
    path = os.path.join(out, 'controls.jsonl')
    items = _todo(items, path, 'control_id')
    print('Judge on %d known answers' % len(items))
    _save_each(path, items, lambda it: judge(model, by_id[it['task_id']], code[it['control_id']]))
