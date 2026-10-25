# Revision: RQ1 and RQ2 (Sections 5.1–5.3)

File: `Seminar_2/sections/05-results.tex`. Every number below was recomputed from `mapping/4_coding/coding.csv`
or checked against `mapping/3_extraction/extraction.csv`.

- **Part A** can be pasted now. It changes wording and adds one table block. No existing count changes, except that
  "three papers with a single weak oracle" becomes five because "weak" is now defined.
- **Part B** lists decisions the team must take first. They change counts: update the xlsx, then the paper.
- **Part C** lists edits needed in other people's sections.

When you paste a block, also delete the `\cmt{Hà Cao}{...}` note that follows the old sentence.

---

## A. Ready to paste

### A1. 5.1: normalize the yearly growth

Why: 8 → 14 → 27 papers partly reflects proceedings that grow from 1,171 to 1,856 papers.

```latex
The corpus grows quickly: \new{8 papers are from 2024, 14 from 2025 and 27 from 2026, or 0.68\%, 0.98\% and 1.45\% of the papers scanned in each year; Table~\ref{tab:search} gives the counts per conference. The 2024 count may be slightly low, since 61 ICSE~2024 papers could be matched on their title only.}
```

### A2. RQ1: state what is counted

Why: 7 of the 28 papers with existing tests report no compile rate, although their code must compile, so O-b counts
*reported* compilation. Put this right after the first sentence of 5.2.

```latex
Compilation and existing tests dominate; formal verification and LLM judges are rare (Figure~\ref{fig:oracle-freq}). \new{We count an oracle when a paper reports its result on the final outputs. An oracle whose result is not reported, such as compiling the code before running its tests, is not counted; this affects compilation most, since 7 of the 28 papers with existing tests report no compile rate.}
```

Figure 2 caption:

```latex
\caption{Oracles used by the 49 main-corpus papers. A paper can use several oracles. \new{An oracle is counted when the paper reports its result on the final outputs.}}
```

### A3. RQ1: define "weak oracle"

Why: Pig and PL/I rely on human judgment alone, which Table 1 also lists as weak. "Three" was therefore a
selective count. **Knock-on:** G6 must change "all three" to "4 of the 5" (see C2).

```latex
Most papers combine oracles: 9 use one, 17 use two, 17 use three, and 6 use four or more, up to eight in ReCodeAgent~\cite{recodeagent}. Nine papers use no oracle that executes code (none of O-c to O-f): they judge outputs by compilation, similarity, a human or an LLM. \new{Five rely on a single oracle that does not execute the code: 2 report only BLEU or CodeBLEU~\cite{vimpt,collaboration}, one only an LLM judge~\cite{wca4z}, and 2 only human judgment~\cite{pig,pli}.}
```

### A4. RQ1: no paper relies on compilation alone; replace the mean per track

Why:
- 31 of the 33 papers that use compilation also run the code. The other two add similarity (CodePlan) or human and LLM
  judgment (DepUpgrade).
- The old means used 3 of 7 tracks, NIER has n=3, and ReCodeAgent (8 oracles) lifts the research mean to 2.8; without
  it the mean is 2.59.
- Medians: research 3, industry/SEIP 3, journal-first 2, short papers 2.

```latex
\begin{added}
Table~\ref{tab:cooc} shows which oracles are combined. Compilation accompanies most other oracles: 21 of the 28 papers with existing tests also \new{use compilation as an oracle}, and so do 13 of the 18 with human evaluation. \new{Conversely, no paper relies on compilation alone: 31 of the 33 papers with compilation also run the code, and the other two add surface similarity~\cite{codeplan} or human and LLM judgment~\cite{depupgrade}.} Differential testing seldom appears next to existing tests (3 of 13 papers), and in 8 of the 13 no \new{test-suite oracle} (O-c, O-d, O-e) is used. Both papers with formal verification also run differential tests. \new{The median paper uses 3 oracles in the research and industry/SEIP tracks and 2 in journal-first and short papers; short papers may, however, describe their evaluation in less detail (Section~\ref{sec:threats}).}
\end{added}
```

