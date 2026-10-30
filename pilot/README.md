# Pilot: one set of translations, four oracles

An LLM translates the 164 HumanEval-X tasks from Python to Java once, and every translation is judged by four
oracles. The tests are the only oracle that executes the translation, so each other oracle is compared with them.

| Oracle | Code in the paper | Accepts a translation when |
| --- | --- | --- |
| Compilation | O-b | `javac` compiles it |
| Existing tests | O-c | the HumanEval-X Java tests pass within 10 seconds |
| Similarity | O-a | its CodeBLEU against the reference solution reaches 0.5, 0.6 or 0.7 |
| LLM judge | O-h | a second model answers YES to "is this Java method equivalent to the Python function?" |

## Files

| File | Content |
| --- | --- |
| `data.py` | Downloads HumanEval-X and pairs each Python function with its Java signature, reference solution and tests |
| `llm.py` | The translation and judge prompts, the Ollama client, and extraction of the code and the YES/NO answer |
| `oracles.py` | The four oracles |
| `pipeline.py` | The stages: self-check, translation, the three oracles that need no model, the judge, the judge on known answers |
| `analyze.py` | Agreement between the oracles: `summary.md`, `summary.json`, `verdicts.csv`, `disagreements.csv` |
| `run.py` | Command line |
| `pilot_kaggle.ipynb` | The full run on a Kaggle GPU; it contains a copy of the six files, so it runs on its own |

The **self-check** runs first: the reference solutions must compile, pass the tests and score CodeBLEU 1.0, and
single-operator mutants of them (for example `<` changed to `<=`) show how many wrong programs the tests catch.
The **judge on known answers** shows the judge each reference solution, which is equivalent, and one mutant per
task that the tests reject, which is not.

## Running

On Kaggle: import `pilot_kaggle.ipynb`, turn on a GPU and Internet, and use Save Version → Save & Run All. The
notebook stores the SHA-256 of the code it ran in `results/code_sha256.json`.

Elsewhere, with Python 3.9+, Java 17+ and Ollama:

```
pip install -r requirements.txt
python run.py all --translator qwen2.5-coder:7b-instruct-q4_K_M --judge llama3.1:8b-instruct-q4_K_M
```

Add `--limit 5` for a quick test. Each stage saves its results as it goes, so an interrupted run continues
where it stopped. `results/run_info.json` records the software versions, the GPU, the model digests and the
prompt hashes.

## Results

The run on a Kaggle T4 GPU on October 25, 2026 is in `results/`: `summary.md` has the rates and counts,
`verdicts.csv` the verdicts and CodeBLEU score of each translation, and `kaggle_run.ipynb` is the executed
notebook. Of the 164 translations, 89.6% compile and 80.5% pass the tests. Of the 32 translations that fail the
tests, compilation accepts 15, CodeBLEU at 0.6 accepts 13 and the LLM judge accepts 16. The judge also rejects 27
of the 132 translations that pass, and 67 of the 164 reference solutions.

## Design choices

- The translator sees the Python function without its docstring, so it translates code instead of solving the
  task again from its description, and it is given the Java signature, so a test failure reflects behavior.
- The task's import lines are put in front of every translation, and `public class Solution` becomes
  `class Solution` when the translation shares a file with the tests.
- The translator (Qwen2.5-Coder 7B) and the judge (Llama 3.1 8B) are different models, so the judge does not
  grade its own output.
- Decoding is greedy with a fixed seed, but a rerun on a GPU can still change some answers. All numbers are
  computed from the saved translations and judgments in `results/`.

## Limitations

HumanEval-X tasks are short single functions with tests, unlike repository-scale code. Of the 288 single-operator
mutants that compile, 46 (16%) survive the tests; some behave like the reference, but at least one does not
(HumanEval/131). One translation fails only because the benchmark misspells a method name that the model corrected
(HumanEval/22). The tests are therefore the best available reference, not the truth. Both models are small, and
HumanEval-X may be in their training data.
