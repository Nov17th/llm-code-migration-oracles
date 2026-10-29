# Review bản paper 29/10 (`Seminar_2_2910`)

Người review: Claude (dùng bộ academic-research-skills, chế độ reviewer), 30/10/2026.
Đối tượng: bản `Seminar_2_2910` (NeurIPS `main.tex` và EASE `main-ease.tex`, chung `sections/`).

## 1. Tóm tắt

**Số liệu trong bài rất chắc.** Tôi đã tính lại khoảng 150 con số (bảng, hình, text, pilot) từ ba nguồn độc lập:
bảng Phụ lục A, `mapping/` trên GitHub `main` (chạy lại `recompute.py`) và `pilot/results/verdicts.csv`. Tất cả
đều khớp. Tôi **không** tìm thấy con số nào sai trong bài.

Các vấn đề còn lại nằm ở bốn nhóm: (a) độ chặt của phương pháp SMS (độ tin cậy khi sàng và mã hoá, phạm vi, ba bài
bị loại vì paywall); (b) cách chọn số để làm tiêu đề (khoảng 3–98 điểm, khoảng 52–90%); (c) một nhãn oracle dễ gây
hiểu sai (O-e); (d) một lỗi LaTeX làm bản sạch không biên dịch được.

Có 33 comment, đánh số R01 đến R33, chèn thẳng vào LaTeX bằng macro `\cmt{Claude}{...}` của nhóm. Chúng hiện
thành chữ xanh dương trong PDF, đúng vị trí cần sửa. Trong đó có **8 vấn đề lớn** (mục 3) và 25 vấn đề nhỏ hoặc
ghi chú (mục 4). Tôi không sửa câu chữ nào của bài, chỉ thêm comment.

| Mức | Số comment | ID |
| --- | --- | --- |
| Lớn (nên sửa trước khi nộp) | 8 | R01, R04, R08, R10, R13, R15, R21, R30 |
| Nhỏ | 23 | còn lại |
| Ghi chú hoặc tuỳ chọn | 2 | R06, R19 |

## 2. Đã kiểm những gì, bằng cách nào

| Nhóm số liệu | Nguồn kiểm | Kết quả |
| --- | --- | --- |
| Bảng 2, Hình 1, 380 lý do loại, Bảng 4 (36 = 31 + 5) | `scanned_papers.csv`, `candidates.csv`, cộng tay | Khớp |
| 5.1: năm (8/14/27, 0,68/0,98/1,45%), track, kiểu di trú, legacy, vai trò LLM, Rust 13 | Phụ lục, `coding.csv` | Khớp |
| Hình 2, Bảng 6 (45 ô), 9/16/18/6, 9 bài không chạy code, 5 bài một oracle, 23/28, 12/17 | Phụ lục, `recompute.py` | Khớp |
| Bảng 7, 14 → 7 → 6 (LIB/VER), 12/6/2 (XL) | Phụ lục, `coding.csv` | Khớp |
| Bảng 8 (126 ô), kỳ vọng ≈ 3 và 1,3 | Phụ lục, tính lại | Khớp |
| RQ3: 33 = 18 + 6 + 9, 7 bài còn lại, 18 dòng Hình 3 (phân số, khoảng cách, thứ tự), 13/18, 4/5, Bảng 10 (tổng 49), 3/17 | Phụ lục, `figure3_*.csv`, `table8_*.csv` | Khớp |
| Pilot: 20 ô Bảng 11, 76/25/4, 15 = 14 + 1, 13/35, 5/52, CodeBLEU 0,98/0,30/0,51/0,76, judge 117/142, 67/164, 70,8%, mutant 298/288/242/46, khoảng Wilson, Ollama 0.40.11 | `verdicts.csv`, `summary.md`, `run_info.json` | Khớp |
| Discussion G1–G5, cột "In the map" của checklist, Intro (119/123 = 96,7%, 62/119 = 52,1%) | đối chiếu với Results, tính lại | Khớp |
| Trích dẫn và `\ref` | script | 65 key đều có trong `refs.bib`; mọi `\ref` đều có `\label` |
| Biên dịch | MiKTeX, trên bản sao | Cả hai bản biên dịch được (có comment: NeurIPS 30 trang, EASE 20 trang). Đặt `\reviewfalse` thì lỗi (R01) |

