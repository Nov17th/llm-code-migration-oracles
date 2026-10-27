"""The four oracles. Each takes a task and a Java translation and returns its verdict as a dict."""
import os
import re
import shutil
import subprocess
import tempfile
import warnings

from llm import judge_messages, parse_verdict

COMPILE_TIMEOUT = 60
TEST_TIMEOUT = 10
THRESHOLDS = (0.5, 0.6, 0.7)


def _java(files, run_main=False):
    """Write the files to a fresh folder, compile them, and optionally run Main.
    Returns (status, log) with status in: ok, compile_error, fail, timeout."""
    d = tempfile.mkdtemp()
    try:
        for name, text in files.items():
            with open(os.path.join(d, name), 'w', encoding='utf-8') as f:
                f.write(text)
        steps = [(['javac', '-encoding', 'UTF-8', '-nowarn'] + list(files), COMPILE_TIMEOUT, 'compile_error')]
        if run_main:
            steps.append((['java', '-cp', '.', 'Main'], TEST_TIMEOUT, 'fail'))
        for cmd, timeout, error in steps:
            try:
                p = subprocess.run(cmd, cwd=d, capture_output=True, text=True, timeout=timeout)
            except subprocess.TimeoutExpired:
                return 'timeout', ''
            if p.returncode != 0:
                log = '\n'.join(l for l in (p.stdout + p.stderr).splitlines() if not l.startswith('Picked up '))
                return error, log[:2000]
        return 'ok', ''
    finally:
        shutil.rmtree(d, ignore_errors=True)


def compile_check(task, java_code):
    """O-b: the translation compiles on its own (the task's imports are put in front)."""
    status, log = _java({'Solution.java': task.java_imports + java_code})
    return {'compiles': status == 'ok', 'compile_log': log}


def test_check(task, java_code):
    """O-c: the translation passes the HumanEval-X tests. Status: pass, fail, timeout or compile_error.
    The tests and the translation share one file, which may hold only one public class (Main)."""
    code = re.sub(r'(^|\n)(\s*)public\s+(class\s+Solution\b)', r'\1\2\3', java_code)
    status, log = _java({'Main.java': task.java_imports + code + '\n' + task.java_test}, run_main=True)
    return {'tests': 'pass' if status == 'ok' else status, 'tests_log': log}


def similarity(task, java_code):
    """O-a: CodeBLEU against the reference solution, with its four components."""
    from codebleu import calc_codebleu
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        s = calc_codebleu([task.java_reference], [java_code], lang='java')
    return {'codebleu': round(s['codebleu'], 4), 'cb_ngram': round(s['ngram_match_score'], 4),
            'cb_weighted_ngram': round(s['weighted_ngram_match_score'], 4),
            'cb_syntax': round(s['syntax_match_score'], 4), 'cb_dataflow': round(s['dataflow_match_score'], 4)}


def judge(model, task, java_code):
    """O-h: a second model answers YES or NO to whether the translation is equivalent."""
    answer = model.chat(judge_messages(task, java_code), max_tokens=128)
    return {'judge': parse_verdict(answer), 'judge_answer': answer.strip()[:1000]}
