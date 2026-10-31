"""Recompute every count of the mapping study from the CSV files of this repository.

Usage:  python mapping/analysis/recompute.py   (from the repository root)
Needs only the Python standard library. The output is also saved in
analysis/expected_output.txt so that changes can be diffed.

Most counts come from the coded data (4_coding/coding.csv and the two files with the
numbers behind Figure 3 and the table of other comparisons). Counts that rest on a
reading of the full texts rather than on a coded field come from
4_coding/reading_counts.csv, one row per paper with the location of the evidence.
The pilot's numbers are computed by pilot/analyze.py.
"""
import csv
import os
import re
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
tab9 = read('4_coding/table9_other_disagreements.csv')
fig3_own = read('4_coding/figure3_own_system.csv')
reading = read('4_coding/reading_counts.csv')

main = [c for c in coding if c['tier'] == 'main']
N = len(main)
ORACLES = ['O-a', 'O-b', 'O-c', 'O-d', 'O-e', 'O-f', 'O-g', 'O-h', 'O-i']
TEST_BASED = {'O-c', 'O-d', 'O-e', 'O-f'}
has = lambda c, o: o in c['oracles'].split(';')
test_based = lambda c: bool(set(c['oracles'].split(';')) & TEST_BASED)
origins = lambda c: [k for k in c['oracle_origin'].split(';') if k]
pct = lambda k, n: '%d (%.0f%%)' % (k, 100.0 * k / n)
of = lambda k, n: '%d of %d' % (k, n)


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
xref = [r for r in scanned if '[Crossref; paper not listed in any researchr program]' in r['track']]
included_ids = {c['candidate_id'] for c in coding}
print('added by Crossref (in no track program):', len(xref), ' keyword hits among them:',
      sum(r['keyword_hit'] == 'yes' for r in xref), ' included:', sum(r['candidate_id'] in included_ids for r in xref))
recall = [c for c in cands if c['recall_set'] == 'yes']
hit_ids = {r['candidate_id'] for r in scanned if r['keyword_hit'] == 'yes'}
missed = sorted(c['candidate_id'] for c in recall if c['candidate_id'] not in hit_ids)
print('recall check: known in-scope papers', len(recall), ' retrieved by the string', len(recall) - len(missed),
      ' missed', missed)
print('included papers that only the scan found:', sum(c['candidate_id'] not in {r['candidate_id'] for r in recall}
                                                      for c in coding))

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
by_year = Counter(c['year'] for c in main)
print('by year:', dict(sorted(by_year.items())))
scanned_year = Counter(r['conference_year'].split()[1] for r in scanned)
print('   share of the papers scanned that year:',
      {y: '%.2f%%' % (100.0 * by_year[y] / scanned_year[y]) for y in sorted(by_year)})
print('by track:', dict(Counter(c['track'] for c in main).most_common()))
kinds = Counter(k for c in main for k in c['migration_kinds'].split(';'))
print('migration kinds (a paper can have several):', dict(kinds.most_common()))
print('legacy:', sum(c['legacy'] == 'yes' for c in main), ' Rust target:', sum(c['targets_rust'] == 'yes' for c in main))
print('LLM role:', dict(Counter(c['llm_role'] for c in main).most_common()))

# ---------------------------------------------------------------- RQ1 (Figure 2, Table 6)
section('RQ1: oracle frequency (Figure 2)')
for o in ORACLES:
    print('  %s %s' % (o, pct(sum(has(c, o) for c in main), N)))
print('number of oracles per paper:', dict(sorted(Counter(int(c['n_oracles']) for c in main).items())))
no_tb = [c for c in main if not test_based(c)]
print('no test-based oracle, i.e. no oracle that executes the code (none of O-c..O-f):', len(no_tb))
single = [c for c in no_tb if c['n_oracles'] == '1']
print('  of these, a single oracle:', len(single), sorted(c['cite_key'] for c in single))
judged = [c for c in no_tb if has(c, 'O-h') or has(c, 'O-i')]
print('  of these, human or LLM judgment:', len(judged), sorted(c['cite_key'] for c in judged))
print('run the original program to compare (O-f or O-g):', sum(has(c, 'O-f') or has(c, 'O-g') for c in main))
print('existing tests but no compile rate (O-c without O-b):', sum(has(c, 'O-c') and not has(c, 'O-b') for c in main))
print('differential testing as the only test-based oracle:',
      sum(has(c, 'O-f') and not any(has(c, o) for o in ('O-c', 'O-d', 'O-e')) for c in main), 'of', sum(has(c, 'O-f') for c in main))
print('mean oracles by track:', {t: round(sum(int(c['n_oracles']) for c in main if c['track'] == t) /
                                     sum(c['track'] == t for c in main), 1) for t in sorted(set(c['track'] for c in main))})