Giới hạn của lần kiểm: tôi **không** đọc lại các bài gốc trong corpus (không có PDF), nên các số lấy từ bài gốc
(ví dụ RustRepoTrans 16–31 điểm, K-COBAgent 82/544) chỉ được kiểm về số học và về độ khớp với ghi chú của nhóm.
Đây là một lượt review của một người, sắp theo các tiêu chí review của ARS (phương pháp, nội dung chuyên môn, phản
biện). Tôi chưa chạy hội đồng 5 reviewer đầy đủ của ARS; nếu nhóm muốn, xem mục 7.

## 3. Tám vấn đề lớn

**R01. Bản sạch không biên dịch được** (`macros.tex`). `\hcrev` và `\revtag` chỉ được định nghĩa trong nhánh
`\ifreview`. Đặt `\reviewfalse` thì pdfLaTeX dừng với "Undefined control sequence \hcrev" và không ra PDF (đã thử).
Sửa: thêm `\newcommand{\hcrev}[1]{#1}` và `\newcommand{\revtag}{}` vào nhánh `\else`. Lưu ý thêm: khi tắt đánh dấu,
các ô `\fillin{N}` sẽ in ra chữ "N" như văn bản thường.

**R04. Khoảng 52–90% trong Abstract** dùng CodeBLEU ở ngưỡng 0,7, mà chính pilot không coi đó là ngưỡng chính. Ở
ngưỡng chính 0,6, khoảng là 67–90%. Abstract cũng nói "the judge accepts half…" mà không nói đó là Llama 3.1 8B
lượng tử hoá 4 bit, trong khi Conclusion có nói "a small LLM judge". Đề xuất: "67% to 90% (52% under a stricter
similarity threshold)" và thêm chữ "small".

**R08. Nhãn O-e "LLM-generated tests" không khớp định nghĩa.** O-e được định nghĩa theo nguồn của kết quả mong đợi
(LLM hoặc đặc tả), không theo ai viết test. Test do LLM viết mà kết quả mong đợi lấy từ việc chạy bản gốc thì là
O-f. Ngược lại, test viết tay từ đặc tả thì vẫn là O-e. Người đọc Abstract sẽ hiểu là "test do LLM sinh rất hiếm
(4%)", trong khi còn 3 bài khác chạy input do LLM sinh (O-f, f:L). Nên đổi nhãn theo nguồn kết quả mong đợi, hoặc
nói rõ điều này ở mọi chỗ báo 4%.

**R10. Phạm vi chưa nhất quán.** Workshop có kỷ yếu riêng bị loại "vì tập sự kiện đổi theo năm", nhưng bài chỉ in
trong Companion volume (có cả bài workshop) lại được quét. Theo `scanned_papers.csv`, 206 trong 216 bài chỉ có trên
Crossref là bài Companion, và chúng lệch mạnh theo năm: FSE có 4 bài năm 2024, 74 bài năm 2025, 95 bài năm 2026;
ICSE có 9, 2, 22; ASE không có bài nào. Đây đúng là kiểu không so sánh được giữa các năm mà lý do loại workshop muốn
tránh. Không bài nào trong số này được chọn, nên corpus không đổi, nhưng mẫu số theo năm ở 5.1 thì có đổi. Ngoài
ra, cụm "main proceedings" làm người đọc nghĩ chỉ có research track. Hướng sửa: hoặc loại nhóm Companion-only, hoặc
báo số này và nêu lý do giữ; đổi tên thành "proceedings (main and Companion volumes)".

