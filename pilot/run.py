"""Command line. Run from this folder, for example:

  python run.py all --translator qwen2.5-coder:7b-instruct-q4_K_M --judge llama3.1:8b-instruct-q4_K_M

Stages, in order: selfcheck, translate, check, judge, controls, analyze. 'all' runs them in turn; each can
also be run on its own. Models are Ollama model names."""
import argparse
import datetime
import json
import os
import platform
import subprocess
import sys

import pipeline
from analyze import analyze
from data import SHA256, load_tasks
from llm import Ollama, prompt_hashes

STAGES = ['selfcheck', 'translate', 'check', 'judge', 'controls', 'analyze']


def version(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True)
        return [l for l in (p.stdout + p.stderr).splitlines() if not l.startswith('Picked up ')][0]
    except Exception:
        return None


def log_run(out, stage, models):
    path = os.path.join(out, 'run_info.json')
    info = json.load(open(path)) if os.path.exists(path) else {'stages': []}
    info['environment'] = {'python': platform.python_version(), 'java': version(['java', '-version']),
                           'gpu': version(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader']),
                           'dataset_sha256': SHA256, 'prompt_sha256': prompt_hashes()}
    info['stages'].append({'stage': stage, 'finished': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
                           'models': {k: m.info() for k, m in models.items()}})
    with open(path, 'w') as f:
        json.dump(info, f, indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('stage', choices=STAGES + ['all'])
    ap.add_argument('--translator', help='Ollama model that translates')
    ap.add_argument('--judge', help='Ollama model that judges (a different model)')
    ap.add_argument('--out', default='results')
    ap.add_argument('--limit', type=int, help='only the first N tasks, for a quick test')
    ap.add_argument('--workers', type=int, default=os.cpu_count(), help='parallel javac/java processes')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tasks = load_tasks(limit=a.limit)
    for stage in STAGES if a.stage == 'all' else [a.stage]:
        print('\n== %s ==' % stage, flush=True)
        models = {}
        if stage == 'selfcheck':
            pipeline.selfcheck(tasks, a.out, a.workers)
        elif stage == 'translate':
            models['translator'] = Ollama(a.translator)
            pipeline.translate(models['translator'], tasks, a.out)
        elif stage == 'check':
            pipeline.check(tasks, a.out, a.workers)
        elif stage == 'judge':
            models['judge'] = Ollama(a.judge)
            pipeline.judge_all(models['judge'], tasks, a.out)
        elif stage == 'controls':
            models['judge'] = Ollama(a.judge)
            pipeline.controls(models['judge'], tasks, a.out)
        else:
            analyze(a.out)
        log_run(a.out, stage, models)


if __name__ == '__main__':
    sys.exit(main())
