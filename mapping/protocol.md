# Protocol and codebook

This document states the protocol followed in the study *How Is Behavioral Equivalence Evaluated in
LLM-Based Code Translation and Migration? A Systematic Mapping Study* and defines every code used
in the data files. Section numbers refer to the paper.

## 1. Research questions

- **RQ1.** Which oracles are used to evaluate behavioral equivalence in LLM-based code translation and migration?
- **RQ2.** Where do test-based oracles get their ground truth, and how does oracle use differ by context? The contexts
  are a legacy source or not, the kind of migration, the track and the year.
- **RQ3.** Which threats to oracle reliability do the studies acknowledge or demonstrate?
- **RQ4.** How do automatic oracles that do not execute the code compare with existing tests on the same LLM translations?
  Answered by the pilot (`pilot/`), not by the mapping.
- **RQ5.** What gaps separate current evaluation practice from the needs of real migration projects, and what
  should studies report and investigate next?

## 2. Scope (Section 4.1)

A paper is in scope if it appears in the 2024, 2025 or 2026 edition of ICSE, FSE or ASE: in any track of the
conference program, including the poster, doctoral symposium and student research competition tracks; in the
conference's main or Companion volume; or, for journal-first papers, as a presentation at the conference. We call
this set the main proceedings. Co-located workshops and conferences that publish their own proceedings, and events
co-hosted in a single year only (ISSTA 2025, Internetware 2025), are out of scope. Workshop papers that appear in a
Companion volume are scanned with that volume.

## 3. Search (Section 4.2)

- **Sources.** The program of each conference-year on conf.researchr.org, every track that had a published
  paper list. Main and Companion volumes were cross-checked through Crossref, which added 216 papers that appear
  in no track program (`track` starts with the volume name in `1_search/scanned_papers.csv`); none of their 13
  keyword hits was included. Missing abstracts were taken from
  Semantic Scholar and Crossref. See `1_search/search_log.csv`.
- **Date of the final scan.** October 23, 2026.
- **String**, applied to titles and abstracts (case-insensitive; `*` is a wildcard):

  ```
  translat* OR transpil* OR migrat* OR moderni* OR legacy OR porting OR ported OR upgrad*
  OR deprecat* OR "cross-language" OR "cross-lingual" OR equivalen*
  ```

- **Papers without an abstract** (80) were matched against the string on their title only, and screened on it.
- **Recall estimate.** 40 in-scope papers that meet the criteria were known before the scan, from exploratory
  searches of the same proceedings and from related work; column `recall_set` of `2_screening/candidates.csv`
  marks them. The string retrieved 39 of them. The one miss (`C169`) was added to the candidates as a known paper.
  The scan found the other 12 included papers.
- **Candidates.** All keyword hits plus that known paper (`2_screening/candidates.csv`, column `source`).

## 4. Selection criteria (Section 4.3)

A paper is included if it satisfies I4 and at least one of I1–I3, provided that no exclusion criterion applies.

| Code | Criterion |
| --- | --- |
| I1 | Uses a neural model or LLM to translate or migrate code between a named source and target (language, version, dialect, library or API, framework) and describes how equivalence is checked, even if only by BLEU |
| I2 | Proposes or studies a method, benchmark or oracle to evaluate translations or migrations |
| I3 | Detects equivalence between programs in two different languages; reported as a separate tier |
| I4 | English, peer-reviewed |
| E1 | Natural-language translation, or NL-to-code tasks with no code-to-code translation |
| E2 | No information at all on how outputs are evaluated |
| E3 | Clone or similarity detection that neither targets functional equivalence nor relates to translation |
| E4 | Secondary study |
| E5 | Duplicate of the same work (the most complete version is kept) |
| E6 | Full text unavailable |

Under E5 the most complete version is kept even when it lies outside the scope; this applies to one candidate
(`C317`, whose full version appeared at MSR 2024), so that work is not mapped. One candidate first excluded under E6
(`C041`, DLBench) was included after an author version was found.

Additional codes used in column `criterion` of `candidates.csv` for exclusions:

| Code | Meaning (as worded in the paper) |
| --- | --- |
| `¬I1 ¬I2` | Neither translation nor its evaluation |
| `¬I1` | Related topic that meets none of I1–I3 (e.g. purely rule-based translation, refactoring with no target, program repair) |
| `I3-instr` | Same-language equivalence detection |

Inclusion codes: `I1`, `I2`, `I3`, or combinations such as `I1/I2`.

### Clarification rules (column `clarification_rule`)