**R13 + R30. Chưa báo độ tin cậy khi sàng và mã hoá; đoạn Calibration chưa làm mà viết như đã làm.** Bài không nói
ai sàng 431 ứng viên, ai trích xuất 49 bài, có quyết định nào do hai người làm độc lập không, và đồng thuận bao
nhiêu. Đây là mục reviewer SMS gần như chắc chắn hỏi. Bài lại khuyên các nghiên cứu khác báo rater agreement (G2,
checklist mục 3), nên càng dễ bị bắt lỗi. Đoạn Calibration ở Threats viết ở thì quá khứ nhưng còn các ô `\fillin`
và README ghi là chưa làm. Không được nộp nguyên như vậy. Hoặc làm calibration thật rồi báo đồng thuận theo từng
trường và kappa (Cohen hoặc Fleiss) cho các trường phân loại, hoặc thay bằng mô tả trung thực cách đã làm và đưa
"mã hoá bởi một người" vào Threats.

**R15. Ba bài bị loại vì paywall IEEE (E6).** Hai trong ba bài là bài research ASE 2025 về benchmark dịch code bằng
LLM: DLBench (dịch SQL) và Polyglot. Đây đúng là loại bài I2 sinh ra để nhận. Bài thứ ba là bài phát hiện clone
xuyên ngôn ngữ (ICSE 2024, journal-first), có thể thuộc tầng I3. Sửa rất dễ: lấy bản qua thư viện trường, mượn liên
thư viện, arXiv hoặc email tác giả, rồi mã hoá.

**R21. Hình 3 không nêu cách chọn cấu hình, và khoảng "3–98" bị kéo bởi một ablation.** Hình 3 trộn hệ thống chính,
hai baseline (RISE, DepWareTrans), một ablation (DepTrans, thưởng chỉ khi biên dịch) và một giai đoạn trước sửa lỗi
(BatFix). Con số 98 ở Abstract, RQ3 và Conclusion đến từ ablation đó, tức một cấu hình được thiết kế để hỏng. Bản
đầy đủ của DepTrans là 60,7% so với 43,5%, chênh 17 điểm. Reviewer phản biện sẽ gọi đây là chọn số. Đề xuất: nêu
quy tắc chọn cấu hình; báo trung vị khoảng cách (19 điểm trên 18 dòng hiện tại, 17 điểm nếu thay ablation bằng bản
đầy đủ); giữ ablation như một ví dụ cực đoan thay vì làm đầu mút của khoảng.

## 4. Vấn đề nhỏ và ghi chú

