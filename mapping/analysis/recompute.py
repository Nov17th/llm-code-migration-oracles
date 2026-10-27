"""Recompute every count reported in the paper from the CSV files of this repository.

Usage:  python mapping/analysis/recompute.py   (from the repository root)
Needs only the Python standard library. The output is also saved in
analysis/expected_output.txt so that changes can be diffed.
"""
import csv
import os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(path):
    with open(os.path.join(ROOT, path), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


scanned = read('1_search/scanned_papers.csv')
log = read('1_search/search_log.csv')
cands = read('2_screening/candidates.csv')
coding = read('4_coding/coding.csv')
fig3 = read('4_coding/figure3_compile_vs_behavior.csv')
tab8 = read('4_coding/table8_other_disagreements.csv')

main = [c for c in coding if c['tier'] == 'main']
N = len(main)
ORACLES = ['O-a', 'O-b', 'O-c', 'O-d', 'O-e', 'O-f', 'O-g', 'O-h', 'O-i']
has = lambda c, o: o in c['oracles'].split(';')
pct = lambda k, n: '%d (%.0f%%)' % (k, 100.0 * k / n)


def section(title):
    print('\n== %s ==' % title)


# ---------------------------------------------------------------- Search (Section 4.2, Table 2)
section('Search (Section 4.2, Table 2)')
print('papers scanned (search log):', sum(int(r['papers_scanned']) for r in log))
print('keyword hits (search log):  ', sum(int(r['keyword_hits']) for r in log))
print('papers scanned (paper list):', len(scanned))
print('without abstract:           ', sum(1 for r in scanned if r['abstract_available'] != 'y'))
print('keyword hits (paper list):  ', sum(1 for r in scanned if r['keyword_hit'] == 'yes'))
cy = lambda r: '%s %s' % (r['conference'], r['year'])
rows = defaultdict(Counter)
for r in scanned:
    rows[r['conference_year']]['papers'] += 1
    rows[r['conference_year']]['no_abstract'] += r['abstract_available'] != 'y'
    rows[r['conference_year']]['hits'] += r['keyword_hit'] == 'yes'
for c in cands:
    rows[cy(c)]['candidates'] += 1
for c in coding:
    rows['%s %s' % (c['conference'], c['year'])]['included' if c['tier'] == 'main' else 'I3'] += 1
print('%-10s %7s %11s %5s %10s %8s %3s' % ('venue', 'papers', 'no abstract', 'hits', 'candidates', 'included', 'I3'))
for k in sorted(rows, key=lambda k: (['ICSE', 'FSE', 'ASE'].index(k.split()[0]), k)):
    v = rows[k]
    print('%-10s %7d %11d %5d %10d %8d %3d' % (k, v['papers'], v['no_abstract'], v['hits'], v['candidates'], v['included'], v['I3']))

# ---------------------------------------------------------------- Selection (Section 4.3-4.4, Figure 1)
section('Selection (Sections 4.3-4.4, Figure 1)')
print('candidates:', len(cands), dict(Counter(c['source'] for c in cands)))
inc = [c for c in cands if c['decision'] == 'include']
exc = [c for c in cands if c['decision'] == 'exclude']
print('included:', len(inc), dict(Counter(c['tier'] for c in inc)), ' excluded:', len(exc))


def reason(c):
    if c['clarification_rule'] == 'L-TASK':
        return 'L-TASK'
    return c['criterion']


print('exclusion reasons (all):', dict(Counter(reason(c) for c in exc).most_common()))
e6 = [c for c in exc if c['criterion'] == 'E6']
ta = [c for c in exc if c['decision_basis'] in ('title', 'abstract') and c['criterion'] != 'E6']
ft_exc = [c for c in exc if c['decision_basis'] == 'full text']
print('excluded on title/abstract:', len(ta), '(title only: %d)' % sum(c['decision_basis'] == 'title' for c in ta))
print('   reasons:', dict(Counter(reason(c) for c in ta).most_common()))
print('full text sought:', len(inc) + len(ft_exc) + len(e6), ' not available (E6):', len(e6),
      ' read:', len(inc) + len(ft_exc))
print('excluded after full text:', len(ft_exc), dict(Counter(reason(c) for c in ft_exc).most_common()))
rules = Counter(c['clarification_rule'] for c in cands if c['clarification_rule'])
print('clarification rules (Table 4):', dict(rules.most_common()), ' total:', sum(rules.values()),
      ' exclusions:', sum(1 for c in cands if c['clarification_rule'] and c['decision'] == 'exclude'),
      ' inclusions:', sum(1 for c in cands if c['clarification_rule'] and c['decision'] == 'include'))

# ---------------------------------------------------------------- Corpus (Section 5.1)
section('Corpus overview (Section 5.1), main corpus n = %d' % N)
print('by year:', dict(sorted(Counter(c['year'] for c in main).items())))
print('by track:', dict(Counter(c['track'] for c in main).most_common()))
kinds = Counter(k for c in main for k in c['migration_kinds'].split(';'))
print('migration kinds (a paper can have several):', dict(kinds.most_common()))
print('legacy:', sum(c['legacy'] == 'yes' for c in main), ' Rust target:', sum(c['targets_rust'] == 'yes' for c in main))
print('LLM role:', dict(Counter(c['llm_role'] for c in main).most_common()))

# ---------------------------------------------------------------- RQ1 (Figure 2, Table 5)
section('RQ1: oracle frequency (Figure 2)')
for o in ORACLES:
    print('  %s %s' % (o, pct(sum(has(c, o) for c in main), N)))
print('number of oracles per paper:', dict(sorted(Counter(int(c['n_oracles']) for c in main).items())))
exe = {'O-c', 'O-d', 'O-e', 'O-f'}
print('no execution-based oracle (none of O-c..O-f):', sum(not (set(c['oracles'].split(';')) & exe) for c in main))
single = [c for c in main if c['n_oracles'] == '1' and not (set(c['oracles'].split(';')) & exe)]
print('  of these, a single oracle:', len(single), sorted(c['cite_key'] for c in single))
print('compare outputs with the original program (O-f or O-g):', sum(has(c, 'O-f') or has(c, 'O-g') for c in main))
print('existing tests but no compile rate (O-c without O-b):', sum(has(c, 'O-c') and not has(c, 'O-b') for c in main))
print('differential testing as the only test-based oracle:',
      sum(has(c, 'O-f') and not any(has(c, o) for o in ('O-c', 'O-d', 'O-e')) for c in main), 'of', sum(has(c, 'O-f') for c in main))
print('mean oracles by track:', {t: round(sum(int(c['n_oracles']) for c in main if c['track'] == t) /
                                     sum(c['track'] == t for c in main), 1) for t in sorted(set(c['track'] for c in main))})
section('RQ1: oracle combinations (Table 5, lower triangle)')
print('     ' + ' '.join('%4s' % o for o in ORACLES))
for i, a in enumerate(ORACLES):
    print('%-4s ' % a + ' '.join('%4d' % sum(has(c, a) and has(c, b) for c in main) for b in ORACLES[:i + 1]))

# ---------------------------------------------------------------- RQ2 (Table 6, Table 7)
section('RQ2: oracle use by context (Table 6)')
groups = [('Legacy', lambda c: c['legacy'] == 'yes'), ('Not legacy', lambda c: c['legacy'] == 'no')]
groups += [(k, (lambda k: lambda c: k in c['migration_kinds'].split(';'))(k)) for k in ['XL', 'LIB', 'VER', 'FW', 'DIA']]
short = {'NIER', 'Ideas, Visions and Reflections', 'Demonstration', 'Poster'}
groups += [('Research', lambda c: c['track'] == 'Research'), ('Industry/SEIP', lambda c: c['track'] == 'Industry/SEIP'),
           ('NIER, IVR, demo, poster', lambda c: c['track'] in short), ('Journal-first', lambda c: c['track'] == 'Journal-first')]
groups += [(y, (lambda y: lambda c: c['year'] == y)(y)) for y in ['2024', '2025', '2026']]
print('%-24s %3s ' % ('group', 'n') + ' '.join('%4s' % o for o in ORACLES))
for name, f in groups:
    g = [c for c in main if f(c)]
    print('%-24s %3d ' % (name, len(g)) + ' '.join('%4d' % sum(has(c, o) for c in g) for o in ORACLES))
section('RQ2: origin of execution-based oracles (Table 7)')
codes = Counter(k for c in main for k in c['oracle_origin'].split(';') if k)
for k in ['c:B', 'c:P', 'c:BP', 'd:S', 'd:H', 'e:S', 'e:U', 'f:F', 'f:T', 'f:L', 'f:C', 'f:U']:
    print('  %-5s %d' % (k, codes[k]))
lv = Counter(); xl = Counter()
for c in main:
    oc = [k for k in c['oracle_origin'].split(';') if k.startswith('c:')]
    if not oc:
        continue
    ks = set(c['migration_kinds'].split(';'))
    if ks & {'LIB', 'VER'}:
        lv[oc[0]] += 1
    elif 'XL' in ks:
        xl[oc[0]] += 1
print('existing-test origin, library or version migration:', dict(lv), ' translation (XL):', dict(xl))

# ---------------------------------------------------------------- RQ3 (Figure 3, Table 8, Table 9)
section('RQ3: several oracles on the same outputs')
mg = Counter(g for c in main for g in c['multi_oracle_group'].split(';') if g and g != 'none')
print('papers:', sum(c['multi_oracle_group'] not in ('', 'none') for c in main), ' by group:', dict(mg))
gaps = [float(r['gap_points']) for r in fig3]
print('Figure 3 rows:', len(fig3), ' gap range: %.0f to %.0f points' % (min(gaps), max(gaps)))
for r in fig3:
    print('  %-26s %6.2f %6.2f  gap %3.0f' % (r['short_name'], float(r['compile_rate_pct']), float(r['behavioral_rate_pct']),
                                         float(r['gap_points'])))
print('Table 8 rows:', len(tab8))
section('RQ3: stated limitations (Table 9)')
for k, v in Counter(c['limitation_theme'] for c in main).most_common():
    print('  %2d  %s' % (v, k))
section('RQ3 and RQ4: other counts')
oi = [c for c in main if has(c, 'O-i')]
print('human evaluation papers:', len(oi), ' reporting rater agreement:', sum(c['reports_rater_agreement'] == 'yes' for c in oi))
print('final oracle also used in the technique:', dict(Counter(c['final_oracle_also_used_in_technique'] for c in main
                                                              if c['final_oracle_also_used_in_technique'])))
print('formal verification papers targeting Rust:', sum(has(c, 'O-g') and c['targets_rust'] == 'yes' for c in main),
      'of', sum(has(c, 'O-g') for c in main))
print('LLM-generated tests / LLM judges by year:',
      dict(Counter(c['year'] for c in main if has(c, 'O-e'))), dict(Counter(c['year'] for c in main if has(c, 'O-h'))))
