# Pilot results

164 tasks.

| Oracle | Accepts (%) |
|---|---|
| O-b compile | 89.6 |
| O-c tests | 80.5 |
| O-a CodeBLEU>=0.5 | 82.3 |
| O-a CodeBLEU>=0.6 | 67.1 |
| O-a CodeBLEU>=0.7 | 51.8 |
| O-h judge | 73.8 |

Compile rate minus test pass rate: 9.1 percentage points. Test outcomes: {'pass': 132, 'compile_error': 18, 'fail': 14}. Interface errors: 1.
CodeBLEU: mean 0.756 when the tests pass, 0.507 when they fail; correlation with the test outcome 0.439.

## Each oracle against the tests

| Oracle | Accepts, passes | Accepts, fails | Rejects, passes | Rejects, fails | Agreement (%) | False acceptance (%) | False rejection (%) |
|---|---|---|---|---|---|---|---|
| O-b compile | 132 | 15 | 0 | 17 | 90.9 | 46.9 | 0.0 |
| O-a CodeBLEU>=0.5 | 118 | 17 | 14 | 15 | 81.1 | 53.1 | 10.6 |
| O-a CodeBLEU>=0.6 | 97 | 13 | 35 | 19 | 70.7 | 40.6 | 26.5 |
| O-a CodeBLEU>=0.7 | 80 | 5 | 52 | 27 | 65.2 | 15.6 | 39.4 |
| O-h judge | 105 | 16 | 27 | 16 | 73.8 | 50.0 | 20.5 |

## Pairwise agreement (%)

| | O-b compile | O-c tests | O-a CodeBLEU>=0.6 | O-h judge |
|---|---|---|---|---|
| O-b compile | 100.0 | 90.9 | 68.9 | 74.4 |
| O-c tests | 90.9 | 100.0 | 70.7 | 73.8 |
| O-a CodeBLEU>=0.6 | 68.9 | 70.7 | 100.0 | 68.9 |
| O-h judge | 74.4 | 73.8 | 68.9 | 100.0 |

## Verdict patterns (O-b compile, O-c tests, O-a CodeBLEU>=0.6, O-h judge; + accepts, - rejects)

| Pattern | Tasks |
|---|---|
| `++++` | 81 |
| `++-+` | 24 |
| `+++-` | 16 |
| `++--` | 11 |
| `----` | 7 |
| `--++` | 5 |
| `+---` | 5 |
| `+-++` | 4 |
| `+--+` | 4 |
| `---+` | 3 |
| `+-+-` | 2 |
| `--+-` | 2 |

76 tasks have at least one oracle that disagrees with the tests.

## Judge on known answers

YES on 97 of 164 reference solutions; NO on 117 of 142 mutants rejected by the tests; balanced accuracy 70.8%.

## Self-check of the harness

Reference solutions (164): 164 compile, 164 pass the tests, 164 score CodeBLEU 1.0, 164 extracted unchanged.
Mutants: 298 generated, 288 compile, 242 rejected by the tests.