| ID | Vị trí | Vấn đề | Gợi ý |
| --- | --- | --- | --- |
| R02 | Abstract | "main proceedings" (xem R10); Abstract dài khoảng 310 từ | Rút gọn cho bản EASE |
| R03 | Abstract | 98 đến từ ablation (xem R21) | Thêm trung vị 19 điểm |
| R05 | Intro, ví dụ DepWareTrans | Cấu hình 38,16% / 9,39% là baseline (STAR, file-by-file), theo chú thích Hình 3 và CSV | Nói rõ là baseline, như ví dụ DepTrans đã nói là ablation |
| R06 | Intro, RQ2 | RQ2 gộp hai câu hỏi (nguồn ground truth; khác biệt theo ngữ cảnh) | Tuỳ chọn: tách hoặc thêm một câu lý do |
| R07 | Background, ví dụ FW | Ví dụ lấy từ GUIMigrator; đích SwiftUI đổi cả ngôn ngữ (Swift/iOS). Sheet trích xuất có ghi "FW/XL could be considered" nhưng bài mã FW, còn IP-preserving mã FW/XL | Thống nhất quy tắc; ví dụ FW dùng đích Jetpack Compose |
| R09 | Related Work, FreshBrew | "exposes reward hacking" mơ hồ | "guards against reward hacking" |
| R11 | 4.2, recall | 40 bài biết trước không độc lập với chuỗi tìm kiếm, nên 97,5% là lạc quan | Thêm snowballing từ 49 bài làm phép kiểm recall độc lập |
| R12 | 4.3 | Tiêu đề và RQ1 nói "LLM-based", nhưng I1 nhận mọi mô hình neural; 3 bài chỉ dùng LLM làm baseline, 1 bài chỉ dùng làm công cụ đánh giá | Một câu giải thích, hoặc chỉnh chữ |
| R14 | 4.3, lý do loại | Ba lý do ("neither…", "related topic…", "same-language…") đều là "không đạt I1–I3" nhưng không định nghĩa khác nhau (dữ liệu dùng ¬I1¬I2, ¬I1, I3-instr). L-TASK (16) có dòng riêng, còn L-ARCH, L-DECOMP, L-BASE (12) nằm trong 96, L-SUM (3) nằm trong E5 | Định nghĩa hoặc gán mã; xử lý các luật như nhau |
| R16 | Bảng 5 | Trường 2 thiếu Doctoral Symposium và SRC dù có trong phạm vi; trường 7 "một chủ đề chính" không nói chọn thế nào khi bài nêu nhiều hạn chế | Nêu "không có bài nào"; thêm quy tắc chọn |
| R17 | 5.1 | "Rust là đích trong 13 bài" không kiểm được vì Phụ lục không có cột ngôn ngữ đích; NIER, SEIP, PLC chưa viết đầy đủ | Thêm cột hoặc bỏ số; viết đầy đủ lần đầu |
| R18 | 5.3, gạch legacy | "Chance does not easily explain" là khẳng định thống kê, trong khi Reliability nói không kiểm định | Báo xác suất siêu bội ≈ 1,1% kèm cảnh báo nhiều ô được xem, hoặc viết nhẹ đi; "would hold at most 1.3" → "expected count is at most 1.3" |
| R19 | 5.3, gạch 2026 | Ghi chú: 3 bài O-f có input do LLM sinh cũng đều năm 2026 | Thêm để củng cố nhận định |
| R20 | 5.4 | CAST và MBTA được mã O-b, O-c và nằm trong 33 bài, nhưng không có trong Hình 3 | Nêu lý do trong một mệnh đề, hoặc thêm vào hình |
| R22 | 5.4, độ giống | "Ít nhất một cặp đảo thứ hạng" là tiêu chí yếu. TerraMod chỉ đảo ở 1/4 model; UniTrans đảo giữa LLM và baseline không phải LLM; CAST đảo nhiều cặp | Báo số cặp đảo trên số cặp so, hoặc tương quan hạng |
| R23 | 5.4, MBTA | MTS tính trên bản dịch của mutant, tức output khác; nó đo độ bền của translator chứ không phải phán quyết thứ hai trên cùng output, nên mâu thuẫn với chú thích Bảng 9 và việc đếm vào 33. Câu "168 programs" dễ hiểu là đúng 168 chương trình đạt CA = 1 (thật ra CA = 1 ở 29,62% chương trình; 168 trong số đó có mutant dịch sai, 147 ở chiều còn lại). CA được dùng trước khi định nghĩa | Đưa MBTA ra khỏi nhóm "cùng output" hoặc giải thích; viết lại câu |
| R24 | Bảng 9 | Fruntke & Krinke: mẫu zero-shot là 10/48 bản vá qua test, trong khi cấu hình zero-shot ở Hình 3 chỉ có 12 bản qua test. Code hints: "Symbolic engine" khiến người đọc nghĩ output không do LLM | Nêu 48 bản gồm model hoặc slice nào; nói LLM làm gì |
| R25 | Bảng 11 | Judge có Accepts = Agrees = 73,8%. Đúng là trùng hợp (nhận đúng 16/32 bản trượt) nhưng trông như lỗi chép | Thêm chú thích chân trang |
| R26 | 6.2 | 76, 25 và 4 là ở ngưỡng 0,6 (ở 0,5: 64, 27, 5; ở 0,7: 86, 23, 2) | Nêu ngưỡng |
| R27 | G4 | Một phần G4 dựa trên quan sát "gặp đâu ghi đó"; `coding.csv` đã có cột oracle dùng lại trong kỹ thuật (5 bài) | Mã cột này cho cả 49 bài |
| R28 | Directions | Mỗi hướng là một đoạn vài trăm từ; bản EASE hiện 18 trang (giới hạn 10). "Ít nhất 18 bài phân loại lỗi" và "năm bài…" không thuộc trường nào trong form | Rút gọn; đánh dấu là quan sát chưa mã hoá |
| R29 | Checklist | Mục 2 "18 of 35" chỉ đếm bài trong Hình 3, nên chỉ là cận dưới. "40 papers with test-based oracles" (mục 4) khác tập với "40 papers that combine oracles" (5.2, 5.4) | Định nghĩa rõ; gọi tên tập mỗi lần dùng |
| R31 | Threats | README cho thấy có dùng Claude để soạn bản thảo và script. Chính sách tác giả của ACM yêu cầu công bố việc dùng AI tạo sinh | Thêm câu công bố; nói việc mã hoá có LLM hỗ trợ (nếu có) được kiểm thế nào |
| R32 | Threats, External | Thiếu các tạp chí (TSE, TOSEM, EMSE); chúng chỉ được tính khi trình bày dạng journal-first | Nêu là giới hạn |
| R33 | Conclusion | "These findings hold for three venues" dễ hiểu là "đã được xác nhận ở" | "are limited to" |