section('RQ1: oracle combinations (Table 6, lower triangle)')
print('     ' + ' '.join('%4s' % o for o in ORACLES))
for i, a in enumerate(ORACLES):
    print('%-4s ' % a + ' '.join('%4d' % sum(has(c, a) and has(c, b) for c in main) for b in ORACLES[:i + 1]))

# ---------------------------------------------------------------- RQ2 (Table 7, Table 8)
section('RQ2: oracle use by context (Table 8)')
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
legacy = [c for c in main if c['legacy'] == 'yes']
n_oc = sum(has(c, 'O-c') for c in main)
print('legacy papers expected to use existing tests if legacy made no difference: %.1f (%d x %d / %d)'
      % (len(legacy) * n_oc / N, len(legacy), n_oc, N))
lib = [c for c in main if 'LIB' in c['migration_kinds'].split(';')]
lib_oi = [c for c in lib if has(c, 'O-i')]
print('LIB papers with human evaluation:', of(len(lib_oi), len(lib)), ' of these also executing the code:',
      sum(test_based(c) for c in lib_oi))
section('RQ2: origin of test-based oracles (Table 7)')
codes = Counter(k for c in main for k in origins(c))
for k in ['c:B', 'c:P', 'c:BP', 'd:S', 'd:H', 'e:S', 'e:U', 'f:F', 'f:T', 'f:L', 'f:C', 'f:U']:
    print('  %-5s %d' % (k, codes[k]))
for o in ['c', 'd', 'e', 'f']:
    print('  O-%s rows sum to %d' % (o, sum(v for k, v in codes.items() if k.startswith(o + ':'))))
lv = Counter(); xl = Counter()
for c in main:
    oc = [k for k in origins(c) if k.startswith('c:')]
    if not oc:
        continue
    ks = set(c['migration_kinds'].split(';'))
    if ks & {'LIB', 'VER'}:
        lv[oc[0]] += 1
    elif 'XL' in ks:
        xl[oc[0]] += 1
print('LIB or VER papers:', sum(bool(set(c['migration_kinds'].split(';')) & {'LIB', 'VER'}) for c in main))
print('existing-test origin, library or version migration:', dict(lv), ' translation (XL):', dict(xl))
cde = [c for c in main if any(has(c, o) for o in ('O-c', 'O-d', 'O-e'))]
print('papers with O-c, O-d or O-e:', len(cde), ' origin of expected outputs not stated (e:U):',
      sum('e:U' in origins(c) for c in cde))
print('differential-testing papers with inputs not described (f:U):',
      of(sum('f:U' in origins(c) for c in main if has(c, 'O-f')), sum(has(c, 'O-f') for c in main)))

# ---------------------------------------------------------------- RQ3 (Figure 3, Table 9, Table 10)
section('RQ3: several oracles on the same outputs')
mg = Counter(g for c in main for g in c['multi_oracle_group'].split(';') if g and g != 'none')
grp = lambda c: set(c['multi_oracle_group'].split(';'))
combine = [c for c in main if int(c['n_oracles']) >= 2]
sep = [c for c in main if c['multi_oracle_group'] not in ('', 'none')]
print('papers combining oracles:', len(combine), ' with separate numbers on the same outputs:', len(sep),
      ' without:', len(combine) - len(sep))
print('   by group (a paper can be in two):', dict(mg))
f3_ids = [c for c in sep if 'figure3' in grp(c)]
t9_only = [c for c in sep if 'table9' in grp(c) and 'figure3' not in grp(c)]
print('   Figure 3:', len(f3_ids), ' table of other comparisons only:', len(t9_only),
      ' other:', sum(grp(c) == {'other'} for c in sep), ' comparable (Figure 3 or table):', len(f3_ids) + len(t9_only))
gaps = [float(r['gap_points']) for r in fig3]
print('Figure 3 rows:', len(fig3), ' gap range: %.0f to %.0f points' % (min(gaps), max(gaps)),
      ' gap above 10 points:', sum(g > 10 for g in gaps), ' above 20 points:', sum(g > 20 for g in gaps))
own = {r['candidate_id']: float(r['compile_rate_pct']) - float(r['behavioral_rate_pct']) for r in fig3_own}
gaps_own = [own.get(r['candidate_id'], float(r['gap_points'])) for r in fig3]
print('   with the paper\'s own system where it reports both rates (figure3_own_system.csv: %s): gap range %.0f to %.0f'
      ' points, above 10 points: %d' % (', '.join(r['short_name'] for r in fig3_own), min(gaps_own), max(gaps_own),
                                        sum(g > 10 for g in gaps_own)))
for r in fig3:
    print('  %-26s %6.2f %6.2f  gap %3.0f' % (r['short_name'], float(r['compile_rate_pct']), float(r['behavioral_rate_pct']),
                                         float(r['gap_points'])))
print('Table 9 rows:', len(tab9), ' papers by group:',
      dict(Counter(g for g, _ in sorted({(r['group'], r['short_name']) for r in tab9}))))


