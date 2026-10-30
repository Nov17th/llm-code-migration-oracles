# Phản hồi review của Hà Cao và các thay đổi đề xuất (kèm prose)

Mọi con số trong 30 comment đều đã được kiểm lại với `coding.csv`, `extraction.csv` và danh sách bài đã quét, và
đều đúng. File này gồm:

1. Các quyết định sau review.
2. Pilot: là gì, vì sao thêm, làm thế nào, kết quả ra sao, nối với các phần khác thế nào.
3. Những chỗ chưa chuẩn khác mà nhóm tự phát hiện, ngoài 30 comment.
4. Prose sửa cho từng mục của paper.
5. Prose của mục Pilot mới.
6. Hai chỗ chưa theo đề xuất, và những gì để sang bản EASE.
7. File sẽ đổi. Cuối file là câu hỏi cho Hà Cao.

Prose viết sẵn bằng LaTeX để dán vào Overleaf; khi áp, phần mới sẽ được bọc `\new{}` như các lần trước. Số trong
ngoặc (comment 5) là số thứ tự comment.

## 1. Quyết định

**Bảng 1, bốn oracle dựa trên test** (comment 5, 22): phân theo một trục duy nhất là *kết quả mong đợi lấy từ đâu*.
O-c: bộ test có sẵn trước nghiên cứu; O-d: test của chương trình gốc, dịch cùng code; O-e: LLM hoặc đặc tả, không
từ việc chạy chương trình gốc; O-f: chính nghiên cứu chạy chương trình gốc trên cùng đầu vào.

**Legacy** (comment 4, 15, 24): theo công nghệ nguồn (COBOL, PL/I, mainframe, ASP.NET WebForms); không tính C hay
API lỗi thời dù bài tự gọi là legacy; kèm câu độ nhạy.

**Quy tắc mã hoá ở 4.5** (comment 7, 10, 11): chỉ mã oracle có báo kết quả; O-b khi có tỉ lệ biên dịch hoặc kiểm
cú pháp; kiểm tra chỉ áp lên test đã dịch không tính; di trú test thì chạy test đã di trú là O-d; vai trò LLM mã
theo việc LLM làm.

**Mã hoá lại 6 bài:**

| Bài | Hiện tại | Sửa thành |
| --- | --- | --- |
| TRAVEL | O-b, O-c, O-e (e:R) | O-b, O-c, O-f (f:L) |
| PtrTrans | O-b, O-e, O-f | O-b, O-f (f:F) |
| ReCodeAgent | 8 oracle | O-b, O-c, O-d, O-f (thêm f:L) |
| MBTA | O-c, O-f | O-b, O-c, O-f |
| VIM-PT, Semi-supervised | no LLM | baseline only |

**Số liệu sau khi sửa:** O-a 13 (27%), O-b 34 (69%), O-c 28 (57%), O-d 7, O-e 2 (4%), O-f 14 (29%), O-g 2,
O-h 2 (4%), O-i 17 (35%). Báo độ đồng thuận giữa người chấm: 3/17. Nhiều oracle nhất: RustAssure (5). Không đổi:
9 bài không chạy code, 33 bài nhiều oracle trên cùng output, Hình 3.

## 2. Pilot

Phần này để Hà Cao xem cách làm có ổn không và có nên đưa vào report không.

### 2.1 Là gì

Một công cụ nhỏ chấm **cùng một bộ bản dịch** bằng bốn oracle, và một lần chạy thử (pilot) trên 164 bài
HumanEval-X: một LLM dịch từng hàm Python sang Java, rồi bản dịch được chấm bằng biên dịch (O-b), test có sẵn của
HumanEval-X (O-c), CodeBLEU so với lời giải chuẩn (O-a) và một LLM khác làm judge (O-h). Test là oracle duy nhất
chạy code nên được lấy làm mốc; mỗi oracle còn lại được so với test.

### 2.2 Vì sao thêm

- **Mapping không so sánh được số liệu giữa các bài.** Hình 3 cho thấy biên dịch cao hơn chạy đúng 3–98 điểm,
  nhưng mỗi bài một model, benchmark, cấu hình (Threats đã ghi). Pilot đặt bốn oracle lên cùng một bộ output, nên
  khác biệt chỉ còn đến từ oracle.
- **Đo trực tiếp các rủi ro mà mapping chỉ ra:** biên dịch thay cho chạy đúng (Hình 3, G5), độ giống mâu thuẫn với
  test (Bảng 8), LLM judge không được kiểm chứng (G4).
- **Bảng điểm của môn:** 40% cho thiết kế và cài đặt ứng dụng, 20% cho đánh giá ứng dụng. Bản chỉ có mapping không
  có ứng dụng nào để chấm hai phần này.
- **Spec ban đầu đã có pilot** (`Project_Spec_v1.md`, mục 5, "Oracle Disagreement"). So với spec, nhóm đổi bốn chỗ:
  dịch Python → Java thay vì Java → Python, để biên dịch có ý nghĩa; thêm O-b; dùng model mở chạy trên Kaggle thay
  vì API; thêm phần tự kiểm công cụ và thử judge trên đáp án biết trước. Mục pilot đặt sau Results của mapping thay
  vì trước, vì cách chọn oracle dựa vào bản đồ.

