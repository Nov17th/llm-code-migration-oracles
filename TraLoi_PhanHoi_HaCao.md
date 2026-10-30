# Trả lời phản hồi review RQ1 + RQ2 (Hà Cao)

Mình đã đọc kỹ `PhanHoi_Review_HaCao.md` và kiểm lại toàn bộ. Cảm ơn bạn, phản hồi rất cẩn thận. File này gồm:

1. Kết quả kiểm số liệu.
2. Những quyết định mình đồng ý.
3. Những chỗ cần sửa trước khi áp vào Overleaf (V1–V7).
4. Ba lỗi trong phần pilot (P1–P3) và hai lưu ý.
5. Trả lời 5 câu hỏi của bạn.
6. Việc tiếp theo.

Đánh số V và P để không nhầm với G1–G6 trong paper. Số comment trong ngoặc dùng đúng cách đánh số của bạn.

## 1. Kết quả kiểm số liệu

Mình áp đúng 6 thay đổi mã hoá bạn đề xuất lên `coding.csv` (chỉ trong bộ nhớ, không sửa file) rồi tính lại mọi con số
trong phản hồi. **Tất cả đều khớp:**

- Hình 2: O-a 13, O-b 34, O-c 28, O-d 7, O-e 2, O-f 14, O-g 2, O-h 2, O-i 17.
- Số oracle mỗi bài: 9 / 17 / 17 / 6. Nhiều nhất là RustAssure (5).
- Bảng 5, Bảng 6 (từng ô) và Bảng 7 (O-f cộng lại thành 15).
- 3/17 bài báo độ đồng thuận; chỉ CodePlan dùng compile mà không có oracle nào khác ngoài độ giống.
- 6/33 bài XL có người chấm; 3/9 bài LIB không chạy code.
- 4 of 14 và 9 of 14 ở đoạn O-f; ô 0 có kỳ vọng tối đa 1,33; khoảng 3 bài legacy kỳ vọng.

Phần pilot: mọi con số trong bảng kết quả đều nhất quán với nhau. Ví dụ ở CodeBLEU 0,6, (132 − 35) + 13 = 110, và
110/164 = 67,1%; balanced accuracy = (97/164 + 117/142)/2 = 70,8%; 76 = 164 − 88. Mình không kiểm được số liệu gốc
vì thư mục `pilot/` chưa có trên repo (xem lưu ý ở mục 4).

## 2. Những quyết định mình đồng ý

| Quyết định | Vì sao đồng ý (theo `extraction.csv`) |
| --- | --- |
| Trục "kết quả mong đợi lấy từ đâu" cho Bảng 1 | Gỡ được chỗ chồng nhau giữa O-e và O-f; TRAVEL, PtrTrans và ReCodeAgent xếp được rõ ràng |
| TRAVEL đổi O-e thành O-f (f:L); PtrTrans chỉ còn O-f (f:F) | Cả hai đều chạy chương trình C gốc để lấy kết quả mong đợi |
| ReCodeAgent còn O-b, O-c, O-d, O-f | O-a, O-h, O-i đều chấm *test đã dịch* ("analysis on the quality of the translated tests", rồi "re-checked by 2 humans") |
| MBTA thêm O-b | Có báo 91,11% compile |
| VIM-PT, Semi-supervised đổi thành "baseline only" | Nhất quán với GUIMigrator |
| **BatFix giữ O-c** | Test cố định của benchmark TransCoder; MBTA, UniTrans, CAST, TransAgent dùng cùng benchmark và đều mã O-c. Theo trục mới, O-f là khi *chính nghiên cứu* chạy chương trình gốc |
| Legacy theo công nghệ nguồn, kèm câu độ nhạy | Đúng như comment 4, 15, 24 đề xuất |
| Viết lại RQ2 thành "legacy or not, kind of migration, track and year" | Giải quyết comment 2 gọn hơn việc thêm trường mới |
| Hoãn trường "test availability" và "primary oracle" sang bản EASE | Chấp nhận được, vì prose đã đổi "relies on" thành "includes" và Threats đã có câu "record that a paper uses an oracle, not that its conclusions rest on it" |
| Các chỗ bạn tự phát hiện ở mục 3 | Đồng ý cả, nhất là câu "as we define legacy" ở đoạn "For practitioners" |