## 5. Ngoài nội dung bài

- **Bản clone local `mapping/` (nhánh `latex`) đã cũ.** Chạy `recompute.py` ở đó ra O-a 14, O-b 33, O-e 5, O-h 3,
  O-i 18, khác bài. Bản trên GitHub `main` (commit `00cbc22`) thì khớp hoàn toàn. Khi tạo release cho Data
  availability, cần lấy từ `main`.
- **Độ dài:** bản NeurIPS 28 trang (README ghi 19); bản EASE 18 trang trong khi giới hạn là 10 (đo trước khi chèn
  comment).
- **README đã cũ:** còn ghi "6 khoảng trống", "62 tài liệu" (nay `refs.bib` có 70 mục, 65 mục được trích), 19 trang.
- 5 mục trong `refs.bib` không được trích (`copilotmig`, `diggs`, `manyshot`, `oracleescape`, `syzygy`). BibTeX tự
  bỏ qua, nhưng nên dọn.

## 6. Thứ tự sửa đề xuất

1. R01 (một dòng LaTeX), R15 (lấy 3 bài), R30 và R13 (quyết định làm calibration hay viết lại).
2. R21, R04, R03, R33: các con số tiêu đề ở Abstract, RQ3 và Conclusion.
3. R10, R14, R16: mô tả phương pháp.
4. R08, R07: phân loại.
5. Các mục nhỏ còn lại.

## 7. Cách dùng comment

- Mọi comment có dạng `\cmt{Claude}{[Rxx] ...}`. Tìm `\cmt{Claude}` để duyệt hoặc xoá từng cái sau khi xử lý.
- Sau khi sửa R01, đặt `\reviewfalse` sẽ ẩn toàn bộ comment cùng các đánh dấu khác.
- Comment trong PDF viết bằng tiếng Anh vì pdfLaTeX với `T1` không in được dấu tiếng Việt; báo cáo này là bản tiếng
  Việt đầy đủ.
- Bản gốc trước khi chèn comment là commit trước commit review này trên nhánh `latex`; có thể dùng `git diff` để
  xem đúng những dòng đã thêm.
- Nếu nhóm muốn có thêm một lượt review theo hội đồng 5 reviewer của ARS (phương pháp, chuyên môn, liên ngành,
  phản biện, biên tập; có thư quyết định và lộ trình sửa), hãy yêu cầu riêng. Bước đầu tiên của lượt đó là để nhóm
  xác nhận cấu hình các reviewer.