### 2.3 Làm thế nào

| Bước | Chi tiết |
| --- | --- |
| Dữ liệu | HumanEval-X: 164 bài có cả Python và Java, kèm lời giải chuẩn và test. Tải từ repo CodeGeeX, kiểm mã SHA-256 |
| Dịch | Qwen2.5-Coder 7B, mỗi bài một lần, nhiệt độ 0, seed cố định. Model thấy hàm Python (bỏ docstring, để nó dịch code chứ không giải lại bài) và chữ ký Java của HumanEval-X (để trượt test là do hành vi, không do sai tên hàm) |
| O-b | `javac` biên dịch riêng bản dịch |
| O-c | Ghép bản dịch với lớp test `Main` của HumanEval-X, biên dịch và chạy, giới hạn 10 giây |
| O-a | CodeBLEU so với lời giải Java chuẩn, xét ở ngưỡng 0,5 / 0,6 / 0,7 |
| O-h | Llama 3.1 8B (khác họ với model dịch, để không tự chấm bài mình) trả lời YES/NO: bản Java có tương đương hàm Python không |
| Tự kiểm công cụ | 164 lời giải chuẩn phải biên dịch, qua test, CodeBLEU 1,0 (đạt cả 164). 298 bản cố tình sai (đổi một toán tử, ví dụ `<` thành `<=`): 288 biên dịch, test bắt 242 |
| Thử judge trên đáp án biết trước | Judge xem 164 lời giải chuẩn (phải YES) và 142 bản cố tình sai mà test đã bắt (phải NO) |
| Chạy | Kaggle, GPU T4, "Save & Run All", ngày 25/10/2026, 42 phút. Notebook chứa sẵn code và ghi mã SHA-256 của code. Tính lại phân tích từ các file kết quả đã lưu ra đúng y kết quả |

### 2.4 Kết quả

| Oracle | Chấp nhận | Cho qua bản trượt test (trên 32) | Đánh trượt bản qua test (trên 132) |
| --- | --- | --- | --- |
| Biên dịch (O-b) | 89,6% | 15 | 0 |
| Test có sẵn (O-c) | 80,5% | – | – |
| CodeBLEU ≥ 0,5 | 82,3% | 17 | 14 |
| CodeBLEU ≥ 0,6 | 67,1% | 13 | 35 |
| CodeBLEU ≥ 0,7 | 51,8% | 5 | 52 |
| LLM judge (O-h) | 73,8% | 16 | 27 |

- Cùng 164 bản dịch, tỉ lệ "đúng" từ 67,1% (CodeBLEU 0,6) đến 89,6% (biên dịch); ở ngưỡng CodeBLEU 0,7 chỉ còn 51,8%.
  Cả bốn oracle đồng ý trên 88 bài (54%).
- Biên dịch cao hơn qua test 9,1 điểm; 15/32 bản sai vẫn biên dịch được.
- CodeBLEU sai cả hai chiều; trung bình 0,76 với bản qua test, 0,51 với bản trượt.
- Judge trên đáp án biết trước: YES với 97/164 lời giải chuẩn (gạt 41% lời giải đúng), NO với 117/142 bản sai;
  balanced accuracy 70,8%. Có 25 bài judge chê lời giải chuẩn nhưng khen bản dịch của model, dù cả hai đều qua test.
- Ví dụ bài 50: phép `%` trong Java cho kết quả âm còn Python thì không; bản dịch biên dịch được, CodeBLEU 0,98, judge
  nói "xử lý đúng trường hợp quay vòng", nhưng trượt test.
- Ví dụ bài 22: HumanEval-X đặt tên hàm sai chính tả `filterIntergers`, model sửa thành `filterIntegers`, nên test
  không gọi được. Test tính đây là trượt dù logic có thể đúng.

### 2.5 Kết luận rút ra và giới hạn

1. Tỉ lệ thành công phụ thuộc oracle: số liệu giữa các bài dùng oracle khác nhau không so sánh được (ủng hộ checklist).
2. Biên dịch và độ giống là thước đo thay thế kém; ngưỡng CodeBLEU tự nó đã làm kết quả dao động 30 điểm.
3. Một LLM judge nhỏ sai cả hai chiều, kể cả trên đáp án biết trước, nên không thể dùng một mình (liên quan G4 và
   bài công nghiệp dùng judge làm oracle duy nhất).
4. Ngay cả test cũng bỏ sót 16% bản cố tình sai: "qua test" chưa phải là tương đương.

Giới hạn: bài cấp hàm, không phải hệ thống cũ; hai model nhỏ, chạy một lần; HumanEval-X có thể đã nằm trong dữ liệu
huấn luyện. Các con số minh hoạ cơ chế bất đồng, không phải ước lượng cho cả lĩnh vực.

### 2.6 Nối với các phần khác