**Tổng kết theo comment:**
- Giải quyết đầy đủ: 23/30 comment.
- Đã sửa nhưng còn sót chi tiết: 3 comment (1, 5, 11).
- Mới sửa một phần: 2 comment (7, 21).
- Hoãn sang EASE: 2 comment (8, 23).

## 3. Cần sửa trước khi áp

### V1. Số bị cũ sau khi mã lại MBTA (comment 11)

Mục 4.7 viết "7 of the 28 papers with existing tests report no compile rate". Sau khi MBTA được thêm O-b, con số đúng
là **6**: Bảng 5 mới có O-b × O-c = 22, và 28 − 22 = 6.

```latex
We count the oracles whose results a paper reports; 6 of the 28 papers with existing tests report no compile rate, although their code must compile to run.
```

### V2. Quy tắc O-b mới vẫn áp chưa đều (comment 7)

Quy tắc ở 4.5 ghi "chỉ mã oracle có báo kết quả; O-b khi có tỉ lệ biên dịch hoặc kiểm cú pháp". Nhưng:

- **RustRepoTrans** vẫn mã O-b, dù `extraction.csv` ghi: "the compile-pass rate is not reported separately". Bài chỉ
  có phân rã các bản trượt test: 92,3% lỗi biên dịch.
- **TransGraph** vẫn mã O-b, dù số liệu "appear only in the figure".
- **CAST** có đúng kiểu phân rã đó (Compile Error/Runtime Error ở RQ8) lại *không* mã O-b.
- **Rule synthesis** đếm lỗi cú pháp vào Failures nhưng chưa được xếp theo quy tắc mới.

Nhóm cần chọn một trong hai phương án. Mình đã tính sẵn tác động:

| Phương án | O-b | Thay đổi kéo theo |
| --- | --- | --- |
| A. Giữ quy tắc như đã viết: bỏ O-b ở RustRepoTrans và TransGraph | 32 (65%) | O-b × O-c: 20; O-c không có O-b: 8; số bài dùng một oracle tăng từ 9 lên 11 (phân bố 11 / 15 / 17 / 6); dòng XL, Research, Short, 2024, 2025 trong Bảng 6 đổi |
| B. Sửa quy tắc thành "rate *hoặc phân rã lỗi theo giai đoạn*": thêm O-b cho CAST | 35 (71%) | O-b × O-c: 23; O-c không có O-b: 5; phân bố 9 / 16 / 18 / 6; dòng XL, Journal-first, 2026 trong Bảng 6 đổi |

Ở cả hai phương án: G5 ("all but one … CodePlan") vẫn đúng, "9 bài không chạy code" và "5 bài chỉ một oracle không chạy
code" không đổi. Con số 69% trong abstract thì đổi. Rule synthesis cần mở full text để xếp theo phương án đã chọn.

### V3. TransAgent không xếp được theo trục mới (comment 5)

O-e giờ được định nghĩa bằng nguồn của kết quả mong đợi, nhưng TransAgent (e:U) "does not say where the expected outputs
come from". Đề xuất thêm vào cuối đoạn mới ở Background:

```latex
When a paper does not say where the expected outputs of LLM-written tests come from, we code them as O-e.
```

### V4. Quy tắc IntentTester mâu thuẫn với Bảng 1 (comment 21)

Định nghĩa O-d mới là "the original program's own tests, translated *along with the code*". IntentTester không dịch code
nào kèm theo; output của bài chính là test đã di trú. Quy tắc ở 4.5 đúng, nhưng Bảng 1 cần nói theo. Đề xuất dòng O-d:

```latex
O-d & Translated tests & Behavior on the original program's own tests, translated along with the code, or, in test migration, the migrated tests themselves & Test and code may share the same translation error; a migrated test that passes may no longer check what the original did \\
```

Và trong đoạn "Translated tests are mostly translated by the system…" ở RQ2:

```latex
in IntentTester the migrated tests are themselves the output under evaluation, so a pass shows that a migrated test passes on the target library, not that it still checks what the original test checked~\cite{intenttester}.
```

### V5. Abstract nhấn mạnh hơn mức Results cho phép (comment 1)

Abstract vẫn nêu thành phát hiện: "LLM-generated tests and LLM judges appear as final-output oracles only in 2026". Trong
khi đó Results ghi "with so few papers the timing may be chance". Đúng vậy: chỉ có 4 bài, và xác suất cả 4 rơi vào 2026
do ngẫu nhiên là khoảng 0,08. Đề xuất **bỏ vế này khỏi abstract**. Nếu muốn giữ thì viết:

```latex
and the four papers with LLM-based final-output oracles are all from 2026
```

### V6. Phần mô tả `\Description` của Hình 2 còn số cũ

Mục 4.7 chỉ nói sửa `\addplot`, `symbolic y coords` và `yticklabels`. Phần `\Description` của Hình 2 trong
`05-results.tex` vẫn ghi 33, 18, 14, 13, 5, 3. Cần sửa thành (nếu chọn phương án V2 nào thì đổi số O-b theo):

```latex
\Description{Horizontal bar chart. Compilation 34 papers (69\%), existing tests 28 (57\%), human evaluation 17 (35\%), differential testing 14 (29\%), surface similarity 13 (27\%), translated tests 7 (14\%), LLM-generated tests 2 (4\%), LLM judge 2 (4\%), formal verification 2 (4\%).}
```

### V7. Phạm vi của "where do oracles come from" (comment 23)

Hoãn phần nguồn gốc của O-h và O-i sang bản EASE thì được. Nhưng RQ2 mới vẫn hỏi "Where do these oracles come from" cho
mọi oracle, trong khi Bảng 7 chỉ có 4 oracle chạy code. Cần thêm một câu giới hạn phạm vi, ví dụ vào chú thích Bảng 7:

```latex
Origin is coded only for the four execution-based oracles; the origin of references, specifications and judgments is left to future work.
```

## 4. Pilot

Thiết kế hợp lý và khớp với `Project_Spec_v1.md` §5. Mình đồng ý đưa pilot vào bản nộp môn, sau khi sửa ba lỗi sau.

### P1. Khoảng "67% to 90%" chọn ngưỡng có lợi

Bảng tự sửa của bạn (mục 3) ghi đã thêm "CodeBLEU at 0.6", nhưng prose ở **Abstract (4.1), Intro (4.2) và Conclusion
(4.12) vẫn chưa ghi ngưỡng**. Ở ngưỡng 0,7, tỉ lệ chỉ còn 51,8%, nên 67% không phải đầu dưới của khoảng. Đề xuất dùng cả
khoảng thật ở cả ba chỗ:

```latex
depending on the oracle, 52\% to 90\% of the same translations counted as correct
```

Còn câu trong mục Pilot thì viết:

```latex
Depending on the oracle, between 51.8\% (CodeBLEU at 0.7) and 89.6\% (compilation) of the same 164 translations count as correct
```

### P2. "Test bỏ sót 16% bản cố tình sai" là nói quá

Mutant đổi một toán tử có thể là *equivalent mutant*: ví dụ `<` thành `<=` mà dấu bằng không bao giờ xảy ra. Khi đó bản
"sai" thực ra vẫn chạy đúng. Vì vậy 16% chỉ là **cận trên** của số bản sai mà test bỏ sót. Lỗi này kéo theo:

- đoạn "Checking the harness":