| Rule | Decision |
| --- | --- |
| L-TEST | Tests count as code: migrating tests between languages or libraries with a neural model or LLM meets I1 |
| L-BASE | A study proposing a deterministic technique meets I1 if the technique and an LLM baseline are evaluated with the same oracle and both results are reported |
| L-ARCH | Microservice extraction and other architecture changes do not meet I1: they restructure a system rather than move its code to another language, version, library, dialect or framework |
| L-DECOMP | Decompilation does not meet I1: it starts from a binary rather than from source code |
| L-DATA | A dataset without an evaluation protocol is E2; one with a protocol meets I2 |
| L-RB | An oracle or benchmark for rule-based translators still meets I2 |
| L-XEQ | Cross-language equivalence detection meets I3, even when a paper frames it as clone detection |
| L-TASK | Translation must be a main goal or research question to meet I1 or I2; general models or benchmarks in which translation is one of three or more tasks, and papers that use translation only as a means, are excluded |
| L-SUM | A paper that summarizes its authors' published results counts as a duplicate (E5) |

## 5. Screening (Sections 4.3–4.4)

- Exclusions could be decided on title and abstract, and on the title alone when no abstract was available.
  Every inclusion required reading the full text.
- Column `decision_basis` records the deepest level read: `title`, `abstract` or `full text`.
- Column `basis_note` records the version read: for example an arXiv preprint, or that only a paywalled
  version existed (E6).
- Column `recall_set` marks the 40 known papers of the recall estimate (see Search above).
- Hard cases were discussed within the team until agreement was reached.
- Study quality was not scored: the RQs ask how studies evaluate equivalence, and RQ3 records the weaknesses that
  the studies state or show.

## 6. Extraction form (Section 4.5, Table 4)

`3_extraction/extraction.csv` has one row per included paper with these fields. The rows are the drafts written
from the full text; where they differ from `4_coding/coding.csv`, for example after the coding rules of Section 4.5
were applied, the coding is final.

1. **Migration kind** (several allowed) and **legacy flag**.
2. **Track.**
3. **Role of the LLM.**
4. **Oracles** that judge the final output.
5. **Origin** of each test-based oracle: where its tests or inputs come from.
6. **Several oracles on the same outputs.** Whether two or more oracles were applied to the same outputs, and
   if so, the numbers under each.
7. **Stated limitations** of the paper's own oracle, with location, later grouped into one main theme per paper.

The `evidence` column gives short quotations and locations in the paper.

## 7. Codes in `4_coding/coding.csv`

**Migration kinds** (`migration_kinds`, several allowed):
- `XL`: between programming languages.
- `VER`: between versions of a language or platform.
- `LIB`: between libraries or APIs, including dependency upgrades with breaking changes.
- `DIA`: between dialects.
- `FW`: between frameworks or application platforms.

`legacy = yes` marks a source written for a language or platform that is no longer in mainstream use, such as
COBOL, PL/I, mainframe systems or ASP.NET WebForms. C sources and deprecated APIs are not flagged, even when a paper
calls them legacy. Code hints does so for deprecated APIs, and at least five C-to-Rust papers that use existing tests
do so for C (`c_source_called_legacy_with_existing_tests` in `4_coding/reading_counts.csv`); flagging these five
would give 5 of 10 legacy papers with existing tests instead of none of 5.

**Track**: Research, Industry/SEIP, Journal-first, NIER, Ideas, Visions and Reflections, Poster, Demonstration.

**LLM role** (`llm_role`): proposed technique; evaluated subject; both (two values separated by `;`); baseline
only; evaluation tooling; no LLM (a smaller neural model or no model). The role is coded by what the LLM does in
the study, whatever kind of technique is proposed: a non-LLM technique compared with LLM baselines is
`baseline only`.

**Oracles** (`oracles`). Only oracles that judge the final output are coded. An oracle used solely inside the
technique (for example a compiler in a repair loop, or a filter on training data) is not coded. Further rules:
- An oracle is coded only if the paper reports its result on the evaluated outputs.
- O-b is coded when the paper reports how many outputs pass compilation or a syntax check, as a rate or as a
  breakdown of failures by stage, in the text, a table or a figure. Compilation implied only by passing tests is
  not coded.
- If a system translates tests along with the code, checks that touch only the translated tests (for example compiling
  them) are not oracles of the translation.
- The four test-based oracles (O-c to O-f) are told apart by where the expected outputs come from. Tests that an
  LLM writes but whose expected outputs come from running the original are differential testing (O-f). When a
  paper does not say where the expected outputs of LLM-written tests come from, they are coded O-e.
- In test migration, where the migrated test is itself the output, running it on the target counts as O-d.
- Tests that benchmark builders translated by hand count as benchmark tests (O-c, origin `c:B`); tests that a paper's
  authors translate for their own evaluation count as translated tests (O-d, origin `d:H`).