### A5. RQ2: opening sentence. Not causal; state the proxy

Why:
- "Follows its context" reads as causal.
- RQ2 asks about settings with and without existing tests, but test availability was never coded. The legacy flag
  was an unstated proxy.

```latex
\new{Oracle use differs by context in this corpus (Table~\ref{tab:context}). We did not code whether the studied systems have usable tests; the closest context we coded is the legacy flag, which we use as a proxy for settings without them. Because the groups are small (2 to 44 papers), we read a pattern only where a count departs clearly from what the group's size would predict.}
```

### A6. Table 6: add LLM-role rows

Why: contribution (1) in the Introduction promises a map by LLM role, but the role was never crossed with the
oracles. The rows reveal a finding (see A10). "Other" groups baseline only (1), evaluation tooling (1) and no LLM (2).
These 4 papers carry the coding inconsistency in B6, so the table is not affected by it.

Insert between the track rows and the year rows:

```latex
    \midrule
    \new{Proposed technique}  & 32 & 8 & 23 & 17 & 5 & 5 & 8 & 1 & 3 & 12 \\
    \new{Evaluated subject}   & 9  & 2 & 6  & 7  & 1 & 0 & 2 & 0 & 0 & 3  \\
    \new{Both}                & 4  & 2 & 2  & 3  & 1 & 0 & 1 & 1 & 0 & 2  \\
    \new{Other}               & 4  & 2 & 2  & 1  & 0 & 0 & 2 & 0 & 0 & 1  \\
```

Add to the end of the caption:

```latex
\new{LLM role as in Section~\ref{sec:overview}; Other: baseline only, evaluation tooling or no LLM.}
```

Each column sums to the oracle totals: 14, 33, 28, 7, 5, 13, 2, 3, 18. Also add these rows to
`mapping/analysis/recompute.py`, so that Table 6 stays fully recomputable.

### A7. Legacy bullet: hedge

Why:
- n=5.
- Legacy is confounded with track: all 5 legacy papers are industry/SEIP or NIER.
- The finding depends on the narrow legacy definition. EvoC2Rust, SmartC2Rust and Code hints call their sources
  legacy but are not flagged, and EvoC2Rust and SmartC2Rust use existing tests.
- It is still the one zero cell worth reporting: about 2.9 papers expected, P(0) ≈ 0.01.

```latex
  \item \textbf{\new{No legacy paper uses existing tests.}} Two of the 5 legacy papers run the original system as a differential oracle~\cite{kcobagent,coboljava}, one generates tests with an LLM from an extracted specification~\cite{ipmodern}, one uses an LLM judge~\cite{wca4z}, and one \new{compares the generated Java with the expected code by hand}~\cite{pli}. \new{This is the one zero cell in Table~\ref{tab:context} that the group sizes do not predict (about 3 papers expected). Two caveats apply. All five legacy papers appear in the industry/SEIP or NIER tracks, so legacy and track cannot be told apart. And the result depends on our legacy definition (Section~\ref{sec:background}): three papers that call their C or Java sources legacy are not flagged, and two of them use existing tests~\cite{evoc2rust,smartc2rust}.}
```

### A8. LIB bullet: presence is not reliance

Why:
- 8 of the 12 LIB papers also run the code. Only 3 assess behavior without running it: Pig, DepUpgrade and Rule
  synthesis.
- Some human checks cover only part of the outputs: Fruntke & Krinke grade a 20% sample, BDUpdater the 24 cases that
  have a developer fix.
- The causal explanation from pylibmig (27 of 314) is removed, since the Discussion already cites it.

```latex
  \item \textbf{\new{Library migration adds human checks.}} \new{Nine of the 12} LIB papers include human evaluation, against 7 of 33 XL papers. \new{For most of them it is an additional check: 8 of the 12 also run the code, and only 3 assess behavior without running it, relying on human or LLM judgment~\cite{pig,depupgrade,rulesynth}. Some human checks cover only part of the outputs, such as a 20\% sample of the patches that pass the tests~\cite{fruntke} or the 24 cases that have a developer's fix~\cite{bdupdater}.} No LIB paper uses LLM-generated tests or formal verification.
```