```latex
Of 298 single-operator mutants of the references (for example \texttt{<} changed to \texttt{<=}), 288 compile and the tests reject 242 (84\%). The other 46 survive the tests; some may be equivalent mutants that behave like the reference, so 16\% is an upper bound on the wrong programs that the tests miss.
```

- đoạn Threats của pilot. Câu "so *failing* the tests is the best available reference" cũng ngược logic: mutant sống sót
  làm yếu kết luận "passing", còn task 22 làm yếu kết luận "failing". Đề xuất:

```latex
Up to 16\% of single-operator mutants survive its tests, and one task fails because of a misspelled method name in the benchmark, so the tests are the best available reference rather than the truth.
```

- kết luận 4 ở mục 2.5 và dòng "Bảng 9" ở mục 2.6: đổi thành "test để sót tối đa 16% mutant".

### P3. "All four oracles agree on 88 tasks" chưa nói dùng ngưỡng CodeBLEU nào

Câu này và câu "disagree with the tests on 76 of 164 tasks" ở phần Answer to RQ5 cần ghi rõ ngưỡng, ví dụ
"(CodeBLEU at 0.6)". Nếu dùng ngưỡng khác thì cả hai số đều đổi.

### Hai lưu ý

- **Commit `pilot/` trước khi đưa vào report**, gồm code, các file kết quả đã lưu và script tính lại số, giống phần
  mapping. Hiện mình chỉ kiểm được tính nhất quán số học, chưa kiểm được số gốc.
- **Bản EASE (giới hạn 10 trang):** spec ghi pilot phải "cắt được". Đưa RQ5 vào cả Abstract, Intro, Discussion và
  Conclusion thì khi cần cắt sẽ phải sửa ở nhiều chỗ. Đề xuất gom các câu về pilot ở những phần đó thành vài câu dễ bỏ,
  hoặc để pilot thành phụ lục trong bản EASE.

## 5. Trả lời 5 câu hỏi của bạn

1. **Trục "kết quả mong đợi lấy từ đâu":** ổn. Thêm quy tắc mặc định ở V3.
2. **BatFix giữ O-c:** đồng ý. **IntentTester giữ O-d:** đồng ý, với điều kiện sửa Bảng 1 và prose như V4.
3. **Mã hoá độc lập các bài ranh giới:** được. Người mã cần làm **mà không xem trước** mã của nhóm, thì kết quả mới
   dùng được làm calibration. Đề xuất thêm RustRepoTrans, TransGraph, CAST và Lost in Translation vào danh sách để chốt luôn V2.
4. **Pilot:** cách làm ổn; nên đưa vào bản nộp môn sau khi sửa P1–P3. Với bản EASE, giữ pilot ở dạng cắt được.
5. **Prose ở phần 4 và 5:** cần sửa V1, V4, V5, V6, V7 và P1–P3. Phần còn lại mình đồng ý.

## 6. Việc tiếp theo

- [ ] Nhóm chọn phương án A hoặc B cho quy tắc O-b (V2), rồi cập nhật xlsx và `coding.csv`.
- [ ] Mã hoá độc lập các bài ranh giới (câu hỏi 3), rồi dùng kết quả để điền đoạn calibration ở Threats.
- [ ] Áp prose của bạn kèm các sửa V1–V7 và P1–P3; chạy lại `recompute.py`, cập nhật `expected_output.txt` và sinh lại
      Phụ lục bằng `make_appendix.py`.
- [ ] Commit `pilot/` (code, kết quả, script tính lại).
- [ ] Sửa `protocol.md` cho Bảng 1 mới (bỏ `e:R`, thêm quy tắc ở 4.5 và V3).

Ngoài lề: commit `c11ed74` có đưa cả file build LaTeX (`main.aux`, `main.pdf`, `main.log`…) lên repo. Nên xoá
chúng khỏi repo và thêm `.gitignore` cho các file này.