| Phần | Mapping nói gì | Pilot thêm gì |
| --- | --- | --- |
| RQ1 | Biên dịch, test phổ biến nhất; LLM judge mới từ 2026 | Chọn đúng các oracle đó |
| RQ3, Hình 3 | 18 bài: biên dịch cao hơn chạy đúng 3–98 điểm, cấu hình khác nhau | Cùng output: 9,1 điểm; 15/32 bản sai vẫn biên dịch |
| RQ3, Bảng 8 | Vài bài thấy CodeBLEU và test ngược nhau | CodeBLEU cho qua 13 bản sai, đánh trượt 35 bản đúng |
| G4 | LLM judge hầu như không được kiểm chứng | Judge gạt 41% lời giải đúng, cho qua nửa số bản sai |
| Bảng 9 | "Test yếu" là giới hạn nêu nhiều nhất | Test bỏ sót 16% bản cố tình sai |
| Checklist | Ghi rõ oracle | Thêm ý: kiểm LLM judge trên đáp án biết trước |

Trong paper: thêm RQ5 và đóng góp thứ 5 ở Intro; mục mới "Pilot" giữa Results và Discussion; một câu ở Abstract,
G4, G5, Conclusion; một đoạn ở Threats (prose ở phần 4 và 5).

## 3. Những chỗ chưa chuẩn khác (ngoài 30 comment)

**Trong bản paper hiện tại:**

| Chỗ | Vấn đề | Đề xuất |
| --- | --- | --- |
| Discussion, "For practitioners" | Câu "No legacy paper in our corpus uses existing tests" cũng phụ thuộc định nghĩa legacy, giống comment 24 nhưng chưa được nêu | Thêm "as we define legacy (Section 2)" (prose ở 4.10) |
| Bảng 4 (trường 3) và chú thích Phụ lục | Sau khi mã lại VIM-PT và Semi-supervised, loại "no LLM" không còn bài nào | Giữ trong Bảng 4 cho đầy đủ; bỏ mã "N" khỏi chú thích Phụ lục |
| Ghi chú trích xuất của Rule synthesis | Hai chỗ ghi khác nhau: "36 cases" và "a sample of 72 cases" | Mở lại full text để kiểm, sửa `extraction.csv`. Paper không dùng con số này nên không ảnh hưởng số liệu |
| `protocol.md` trên repo | Còn mã `e:R` và định nghĩa cũ của O-e, O-f | Sửa cùng lượt với Bảng 1 |

**Trong prose mình viết, đã tự sửa trước khi gửi:**

| Chỗ | Viết sai | Đã sửa thành |
| --- | --- | --- |
| Results, gạch đầu dòng LIB | "Only 3 LIB papers judge behavior without running code" (sai: CodePlan cũng không chạy code, nên là 4) | "Trong 9 bài LIB có người chấm, chỉ 3 bài không chạy code" |
| Results, ô trống | "Each cell would hold between 0.1 and 1.3 papers" (ô thấp nhất là 0,08) | "at most 1.3 papers" |
| Abstract, Pilot | "67% đến 90%" mà không nói ngưỡng (ở CodeBLEU 0,7 chỉ còn 52%) | Ghi rõ "CodeBLEU at 0.6"; đoạn kết quả nêu tác động của ngưỡng |

**Về pilot, cần biết khi đọc kết quả:**
- Chạy lại có thể ra vài câu trả lời khác dù nhiệt độ 0 và seed cố định (thử trên máy cloud: 3/4 bản dịch giống
  hệt). Vì vậy mọi con số tính từ các file kết quả đã lưu của lần chạy.
- "Judge thiên về code giống bản Python" là diễn giải từ 25 bài, chưa kiểm chứng riêng; prose viết "seems".
- Bài 22 trượt do lỗi chính tả trong benchmark; theo quy tắc vẫn tính là trượt test, prose nêu rõ.

## 4. Prose sửa theo từng mục

### 4.1 Abstract (comment 1; thêm pilot)

```latex
Large language models (LLMs) are now used to translate code between languages and to migrate it across versions, libraries and frameworks. Whether the migrated code behaves like the original is always decided by some oracle, and the choice of oracle can change the reported result. We present a systematic mapping study of how behavioral equivalence is evaluated in this line of research, covering the main proceedings of ICSE, FSE and ASE from 2024 to 2026, and a pilot that applies four oracles to the same translations. From 4,451 papers we screened 431 candidates and included 51 (49 in the main corpus, 2 on cross-language equivalence detection), each read in full. Compilation (69\%) and existing tests (57\%) dominate, while formal verification, LLM-generated tests and LLM judges (4\% each) are rare; 9 papers use no execution-based oracle at all. Oracle use differs by context: no paper with a legacy source uses existing tests, most library migrations include a human check (9 of 12 papers), and LLM-generated tests and LLM judges appear as final-output oracles only in 2026. Thirty-three papers report two or more oracles on the same outputs; among the 18 that report both a compile rate and a behavioral pass rate, compile rates exceed behavioral pass rates by up to 98 percentage points. Nine papers state no limitation of their own oracle. In the pilot, an LLM translated 164 HumanEval-X tasks from Python to Java; depending on the oracle, 67\% to 90\% of the same translations counted as correct, and an LLM judge accepted half of the translations that fail the tests while rejecting 41\% of correct reference solutions. We contribute a coded map of oracle practice, a catalog of how oracles disagree on the same outputs, a classification of the limitations studies report about their own oracles, six gaps between evaluation practice and real migration, a checklist for reporting oracle provenance, and an open harness that applies several oracles to the same translations.
```

### 4.2 Introduction (comment 2, 3; thêm RQ5)

Cuối đoạn "Papers in our own scope show…", thêm:

```latex
Our own pilot finds the same on a single set of 164 translations: depending on the oracle, 67\% to 90\% of them count as correct (Section~\ref{sec:pilot}).
```

RQ2 thay bằng, và thêm RQ5 sau RQ4:

```latex
\item[\textbf{RQ2.}] Where do these oracles come from, and how does their use differ by context: legacy or not, kind of migration, track and year?
\item[\textbf{RQ5.}] On the same LLM translations, how often do compilation, similarity and an LLM judge disagree with the tests?
```

Câu đóng góp thay bằng:

```latex
Our contributions are: (1) a coded map of 49 primary studies by oracle, oracle origin, migration kind and track, with the empty cells that mark under-studied combinations; (2) a catalog of the 33 studies that report two or more oracles on the same outputs, showing how far those oracles disagree; (3) a classification of the limitations that studies report about their own oracles; (4) six gaps between evaluation practice and real migration, with a checklist for reporting oracle provenance; and (5) an open harness that judges the same LLM translations with four oracles, with a pilot on 164 HumanEval-X tasks. All data, code and coding are released (Section~\ref{sec:conclusion}).
```

Đoạn Structure, câu giữa thay bằng:

```latex
Section~\ref{sec:results} answers RQ1 to RQ3, Section~\ref{sec:pilot} answers RQ5 with the pilot, and Section~\ref{sec:discussion} answers RQ4 and proposes the checklist.
```

### 4.3 Background (comment 4, 5, 22)

Câu legacy cuối đoạn "Kinds of migration" thay bằng:

```latex
A \emph{legacy} flag marks a source written for a language or platform that is no longer in mainstream use, such as COBOL, PL/I, mainframe systems or ASP.NET WebForms. We do not flag C sources or deprecated APIs, even when a paper calls them legacy; Section~\ref{sec:rq2} reports how one result changes if they are flagged.
```

Bảng 1, bốn dòng O-c đến O-f thay bằng:

```latex
O-c & Existing tests & Behavior on a test suite that existed before the study, built for a benchmark or by the project's developers & Only as strong as the tests; benchmarks often have few \\
O-d & Translated tests & Behavior on the original program's own tests, translated along with the code & Test and code may share the same translation error \\
O-e & LLM-generated tests & Behavior on new tests whose expected outputs come from an LLM or a specification & Expected outputs can be wrong or aligned with the output \\
O-f & Differential testing & Same outputs as the original, which the study runs on the same inputs (from fuzzing, existing tests or an LLM) & Limited by input generation; needs the original to run \\
```

Sau đoạn "The categories are not exclusive…", thêm:

```latex
The four test-based categories (O-c to O-f) are told apart by where the expected outputs come from: a test suite that existed before the study (O-c), the original program's tests translated with the code (O-d), an LLM or a specification (O-e), or a run of the original program during the study (O-f). Tests that an LLM writes but whose expected outputs come from running the original are therefore differential testing (O-f); the source of the inputs is recorded as the origin of the oracle.
```

### 4.4 Related Work (comment 6)

```latex
our map shows how rarely that advantage is used (14 of 49 papers use the original program as a differential oracle; Figure~\ref{fig:oracle-freq}).
```

### 4.5 Method, mục 4.5 (comment 7, 10, 11)

Sau câu "…is not counted.", thêm:

```latex
Five rules settle boundary cases. We code an oracle only if the paper reports its result on the evaluated outputs, so a compile step implied by passing tests is not counted unless its rate is reported. A compilation or syntax check counts as O-b when the paper reports its rate. Checks applied only to translated tests, not to the translated code, are not oracles of the translation. When the output is itself a migrated test, running it on the target counts as O-d. The role of the LLM is coded by what the LLM does in the study, whatever kind of technique is proposed.
```

### 4.6 Results, 5.1 (comment 9, 10)

Câu đầu thay bằng:

```latex
The corpus grows quickly: 8 papers are from 2024, 14 from 2025 and 27 from 2026, or 0.68\%, 0.98\% and 1.45\% of the papers scanned in each year (Table~\ref{tab:search}). The 2024 share may be slightly low, since 61 ICSE~2024 papers had no abstract and were matched on their titles only.
```

Câu vai trò LLM thay bằng:

```latex
The LLM is the proposed technique in 32 papers, the evaluated subject in 9, and both in 4; in the remaining 4 it is only a baseline (3, two of which propose a smaller neural model) or part of the evaluation tooling (1).
```

### 4.7 Results, 5.2 RQ1 (comment 11, 12, 13)

Hình 2, dòng `\addplot` thay bằng (thứ tự cột: O-b, O-c, O-i, O-f, O-a, O-d, O-e, O-h, O-g; sửa cả `symbolic y coords` và `yticklabels` theo thứ tự này):

```latex
\addplot[fill=blue!55!black, draw=none] coordinates {(34,ob) [34 (69\%)] (28,oc) [28 (57\%)] (17,oi) [17 (35\%)] (14,of) [14 (29\%)] (13,oa) [13 (27\%)] (7,od) [7 (14\%)] (2,oe) [2 (4\%)] (2,oh) [2 (4\%)] (2,og) [2 (4\%)]};
```

Đoạn sau Hình 2 thay bằng:

```latex
Most papers combine oracles: 9 use one, 17 use two, 17 use three, and 6 use four or more, up to five in RustAssure~\cite{rustassure}. We count the oracles whose results a paper reports; 7 of the 28 papers with existing tests report no compile rate, although their code must compile to run. Nine papers use no oracle that executes code (none of O-c to O-f): they judge outputs by compilation, similarity, a human or an LLM. Five rely on a single oracle that does not run the code: 2 report only BLEU or CodeBLEU~\cite{vimpt,collaboration}, one only an LLM judge~\cite{wca4z}, and 2 only human judgment~\cite{pig,pli}.
```

Đoạn về Bảng 5 thay bằng (bỏ câu trung bình theo track):

```latex
Table~\ref{tab:cooc} shows which oracles are combined. Compilation accompanies most other oracles: 22 of the 28 papers with existing tests also use compilation as an oracle, and so do 12 of the 17 with human evaluation. Differential testing seldom appears next to existing tests (4 of 14 papers), and in 9 of the 14 no test-suite oracle (O-c, O-d, O-e) is used. Both papers with formal verification also run differential tests.
```

Bảng 5, phần thân thay bằng:

```latex
O-a & 13 &    &    &   &   &    &   &   &    \\
O-b & 6  & 34 &    &   &   &    &   &   &    \\
O-c & 7  & 22 & 28 &   &   &    &   &   &    \\
O-d & 0  & 7  & 5  & 7 &   &    &   &   &    \\
O-e & 1  & 1  & 1  & 0 & 2 &    &   &   &    \\
O-f & 1  & 12 & 4  & 3 & 0 & 14 &   &   &    \\
O-g & 0  & 2  & 0  & 1 & 0 & 2  & 2 &   &    \\
O-h & 0  & 1  & 0  & 0 & 0 & 0  & 0 & 2 &    \\
O-i & 4  & 12 & 6  & 3 & 0 & 5  & 1 & 1 & 17 \\
```

### 4.8 Results, 5.3 RQ2 (comment 14–20, 22, 23)

Câu mở đầu thay bằng:

```latex
Oracle use differs by context in this corpus (Table~\ref{tab:context}). Most groups are small, so patterns in groups of five papers or fewer are illustrative only.
```

Bảng 6, phần thân thay bằng:

```latex
Legacy                    & 5  & 0  & 1  & 0  & 0 & 1 & 2  & 0 & 1 & 1  \\
Not legacy                & 44 & 13 & 33 & 28 & 7 & 1 & 12 & 2 & 1 & 16 \\
\midrule
XL                        & 33 & 7  & 22 & 20 & 6 & 2 & 11 & 2 & 1 & 6  \\
LIB                       & 12 & 4  & 9  & 6  & 2 & 0 & 1  & 0 & 1 & 9  \\
VER                       & 3  & 1  & 2  & 1  & 0 & 0 & 1  & 0 & 0 & 1  \\
FW                        & 3  & 1  & 3  & 1  & 0 & 1 & 1  & 0 & 0 & 1  \\
DIA                       & 2  & 1  & 1  & 0  & 0 & 0 & 1  & 0 & 0 & 2  \\
\midrule
Research                  & 28 & 8  & 19 & 15 & 6 & 1 & 8  & 2 & 1 & 13 \\
Industry/SEIP             & 9  & 2  & 7  & 5  & 1 & 1 & 3  & 0 & 1 & 2  \\
NIER, IVR, demo, poster   & 7  & 2  & 4  & 3  & 0 & 0 & 2  & 0 & 0 & 2  \\
Journal-first             & 5  & 1  & 4  & 5  & 0 & 0 & 1  & 0 & 0 & 0  \\
\midrule
2024                      & 8  & 3  & 5  & 5  & 1 & 0 & 2  & 0 & 0 & 1  \\
2025                      & 14 & 3  & 10 & 8  & 3 & 0 & 4  & 2 & 0 & 6  \\
2026                      & 27 & 7  & 19 & 15 & 3 & 2 & 8  & 0 & 2 & 10 \\
```

Danh sách gạch đầu dòng thay bằng:

```latex
\item \textbf{No legacy paper uses existing tests.} Two of the 5 legacy papers run the original system as a differential oracle~\cite{kcobagent,coboljava}, one generates tests with an LLM from an extracted specification~\cite{ipmodern}, one uses an LLM judge~\cite{wca4z}, and one compares the generated Java with the expected code by hand~\cite{pli}. This is the one empty cell that chance does not easily explain: with 28 of the 49 papers using existing tests, about 3 legacy papers would be expected to use them. With five papers, all in the industry/SEIP or NIER tracks, legacy cannot be separated from track, and the result depends on our definition: if the three papers that call their C or Java sources legacy were flagged~\cite{evoc2rust,smartc2rust,codehints}, 2 of 8 legacy papers would use existing tests.
\item \textbf{Library migration often includes a human check.} Nine of the 12 LIB papers include human evaluation, against 6 of 33 XL papers, but only 3 of these nine judge behavior without also running the code~\cite{pig,depupgrade,rulesynth}. Several human checks cover a sample, such as 20\% of the patches that passed the tests~\cite{fruntke}. No LIB paper uses LLM-generated tests or formal verification.
\item \textbf{Both formal-verification papers target Rust} ($n = 2$)~\cite{rustassure,vert}.
\item \textbf{LLM-based final-output oracles appear only in 2026.} The 2 papers with LLM-generated tests and the 2 with LLM judges are all from 2026. Earlier papers use LLM-generated tests inside the technique~\cite{unitrans,collaboration}, and with so few papers the timing may be chance.
\item \textbf{All 5 journal-first papers use existing tests}, and none uses human evaluation.
\item \textbf{Zero cells} mark combinations that no paper uses: legacy with similarity, existing, translated or formal-verification oracles; library migration with LLM-generated tests or formal verification; dialect translation with any test-suite oracle; and short papers with translated tests, generated tests, formal verification or LLM judges. Except for legacy with existing tests, each of these cells would hold at most 1.3 papers if oracle use did not depend on the group, so an empty cell says little on its own.
```

