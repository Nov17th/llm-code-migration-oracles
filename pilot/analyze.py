"""Combine the verdicts and measure how often the oracles disagree. The tests (O-c) are the reference, since
they are the only oracle that runs the translation.

Writes summary.md, summary.json, verdicts.csv (one row per task) and disagreements.csv (tasks where an oracle
disagrees with the tests, with an empty column for manual review)."""
import csv
import json
import os
from collections import Counter

from oracles import THRESHOLDS
from pipeline import read_jsonl

MAIN_THRESHOLD = 0.6


def pct(k, n):
    return round(100.0 * k / n, 1) if n else None


def against_tests(accepts, passes):
    pairs = list(zip(accepts, passes))
    tp, fp = sum(a and p for a, p in pairs), sum(a and not p for a, p in pairs)
    fn, tn = sum(p and not a for a, p in pairs), sum(not a and not p for a, p in pairs)
    return {'accepts_passes': tp, 'accepts_fails': fp, 'rejects_passes': fn, 'rejects_fails': tn,
            'agreement_pct': pct(tp + tn, len(pairs)), 'false_acceptance_pct': pct(fp, fp + tn),
            'false_rejection_pct': pct(fn, tp + fn)}


def correlation(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx, syy = sum((x - mx) ** 2 for x in xs), sum((y - my) ** 2 for y in ys)
    return round(sxy / (sxx * syy) ** 0.5, 3) if sxx and syy else None


def write_csv(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        if rows:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)


def analyze(out):
    load = lambda name: {r['task_id']: r for r in read_jsonl(os.path.join(out, name))}
    trans, orc, jud = load('translations.jsonl'), load('oracles.jsonl'), load('judgments.jsonl')
    ids = [i for i in trans if i in orc]
    rows = [dict({'task_id': i, 'judge': jud.get(i, {}).get('judge', ''), 'seconds': trans[i]['seconds']},
                 **{k: orc[i][k] for k in ('compiles', 'tests', 'codebleu', 'cb_ngram', 'cb_weighted_ngram', 'cb_syntax', 'cb_dataflow')})
            for i in ids]
    n = len(rows)
    verdicts = {'O-b compile': [r['compiles'] for r in rows], 'O-c tests': [r['tests'] == 'pass' for r in rows]}
    for t in THRESHOLDS:
        verdicts['O-a CodeBLEU>=%.1f' % t] = [r['codebleu'] >= t for r in rows]
    if all(i in jud for i in ids):
        verdicts['O-h judge'] = [r['judge'] == 'YES' for r in rows]
    passes = verdicts['O-c tests']
    cb = [r['codebleu'] for r in rows]

    s = {'tasks': n, 'accept_pct': {k: pct(sum(v), n) for k, v in verdicts.items()}}
    s['compile_minus_tests_pp'] = round(s['accept_pct']['O-b compile'] - s['accept_pct']['O-c tests'], 1)
    s['test_status'] = dict(Counter(r['tests'] for r in rows))
    s['interface_errors'] = sum(r['compiles'] and r['tests'] == 'compile_error' for r in rows)
    s['judge_unparsed'] = sum(r['judge'] == 'UNPARSED' for r in rows)
    s['codebleu_mean_if_pass'] = round(sum(c for c, p in zip(cb, passes) if p) / max(1, sum(passes)), 3)
    s['codebleu_mean_if_fail'] = round(sum(c for c, p in zip(cb, passes) if not p) / max(1, n - sum(passes)), 3)
    s['codebleu_test_correlation'] = correlation(cb, [float(p) for p in passes])
    s['against_tests'] = {k: against_tests(v, passes) for k, v in verdicts.items() if k != 'O-c tests'}

    main = [k for k in verdicts if not k.startswith('O-a') or k.endswith('%.1f' % MAIN_THRESHOLD)]
    s['pairwise_agreement_pct'] = {a: {b: pct(sum(x == y for x, y in zip(verdicts[a], verdicts[b])), n) for b in main} for a in main}
    patterns = Counter(''.join('+' if verdicts[k][i] else '-' for k in main) for i in range(n))
    s['patterns'] = {'order': main, 'counts': dict(patterns.most_common())}

    ctrl = read_jsonl(os.path.join(out, 'controls.jsonl'))
    ref = [c['judge'] == 'YES' for c in ctrl if c['kind'] == 'reference']
    mut = [c['judge'] == 'NO' for c in ctrl if c['kind'] == 'mutant']
    if ref and mut:
        s['judge_on_known_answers'] = {'references': len(ref), 'yes_on_references': sum(ref),
                                       'mutants': len(mut), 'no_on_mutants': sum(mut),
                                       'balanced_accuracy_pct': round((pct(sum(ref), len(ref)) + pct(sum(mut), len(mut))) / 2, 1)}
    ref = read_jsonl(os.path.join(out, 'selfcheck', 'reference.jsonl'))
    mut = read_jsonl(os.path.join(out, 'selfcheck', 'mutants.jsonl'))
    if ref:
        s['selfcheck'] = {'references': len(ref), 'compile': sum(r['compiles'] for r in ref),
                          'pass_tests': sum(r['tests'] == 'pass' for r in ref),
                          'codebleu_1': sum(r['codebleu'] >= 0.9999 for r in ref), 'extraction_ok': sum(r['extraction_ok'] for r in ref),
                          'mutants': len(mut), 'mutants_compile': sum(m['compiles'] for m in mut),
                          'mutants_rejected': sum(m['compiles'] and m['tests'] != 'pass' for m in mut)}

    write_csv(os.path.join(out, 'verdicts.csv'), rows)
    disagreements = []
    for i, r in enumerate(rows):
        differ = [k.split()[0] for k in main if k != 'O-c tests' and verdicts[k][i] != passes[i]]
        if differ:
            disagreements.append(dict(r, differ_from_tests=' '.join(differ),
                                      tests_log=(orc[r['task_id']]['tests_log'].splitlines() or [''])[0][:200],
                                      judge_answer=jud.get(r['task_id'], {}).get('judge_answer', '')[:300].replace('\n', ' '),
                                      manual_review=''))
    write_csv(os.path.join(out, 'disagreements.csv'), disagreements)
    s['tasks_with_disagreement'] = len(disagreements)

    with open(os.path.join(out, 'summary.json'), 'w') as f:
        json.dump(s, f, indent=2)
    with open(os.path.join(out, 'summary.md'), 'w') as f:
        f.write(report(s))
    print(report(s))


def report(s):
    L = ['# Pilot results', '', '%d tasks.' % s['tasks'], '', '| Oracle | Accepts (%) |', '|---|---|']
    L += ['| %s | %s |' % kv for kv in s['accept_pct'].items()]
    L += ['', 'Compile rate minus test pass rate: %s percentage points. Test outcomes: %s. Interface errors: %d.'
          % (s['compile_minus_tests_pp'], s['test_status'], s['interface_errors']),
          'CodeBLEU: mean %s when the tests pass, %s when they fail; correlation with the test outcome %s.'
          % (s['codebleu_mean_if_pass'], s['codebleu_mean_if_fail'], s['codebleu_test_correlation']),
          '', '## Each oracle against the tests', '',
          '| Oracle | Accepts, passes | Accepts, fails | Rejects, passes | Rejects, fails | Agreement (%) | False acceptance (%) | False rejection (%) |',
          '|---|---|---|---|---|---|---|---|']
    L += ['| %s | %d | %d | %d | %d | %s | %s | %s |' % ((k,) + tuple(v.values())) for k, v in s['against_tests'].items()]
    names = list(s['pairwise_agreement_pct'])
    L += ['', '## Pairwise agreement (%)', '', '| | ' + ' | '.join(names) + ' |', '|---' * (len(names) + 1) + '|']
    L += ['| %s | ' % a + ' | '.join(str(v) for v in s['pairwise_agreement_pct'][a].values()) + ' |' for a in names]
    L += ['', '## Verdict patterns (%s; + accepts, - rejects)' % ', '.join(s['patterns']['order']), '', '| Pattern | Tasks |', '|---|---|']
    L += ['| `%s` | %d |' % kv for kv in s['patterns']['counts'].items()]
    L += ['', '%d tasks have at least one oracle that disagrees with the tests.' % s['tasks_with_disagreement']]
    if 'judge_on_known_answers' in s:
        j = s['judge_on_known_answers']
        L += ['', '## Judge on known answers', '', 'YES on %d of %d reference solutions; NO on %d of %d mutants rejected by the tests; balanced accuracy %s%%.'
              % (j['yes_on_references'], j['references'], j['no_on_mutants'], j['mutants'], j['balanced_accuracy_pct'])]
    if 'selfcheck' in s:
        c = s['selfcheck']
        L += ['', '## Self-check of the harness', '',
              'Reference solutions (%d): %d compile, %d pass the tests, %d score CodeBLEU 1.0, %d extracted unchanged.'
              % (c['references'], c['compile'], c['pass_tests'], c['codebleu_1'], c['extraction_ok']),
              'Mutants: %d generated, %d compile, %d rejected by the tests.' % (c['mutants'], c['mutants_compile'], c['mutants_rejected'])]
    return '\n'.join(L) + '\n'