### A9. Formal-verification bullet: n=2

Why: 13 of 49 papers target Rust, so both O-g papers landing there has P ≈ 0.07 by chance alone.

```latex
  \item \textbf{\new{Both formal-verification papers target Rust}~\cite{rustassure,vert}.} \new{With only two such papers, this is an observation rather than a pattern.}
```

### A10. LLM-based oracles: scope the time claim and add the LLM-role finding

Why:
- UniTrans (2024) and Collaboration (2025) already use LLM-generated tests inside the technique. "Only in 2026" holds
  for final-output oracles only.
- 2026 holds 27 of the 49 papers, so all 3 LLM judges falling in 2026 has P ≈ 0.16 by chance.
- From A6: all 7 papers with an LLM-based oracle propose the technique they evaluate. None of the 13 papers that
  evaluate LLMs as subjects uses one, and the 9 that only evaluate LLMs rely on existing tests (7 of 9).

```latex
  \item \textbf{LLM-based oracles are new\new{ and come with the technique}.} \new{As oracles for the final output,} all 5 papers with LLM-generated tests and all 3 with LLM judges are from 2026\new{; earlier papers used LLM-generated tests only inside the technique~\cite{unitrans,collaboration}. All 7 of these papers (ReCodeAgent uses both) also propose the technique they evaluate: none of the 13 papers that evaluate LLMs as subjects, alone or alongside a technique, uses an LLM-based oracle, and the 9 that only evaluate LLMs rely on existing tests (7 of 9). With 27 of the 49 papers from 2026, a larger sample is needed to confirm the trend over time.}
```

### A11. New bullet: track

Why: RQ2 asks "in which track", but the old text only touched on track through legacy and short papers.

```latex
  \item \textbf{\new{Journal-first papers stay with existing tests.}} \new{All 5 use existing tests and none uses human evaluation, whereas half of the research papers (14 of 28) include human evaluation.}
```

### A12. Zero cells: add the caveat

Why: 12 of the 13 zero cells listed have expected counts of only 0.2–1.4 papers, so a zero is unsurprising.

```latex
  \item \textbf{\new{Zero cells}} mark combinations \new{that no paper uses}: legacy with \new{similarity,} existing, translated or formal-verification oracles; library migration with LLM-generated tests or formal verification; dialect translation with any \new{test-suite} oracle; and short papers with translated tests, generated tests, \new{formal verification} or LLM judges. \new{Apart from legacy with existing tests, these groups are small enough that a zero is expected by chance (0.2 to 1.4 papers expected), so the cells show gaps in this corpus, not settled absences.}
```

### A13. Origin paragraph: "the norm" in LIB/VER

Why: only 7 of the 14 LIB/VER papers use existing tests at all.

```latex
\new{In library and version migration, 6 of the 7 papers that use existing tests rerun the client project's own suite after the change~\cite{fruntke,byam,bdupdater,freshbrew}; the other 7 LIB and VER papers use no existing tests.} In translation between languages, benchmark tests are more common: 12 papers, against \new{6} with project suites and \new{2} with both.
```

### A14. IntentTester: say what its "translated tests" show

Why: the migrated tests are the output itself, and they run pass/fail on the target library without any comparison
with the original. Whether to keep the O-d code is B2.

```latex
in IntentTester the migrated tests are themselves the output under evaluation, and they are run without comparison with the original tests, so a pass shows that a migrated test passes on the target library, not that it checks the same behavior~\cite{intenttester}.
```

### A15. Cleanup

- Delete the commented-out old paragraph above `\paragraph{Where the ground truth comes from.}`. It starts with
  `%% Previous paragraph, replaced by the analysis below`.

---

## B. Team decisions needed. These change counts: update the xlsx first, then the paper