Xoá đoạn cũ để trong comment (`%% Previous paragraph, replaced…`). Đoạn "Where the ground truth comes from" thay bằng:

```latex
\paragraph{Where the ground truth comes from.} Table~\ref{tab:origin} breaks down the four execution-based oracles by the origin of their ground truth. Existing tests split almost evenly: 14 papers use tests built for a benchmark of curated problems or reference translations, 12 use the test suite that a real project's developers wrote, and 2 use both~\cite{dgir,recodeagent}. Among the 14 LIB and VER papers, 7 use existing tests, and 6 of these 7 rerun the client project's own suite after the change~\cite{fruntke,byam,bdupdater,freshbrew}. In translation between languages, benchmark tests are more common: 12 papers, against 6 with project suites and 2 with both.

Translated tests are mostly translated by the system under evaluation (5 of 7). In 4 of these papers a translation error can therefore affect the code and its tests alike; in IntentTester the migrated tests are themselves the output under evaluation~\cite{intenttester}. In 3 papers the authors translated tests by hand, in one of them alongside tests translated by its system~\cite{lostintranslation,rustassure,recodeagent}. Only 2 papers use LLM-generated tests in the sense of Table~\ref{tab:oracles}: one derives them from the same specification it uses to generate the code~\cite{ipmodern}, and one does not say where the expected outputs come from~\cite{transagent}. Differential testing takes its inputs from fuzzing, property-based testing or symbolic execution in 5 papers, reuses existing tests or benchmark data in 3, uses LLM-generated inputs in 3~\cite{prognosticator,travel,recodeagent}, compares curated samples or rendered screens in 2, and does not describe its inputs in 2.
```

Bảng 7, phần O-e và O-f thay bằng (chú thích bảng thêm: "One differential-testing paper has two input origins, so the O-f rows sum to 15."):

```latex
\multicolumn{2}{@{}l}{\textit{O-e LLM-generated tests (2)}} \\
\quad Derived from the specification that also generates the code & 1 \\
\quad Source of expected outputs not stated & 1 \\
\multicolumn{2}{@{}l}{\textit{O-f Differential testing (14)}} \\
\quad Inputs from fuzzing, property-based testing or symbolic execution & 5 \\
\quad Inputs from existing tests or benchmark data & 3 \\
\quad Inputs generated by an LLM & 3 \\
\quad Curated samples or rendered screens & 2 \\
\quad Inputs not described & 2 \\
```

### 4.9 Results, 5.4 RQ3 (comment 12, 27)

```latex
Nine papers state no limitation of their own oracle, including 4 of the 5 that rely on a single oracle that does not run the code.
```

Trong đoạn "Oracles reused inside the technique", câu TRAVEL thay bằng:

```latex
TRAVEL rewards its model with the same kind of check it also evaluates with, comparing outputs with the original program on LLM-generated inputs~\cite{travel},
```

### 4.10 Discussion (comment 24–28)

```latex
\item \textbf{Legacy settings are rare.} Only 5 of the 49 papers migrate a legacy system as we define it (Section~\ref{sec:background}), all in the industry/SEIP and NIER tracks, and none of them uses existing tests. Two run the original system as a differential oracle; the other 3 use generated tests, an LLM judge or a person (Section~\ref{sec:rq2}).
```

```latex
\item \textbf{Judgment-based oracles go unvalidated.} Human evaluation appears in 17 papers, but only 3 report agreement between raters~\cite{pylibmig,translibeval,fruntke}. LLM judges appear in 2 papers, and one industrial paper relies on an LLM judge alone~\cite{wca4z}. Our pilot shows why this matters: a small LLM judge rejected 41\% of correct reference solutions and accepted half of the translations that fail the tests (Section~\ref{sec:pilot}).
\item \textbf{Compile rates are reported next to much lower behavioral rates.} Thirty-four papers use compilation as an oracle, and all but one also use a behavioral, human or LLM oracle~\cite{codeplan}. Yet in the 18 that report a compile rate and a behavioral pass rate for the same outputs, behavior trails compilation by 3 to 98 percentage points in the configurations shown in Figure~\ref{fig:compile-gap}; in our pilot, 15 of the 32 translations that fail the tests compile.
\item \textbf{Oracle limitations go unstated.} Nine papers state no limitation of their own oracle, including 4 of the 5 that rely on a single oracle that does not run the code.
```