| Code | Oracle | What it checks |
| --- | --- | --- |
| O-a | Surface similarity (BLEU, CodeBLEU, exact match, AST match) | Closeness to a reference solution |
| O-b | Compilation, type checking or another well-formedness check | The output is well-formed in the target |
| O-c | Existing tests | Behavior on a test suite that existed before the study, built for a benchmark or by the project's developers |
| O-d | Translated tests | Behavior on the original program's own tests after they are translated for the study; in test migration, on the migrated tests themselves |
| O-e | LLM-generated tests | Behavior on new tests whose expected outputs come from an LLM or a specification |
| O-f | Differential testing | Same results as the original program, run by the study on the same inputs (for example from fuzzing, existing tests or an LLM) |
| O-g | Formal verification | Equivalence proven or bounded-checked against the original or a specification |
| O-h | LLM judge | An LLM's verdict on equivalence |
| O-i | Human evaluation | A person's judgment |

**Origin of test-based oracles** (`oracle_origin`, main corpus only; one or more codes per oracle):

| Code | Meaning |
| --- | --- |
| `c:B` | Existing tests built for a benchmark (curated problems, reference translations). Tests that benchmark builders translated by hand count here. |
| `c:P` | Existing tests: a real project's own test suite |
| `c:BP` | Existing tests of both kinds |
| `d:S` | Translated tests, translated by the system under evaluation |
| `d:H` | Translated tests, translated by hand by the paper's authors |
| `e:S` | LLM-generated tests derived from the specification that also generates the code |
| `e:U` | LLM-generated tests; origin of expected outputs not stated |
| `f:F` | Differential testing with inputs from fuzzing, property-based testing or symbolic execution |
| `f:T` | Differential testing with inputs from existing tests or benchmark data |
| `f:L` | Differential testing with LLM-generated inputs |
| `f:C` | Differential testing on curated samples or rendered screens |
| `f:U` | Differential testing; inputs not described |

**Limitation theme** (`limitation_theme`): one main theme per paper, as in Table 9 of the paper.

**Several oracles on the same outputs** (`multi_oracle_group`). Used for papers that report, in the text or
tables, numbers under two or more oracle categories for the same outputs:
- `figure3`: the paper reports both a compile (or well-formedness) rate and a behavioral pass rate. Data in
  `figure3_compile_vs_behavior.csv`.
- `table8`: the paper reports one of the three groups of other comparisons in RQ3: a similarity score next to a
  pass rate; how many outputs that pass tests or fuzzing also pass a further check; or a mutation score next to CA.
  Data in `table8_other_disagreements.csv`, with one or two settings per paper; the `note` column says what holds
  across the paper's other settings. A paper can be both `figure3` and `table8`.
- `other`: the paper reports per-oracle numbers in another form.
- `none`: none of the above.

Papers close to these three groups but not in them: RustAssure runs differential fuzzing and symbolic testing on
different transpilations (FLUORINE's and its own); RISE does not report how many outputs its manual step rejects;
EvoC2Rust reports similarity at project level and tests at module level; Python library migration runs tests on 25
of its 314 outputs; Rule synthesis compares similarity with manual review, without a pass rate; AlphaTrans and
ReCodeAgent compare two test suites, which is not one of the three groups.

**Other flags**:
- `targets_rust`: Rust is a target language.
- `reports_rater_agreement`: for papers with O-i, whether an agreement figure between raters is reported.
- `final_oracle_also_used_in_technique`: flagged during extraction, not coded systematically.

## 8. Counts from reading the full texts (`4_coding/reading_counts.csv`)

A few counts in the paper rest on a reading of the full texts rather than on a field of the extraction form. They
are recorded in `4_coding/reading_counts.csv`, one row per paper and count, with the location in the paper and a
short quotation. Column `used_in` names the place in the paper where the count appears, `category` the value for
that paper, and `n` a number where the row needs one: the number of kinds in a classification, of kinds of fault or of
checks, of LLMs compared, or the size of a sample or a denominator.
Where the paper says "at least", the rows give a lower bound.

| `count_id` | A paper is counted when it |
| --- | --- |
| `fault_classification` | classifies the failures of migrated code into kinds |
| `slip_past_kinds`, `slip_past_oracles` | describes kinds of fault that pass one check but not another, and which checks |
| `ranking_benchmark_vs_real` | ranks systems differently on a benchmark and on real projects |
| `hidden_vs_own_tests` | reports pass rates both on tests the system translated itself and on tests it never saw |
| `c_source_called_legacy_with_existing_tests` | migrates C to Rust, calls the C code legacy and uses existing tests |
| `no_separate_numbers` | combines oracles without separate numbers on the same outputs; `category` gives why |
| `other_comparison` | reports several oracles on the same outputs but fits neither Figure 3 nor the table of other comparisons; `category` gives why |
| `partial_human_check` | has people check only part of the outputs |
| `translated_tests_with_code` | evaluates a system that translates the tests; `category` says whether it also translates the code |
| `baseline_smaller_model` | uses the LLM only as a baseline; `category` gives the kind of technique proposed |
| `judge_accuracy_reported` | uses an LLM judge; `category` says whether its accuracy on known answers is reported |
| `denominator_excludes_noncompiling` | computes its behavioral rate over the compiling outputs only (Figure 3 recomputes it over all outputs) |