def numbers(s):
    return [float(x) for x in re.findall(r'\d+(?:\.\d+)?', s)]


sim = defaultdict(list)
for r in tab9:
    if r['group'] == 'Similarity next to a pass rate':
        sim[r['short_name']].append(numbers(r['result'])[:2])
rev = sorted(p for p, v in sim.items() if (v[0][0] - v[1][0]) * (v[0][1] - v[1][1]) < 0)
print('similarity next to a pass rate:', len(sim), 'papers; the two rows are ranked in opposite order in', len(rev), rev)
em = [p for p in sim if any('exact match' in r['oracles_compared'] for r in tab9 if r['short_name'] == p)]
print('   papers with exact match:', sorted(em), ' exact match below the pass rate in every row:',
      all(a > b for p in em for a, b in sim[p]))
section('RQ3: stated limitations (Table 10)')
for k, v in Counter(c['limitation_theme'] for c in main).most_common():
    print('  %2d  %s' % (v, k))
theme = lambda c, t: c['limitation_theme'].startswith(t)
print('limitation of the own oracle stated:', of(sum(not theme(c, 'No limitation') for c in main), N))
oc = [c for c in main if has(c, 'O-c')]
weak = [c for c in oc if theme(c, 'Weak or few tests')]
print('papers with existing tests naming weak or few tests:', of(len(weak), len(oc)), ' by origin:',
      dict(Counter([k for k in origins(c) if k.startswith('c:')][0] for c in weak)))
print('single oracle without executing the code, no limitation stated:',
      of(sum(theme(c, 'No limitation') for c in single), len(single)))
of_ = [c for c in main if has(c, 'O-f')]
print('differential-testing papers naming incomplete checks:', of(sum(theme(c, 'Incomplete') for c in of_), len(of_)))
section('RQ3 and RQ4: other counts')
oi = [c for c in main if has(c, 'O-i')]
no_agree = [c for c in oi if c['reports_rater_agreement'] != 'yes']
print('human evaluation papers:', len(oi), ' reporting rater agreement:', len(oi) - len(no_agree),
      ' without:', len(no_agree), ' of these naming subjective evaluation:',
      sum(theme(c, 'Subjective') for c in no_agree))
print('final oracle also used in the technique:', dict(Counter(c['final_oracle_also_used_in_technique'] for c in main
                                                              if c['final_oracle_also_used_in_technique'])))
print('formal verification papers targeting Rust:', sum(has(c, 'O-g') and c['targets_rust'] == 'yes' for c in main),
      'of', sum(has(c, 'O-g') for c in main))
print('LLM-generated tests / LLM judges by year:',
      dict(Counter(c['year'] for c in main if has(c, 'O-e'))), dict(Counter(c['year'] for c in main if has(c, 'O-h'))))

# ---------------------------------------------------------------- Counts from reading the full texts
section('Counts from reading the full texts (4_coding/reading_counts.csv)')
by_count = defaultdict(list)
for r in reading:
    by_count[r['count_id']].append(r)
for cid in sorted(by_count):
    rs = by_count[cid]
    cats = Counter(r['category'] for r in rs)
    line = '  %-44s %2d papers' % (cid, len({r['candidate_id'] for r in rs}))
    if cid.startswith('slip_past'):
        line += '  largest n per paper: %d' % max(int(r['n']) for r in rs)
    elif len(cats) <= 4:
        line += '  ' + str(dict(cats.most_common()))
    print(line)

# ---------------------------------------------------------------- Checklist (Section 7.3, column "In the map")
section('Checklist (Section 7.3, column "In the map")')
rc = lambda cid, cat=None: sum(1 for r in by_count[cid] if cat is None or r['category'] == cat)
print('1. behavioral rate over compiling outputs only:', of(rc('denominator_excludes_noncompiling'), len(fig3)),
      'papers in Figure 3')
print('2. O-a with a behavioral rate on the same outputs:', of(len(sim), sum(has(c, 'O-a') for c in main)),
      '; O-b:', of(len(f3_ids), sum(has(c, 'O-b') for c in main)))
print('3. rater agreement:', of(len(oi) - len(no_agree), len(oi)), '; judge accuracy:',
      of(rc('judge_accuracy_reported') - rc('judge_accuracy_reported', 'no accuracy figure'),
         sum(has(c, 'O-h') for c in main)))
print('4. origin not stated:', of(sum('e:U' in origins(c) for c in cde), len(cde)), 'papers with O-c, O-d or O-e')
print('5. results on tests the system neither produced nor used:', rc('hidden_vs_own_tests'), 'paper')
print('6. compared with the original:', of(len(of_), N), '; inputs not described:',
      of(sum('f:U' in origins(c) for c in of_), len(of_)))
print('7. limitations stated:', of(sum(not theme(c, 'No limitation') for c in main), N))