Đoạn "For benchmark builders": "still appears in 14 papers" → "still appears in 13 papers"; câu zero cells thay bằng:

```latex
The zero cells of Table~\ref{tab:context} may point to benchmarks that do not yet exist: legacy migrations with existing or translated test suites, dialect pairs with test suites, and library migrations evaluated with generated tests or formal verification.
```

Đoạn "For practitioners", câu đầu thay bằng:

```latex
No legacy paper in our corpus, as we define legacy (Section~\ref{sec:background}), uses existing tests, and the corpus shows what replaces them:
```

Checklist, mục 6 thay bằng:

```latex
\item For human or LLM judges: who or which model, the protocol, agreement with a ground truth or between raters, and, for an LLM judge, its accuracy on outputs known to be equivalent or not.
```

### 4.11 Threats (comment 29, 30)

Cuối đoạn Construct validity, trước `\TODO`, thêm:

```latex
Three coding choices shape RQ1 and RQ2: the test-based oracles are told apart by where the expected outputs come from (Section~\ref{sec:background}), legacy is defined narrowly by the source technology, and oracle codes record that a paper uses an oracle, not that its conclusions rest on it.
```

Đoạn Reliability, sau câu đầu, thêm:

```latex
Several patterns rest on groups of five papers or fewer (Table~\ref{tab:context}); we report them as observations, not as rules.
```

Thêm đoạn mới cuối mục:

```latex
\paragraph{The pilot.} The pilot uses short function-level tasks that come with tests, far from the legacy systems that motivate this study, and two small open models in a single run. HumanEval-X is public and may be part of the models' training data, and its tests miss 16\% of single-operator mutants, so failing the tests is the best available reference rather than the truth. Greedy decoding with a fixed seed can still give slightly different answers on a rerun, so all numbers are computed from the stored outputs. The pilot therefore shows how oracles can disagree on the same outputs; its rates are not estimates for the field.
```

### 4.12 Conclusion và Data availability

Câu "The gaps to real migration are clear: …" thay đoạn "compilation is reported as if it were evidence" bằng "compile rates are reported next to much lower behavioral rates". Sau câu đó thêm:

```latex
Our pilot shows the same on one set of 164 translations: depending on the oracle, 67\% to 90\% of them count as correct, and an LLM judge errs in both directions even on answers known in advance.
```

Data availability (bản đang in) thêm vào cuối danh sách: "…a script that recomputes every count, and the pilot's harness, translations, oracle verdicts and executed notebook". Link Kaggle điền khi có.

## 5. Mục mới: Pilot (file `sections/06-pilot.tex`, đặt giữa Results và Discussion)

Cần thêm 3 tài liệu vào `refs.bib`: `humanevalx` (Zheng et al., KDD 2023, doi 10.1145/3580305.3599790), `codebleu`
(Ren et al., arXiv:2009.10297), và hai model: `qwencoder` (Hui et al., arXiv:2409.12186), `llama3` (Grattafiori et
al., arXiv:2407.21783).

