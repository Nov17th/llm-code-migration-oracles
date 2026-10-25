# LLM Code Migration Oracles

Data and scripts for the systematic mapping study **How Is Behavioral Equivalence Evaluated in LLM-Based Code
Translation and Migration?** The paper refers to this repository as its replication package. The final scan of the proceedings was run on October 23, 2026.

| Folder | Content |
| --- | --- |
| `mapping/` | The mapping study: protocol, search, screening, extraction, coding, and a script that recomputes every count in the paper |

## Mapping study

| Step | Files in `mapping/` | In the paper |
| --- | --- | --- |
| Protocol, selection criteria and all codes | `protocol.md` | Sections 1, 2 and 4 |
| 1. Search: every scanned paper, its keyword matches, and the search log | `1_search/` | Section 4.2, Table 2 |
| 2. Screening of the 431 candidates | `2_screening/candidates.csv` | Sections 4.3–4.4, Figure 1 |
| 3. Extraction from the full text of the 51 included papers | `3_extraction/extraction.csv` | Section 4.5, Table 4 |
| 4. Coding of the 51 papers, with the data of Figure 3 and Table 8 | `4_coding/` | Section 5 (Tables 5–9, Figures 2–3), Appendix A |
| 5. Recomputation of every count | `analysis/recompute.py` | All tables and figures |

To recompute the counts (Python 3, standard library only):

```
python mapping/analysis/recompute.py
```

and compare the output with `mapping/analysis/expected_output.txt`.

- `candidate_id` (`C001`–`C431`) identifies a paper in every file.
- `extraction.csv` lists every oracle a paper mentions; `coding.csv` keeps only the oracles that judge the final
  output, and all counts in the paper come from it.
- Abstracts and full texts are not included because publishers hold their copyright; each row gives the DOI or URL.