| # | Decision | Papers | Effect if changed |
|---|---|---|---|
| B1 | **O-e vs O-f.** Proposed rule: if the expected outputs come from running the original at evaluation time, the oracle is O-f, whoever wrote the inputs; the input source goes to the origin field. Also settle BatFix: it is coded O-c, but the extraction says "O-f in nature". | TRAVEL (O-e), PtrTrans (O-e + O-f), ReCodeAgent, PROGnosticator (O-f, f:L), BatFix | O-e 5 → 2. O-f gains TRAVEL. Fig. 2, Tables 5–7, A10 and the abstract change. |
| B2 | **IntentTester O-d.** The migrated tests are the output, so they are not an equivalence oracle. | IntentTester | O-d 7 → 6, d:S 5 → 4 |
| B3 | **ReCodeAgent O-h and O-a.** Both judge the translated tests, not the translation (§4.3 of the paper; check before recoding). | ReCodeAgent | O-h 3 → 2. Abstract 6% → 4%. G4. |
| B4 | **Other boundary rules**: parse-only checks as O-b (O-b in AlphaTrans and Python library migration, not in Rule synthesis); compile rates reported as "secondary" (MBTA 91.11%); sample-only or diagnostic human checks as O-i. | AlphaTrans, PyLibMig, Rule synthesis, MBTA, Lost in Translation, PtrTrans … | The middle of Fig. 2 may reorder. The top two (O-b, O-c) and the bottom two (O-h, O-g) are robust. |
| B5 | **RQ2 "with or without existing tests".** Either add a field (yes / partial / no / unstated; the evidence is often already in extraction.csv), or rephrase RQ2 in the Introduction as legacy vs non-legacy. | all | New rows in Table 6, or a new RQ2 wording |
| B6 | **Legacy definition.** Keep the narrow one (COBOL, PL/I, WebForms) and justify it, or widen it and report both. | EvoC2Rust, SmartC2Rust, Code hints | Wider: 8 legacy papers, 2 with existing tests. The headline in A7 fails. |
| B7 | **LLM-role rule** for a non-LLM technique with LLM baselines. | VIM-PT, Semi-supervised ("no LLM") vs GUIMigrator ("baseline only") | Section 5.1 counts only. Table 6 is unaffected. |
| B8 | **Origin of non-execution oracles**, which RQ2 asks about: for O-h, which model judges and whether it produced the outputs; for O-i, who the raters are. | 3 O-h papers, 18 O-i papers | A new sentence or rows in Table 7 |
| B9 | **Coder agreement.** A second coder codes the 5 calibration papers plus the boundary papers above; report agreement (Threats TODO). | ≈ 20 papers | Reliability evidence for every RQ1/RQ2 count |

Optional, if time allows: add a **primary-oracle** field (the oracle behind the headline result). It would support or
refute "relies on" (A8) and G5.

---

## C. Knock-on edits in other sections

- **C1. Abstract** (00): "library migration relies on human judgment (9 of 12 papers)" → "includes human judgment (9 of
  12 papers)". "LLM-generated tests and LLM judges appear only in 2026" → add "as final-output oracles".
- **C2. G6** (06, Minh): "including all three that rely on a single weak oracle" → "including 4 of the 5 that rely on a
  single oracle that does not execute the code" (see A3).
- **C3. G5** (06, Minh): 31 of the 33 compile papers also run the code, and none relies on compilation alone. Reword
  "Compilation is reported as if it were evidence", or base it on papers whose headline metric is compilation, such as
  DepUpgrade.
- **C4. Implications, benchmark builders** (06): "The zero cells … point to benchmarks that do not yet exist" → "may
  point to" (see A12).
- **C5. Related Work** (03): "13 of 49" counts O-f only. Say "as a differential oracle (O-f)".
- **C6. Introduction** (01): the RQ2 wording depends on B5. Contribution (1) "LLM role" is now covered by A6.
- **C7. Threats** (07): under construct validity, name the O-e/O-f boundary, the legacy definition, and that the codes
  record presence, not reliance.