```latex
\section{Pilot: Four Oracles on the Same Translations}
\label{sec:pilot}

The mapping counts the oracles that papers report, but each paper applies them to different models, benchmarks and configurations, so their numbers cannot be compared directly (Section~\ref{sec:threats}). To see how much the choice of oracle alone changes the result, we built a harness that applies four oracles to one set of LLM translations and ran it as a pilot (RQ5).

\subsection{Design}

\paragraph{Oracles.} We chose the oracles that the map shows to be the most used or the newest: compilation (O-b, 34 papers), existing tests (O-c, 28), surface similarity (O-a, 13), and an LLM judge (O-h), which appears only in 2026 and is rarely validated (G4). The tests are the only one of the four that runs the translation, so we use them as the reference and compare each other oracle with them.

\paragraph{Data and models.} HumanEval-X~\cite{humanevalx} provides the same 164 problems in Python and Java, each with a reference solution and tests in both languages. An LLM translates each Python function into Java once; we translate into Java rather than Python so that compilation is a meaningful check. The translator sees the function without its docstring, so that it translates code rather than solving the problem again from its description, and it is given the Java class and method signature, so that a test failure reflects behavior. The translator is Qwen2.5-Coder 7B~\cite{qwencoder} and the judge Llama~3.1 8B~\cite{llama3}, two open models from different families, both served by Ollama with greedy decoding and a fixed seed.

\paragraph{The harness.} The harness has six components: data loading, model access, the four oracles, the stages of a run, the analysis and a command line. Compilation runs \texttt{javac} on the translation alone. The test oracle compiles the translation together with the HumanEval-X test class and runs it with a 10-second limit. Similarity is CodeBLEU~\cite{codebleu} against the reference Java solution, turned into a verdict at thresholds of 0.5, 0.6 and 0.7. The judge sees the Python function and the translation and answers YES or NO to whether they are functionally equivalent. Every stage stores its results, and all numbers are computed from the stored files.

\paragraph{Checking the harness.} Before trusting the harness we checked it on known answers. All 164 reference solutions compile, pass their tests and score CodeBLEU 1.0 against themselves. Of 298 single-operator mutants of the references (for example \texttt{<} changed to \texttt{<=}), 288 compile and the tests reject 242 (84\%), so the tests miss 16\% of these wrong programs. To check the judge, we also showed it each reference solution, which is equivalent, and one mutant per task that the tests reject, which is not.

\subsection{Results}

The run on a Kaggle T4 GPU took 42 minutes. Table~\ref{tab:pilot} compares each oracle with the tests: 132 translations pass them and 32 fail.

\begin{table}[t]
  \centering
  \caption{The same 164 translations under four oracles, compared with the tests.}
  \label{tab:pilot}
  \small
  \begin{tabular}{@{}lrrr@{}}
    \toprule
    Oracle & Accepts (\%) & Accepts, fails tests & Rejects, passes tests \\
    \midrule
    Compilation (O-b)          & 89.6 & 15 & 0  \\
    Existing tests (O-c)       & 80.5 & -- & -- \\
    CodeBLEU $\geq$ 0.5 (O-a)  & 82.3 & 17 & 14 \\
    CodeBLEU $\geq$ 0.6 (O-a)  & 67.1 & 13 & 35 \\
    CodeBLEU $\geq$ 0.7 (O-a)  & 51.8 & 5  & 52 \\
    LLM judge (O-h)            & 73.8 & 16 & 27 \\
    \bottomrule
  \end{tabular}
\end{table}

\paragraph{The same translations, different success rates.} Depending on the oracle, between 67.1\% (CodeBLEU at 0.6) and 89.6\% (compilation) of the same 164 translations count as correct, and all four oracles agree on only 88 tasks (54\%). Compilation accepts 15 of the 32 translations that fail the tests, so the compile rate exceeds the test pass rate by 9.1 percentage points. CodeBLEU errs in both directions: at a threshold of 0.6 it accepts 13 failing translations and rejects 35 passing ones, and moving the threshold from 0.5 to 0.7 lowers its acceptance rate from 82.3\% to 51.8\%. Its mean is 0.76 for translations that pass and 0.51 for those that fail.

\paragraph{The LLM judge.} The judge accepts 16 of the 32 failing translations and rejects 27 of the 132 passing ones. On known answers it says NO to 117 of the 142 rejected mutants but also to 67 of the 164 reference solutions, a balanced accuracy of 70.8\%. It seems to favor code that mirrors the Python: on 25 tasks it rejects the reference solution but accepts the model's translation, although both pass the tests. Its reasons can be confidently wrong. In task 50 the translation computes \texttt{(ch - 5 - 'a') \% 26}, which can be negative in Java but not in Python; the translation compiles and scores CodeBLEU 0.98, and the judge accepts it because it ``handles wrap-around cases correctly'', yet it fails the tests.

\paragraph{A failure the tests do not explain.} One translation compiles on its own but not with the tests: HumanEval-X names the method \texttt{filterIntergers}, the model corrected the spelling, and the tests can no longer call it. The test oracle counts such interface errors as behavioral failures even when the logic is right.

\paragraph{Answer to RQ5.} On one set of translations, compilation, similarity and an LLM judge disagree with the tests on 76 of 164 tasks. Compilation and similarity overstate correctness, similarity also understates it, and a small LLM judge errs in both directions, even on answers known in advance. A success rate is therefore only meaningful together with the oracle that produced it.
```

## 6. Hai chỗ chưa theo đề xuất

- **BatFix giữ O-c** (comment 5): test của BatFix là test cố định của benchmark TransCoder, giống MBTA, UniTrans,
  CAST, TransAgent (đều O-c). Theo trục mới, test có sẵn luôn là O-c.
- **IntentTester giữ O-d** (comment 7, 21): output là test đã di trú; chạy nó trên thư viện đích, với assertion mang
  từ test gốc sang, là kiểm tra bằng chạy code với cùng điểm yếu như mọi oracle dựa trên test. Đã ghi thành quy tắc
  ở 4.5.

Để sang bản EASE: trường "hệ thống có test không" và "oracle chính" (comment 2, 8), nguồn gốc của O-h và O-i
(comment 23).

## 7. File sẽ đổi

- Branch `main`: `mapping/4_coding/coding.csv`, `mapping/protocol.md`, `mapping/analysis/expected_output.txt`;
  thêm `pilot/` (code và kết quả) nếu nhóm đồng ý đưa pilot vào report.
- Overleaf: mục 0–8, `sections/06-pilot.tex` (mới), `main.tex` (thêm `\input` cho mục pilot), Hình 2, Bảng 1, 5, 6,
  7, Phụ lục, `refs.bib`.
- File xlsx của nhóm.

## Câu hỏi cho Hà Cao

1. Trục "kết quả mong đợi lấy từ đâu" cho Bảng 1 có ổn không?
2. Đồng ý giữ BatFix là O-c và IntentTester là O-d không?
3. Bạn có thể mã hoá độc lập lại các bài ranh giới (TRAVEL, PtrTrans, ReCodeAgent, BatFix, MBTA, IntentTester,
   Rule synthesis, VIM-PT, Semi-supervised, GUIMigrator) theo quy tắc mới không? Kết quả so với bản của nhóm sẽ
   điền vào đoạn calibration còn `\TODO` ở Threats.
4. Cách làm pilot (phần 2) có ổn không, và có nên đưa vào report như phần 5 không?
5. Prose ở phần 4 và 5, và các chỗ ở phần 3, có chỗ nào cần sửa không?
