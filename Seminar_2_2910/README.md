# Paper LaTeX: Behavioral Equivalence in LLM Code Translation (SMS)

Bản LaTeX của paper, chuyển từ Claude Doc "Paper draft (EN)" rồi bổ sung ngày 25/10/2026. Số liệu khớp
file `Kiem_tra_3_tab_ICSE_FSE_ASE.xlsx` bản 25/10/2026 (sheet "Mã hoá tổng hợp" có thêm hai cột: "Nguồn gốc
oracle thực thi" và "Nhiều oracle trên cùng output: nhóm"; track của 3 bài Companion đã sửa theo trang hội nghị).

## Hai bản, một nội dung

| File chính | Template | Dùng để | Số trang hiện tại |
| --- | --- | --- | --- |
| `main.tex` | NeurIPS 2025 (`neurips_2025.sty`, tuỳ chọn `preprint`), một cột | Nộp môn | 19 |
| `main-ease.tex` | ACM `sigconf` (`acmart`), hai cột | Nộp EASE 2027 (Hà Nội), sau khi cắt về 10 trang | 12 |

Cả hai đọc chung `sections/`, `figures/`, `refs.bib`. **Sửa nội dung một lần, biên dịch file nào cũng được.**
Chỉ phần tác giả và kiểu trích dẫn khác nhau (NeurIPS dùng `plainnat`, ACM dùng `ACM-Reference-Format`).

**Số dòng bên lề đã tắt ở cả hai bản** vì đây là bản nộp môn. Muốn bật lại cho một vòng góp ý nội bộ: bỏ
comment hai dòng `lineno` trong `main.tex`; với `main-ease.tex` thêm tuỳ chọn `review` (khi nộp EASE thì bắt buộc có).

Bản NeurIPS đã xoá dòng chú thích "Preprint." ở chân trang 1, vì đây là bài môn học chứ không phải bài
NeurIPS. Đừng bật tuỳ chọn `final`: nó in "NeurIPS 2025" ở chân trang.

## Cách biên dịch

- **Overleaf:** New Project → Upload Project → chọn file zip. Overleaf tự chọn `main.tex`; muốn biên dịch
  bản EASE thì Menu → Main document → `main-ease.tex`. Compiler pdfLaTeX.
- **Máy cá nhân:** TeX Live đầy đủ. `latexmk -pdf main.tex` hoặc `latexmk -pdf main-ease.tex`.

## Cấu trúc

| File | Nội dung |
| --- | --- |
| `main.tex`, `main-ease.tex` | Khung paper: template, 5 tác giả, thứ tự các mục |
| `macros.tex` | Gói và macro dùng chung, gồm macro ghi chú khi sửa |
| `neurips_2025.sty` | Style NeurIPS 2025, tải từ trang NeurIPS, không sửa |
| `sections/00-abstract.tex` | Abstract |
| `sections/01-introduction.tex` | 1 Introduction, RQ1–RQ4, đóng góp, cấu trúc bài |
| `sections/02-background.tex` | 2 Background: kiểu di trú, định nghĩa tương đương hành vi, Bảng 1 (9 nhóm oracle) |
| `sections/03-related-work.tex` | 3 Related Work |
| `sections/04-method.tex` | 4 Method: phạm vi, keyword, bảng số theo hội nghị, sơ đồ chọn bài, tiêu chí, full text, form trích xuất |
| `sections/05-results.tex` | 5 Results: RQ1 (kèm bảng kết hợp oracle), RQ2 (kèm bảng nguồn gốc oracle), RQ3 |
| `sections/06-discussion.tex` | 6 Discussion: 6.1 trả lời RQ4 (6 khoảng trống), 6.2 hàm ý, 6.3 checklist |
| `sections/07-threats.tex` | 7 Threats: construct, internal, external, reliability |
| `sections/08-conclusion.tex` | 8 Conclusion và Data availability |
| `sections/09-appendix.tex` | Phụ lục: 51 bài kèm toàn bộ mã hoá. **File sinh tự động**, xem dưới |
| `figures/selection-flow.tex` | Hình 1: sơ đồ chọn bài kiểu PRISMA (TikZ) |
| `figures/oracle-freq.tex` | Hình 2: tần suất oracle (pgfplots) |
| `figures/compile-gap.tex` | Hình 3: tỉ lệ biên dịch so với tỉ lệ chạy đúng ở 18 bài |
| `refs.bib` | 62 tài liệu tham khảo, lấy từ Crossref và DataCite |

## Quy ước khi sửa

1. **Mỗi người sửa file của mình.** Chia việc theo bảng dưới. Muốn góp ý file của người khác thì dùng
   macro ghi chú, không sửa thẳng.
2. **Macro ghi chú** (trong `macros.tex`):
   - `\cmt{Tên}{nội dung}`: góp ý, màu xanh dương.
   - `\new{...}` và `\begin{added}...\end{added}`: phần mới thêm, màu xanh ngọc. Bảng hoặc hình mới
     có chữ **[new]** ở đầu caption (`\addedtag`). Đọc xong, đồng ý thì cứ để; macro tự biến mất khi xuất bản sạch.
   - `\TODO{...}`: chỗ còn thiếu, màu đỏ.
   - `\fillin{...}`: ô nhóm phải điền (con số, tên, link), nền cam.
   - Đổi `\reviewtrue` thành `\reviewfalse` trong `macros.tex` để ẩn mọi đánh dấu (màu, [new], TODO).
3. **Con số.** Mọi con số lấy từ file xlsx. Sửa một con số thì sửa ở xlsx trước, rồi mọi chỗ trong
   paper dùng số đó (abstract, Results, Discussion, Conclusion, hình). Dùng Ctrl+F để tìm hết.
4. **Trích dẫn.** `\cite{key}`; key nằm trong `refs.bib`. Bài trong corpus có key là tên ngắn viết
   thường, ví dụ `\cite{alphatrans}`, `\cite{dgir}`.
5. **Hình.** Số liệu của hình nằm ngay trong `figures/*.tex`. Sửa số thì sửa ở đó.
6. **Phụ lục** sinh bằng `make_appendix.py` từ dữ liệu mã hoá; sửa tay sẽ bị đè ở lần sinh lại.

## Đoạn viết sẵn dạng comment (bỏ dấu % là thành prose dùng được)

| Ở đâu | Nội dung | Điều kiện để bỏ comment |
| --- | --- | --- |
| `07-threats.tex`, ngay sau `\TODO` | Đoạn **Calibration**: 5 tác giả cùng mã hoá 5 bài, báo số giá trị khớp | Sau khi làm bước 4 của kế hoạch; điền các ô `\fillin` |
| `04-method.tex`, cuối mục Selection | Sàng độc lập hai người trên mọi ứng viên | Nếu nhóm làm bước 3 (sàng cặp); điền số ca lệch |
| `08-conclusion.tex`, cuối file | Data availability, hai bản: A (công khai trên GitHub) và B (không công khai, gửi khi được hỏi); Acknowledgments | Chọn một bản. A: khi repo đã có release; B: nếu nhóm không công khai dữ liệu |

Bỏ comment xong thì xoá `\TODO` tương ứng.

## Chia việc đọc và sửa

Điền tên vào hai cột cuối. Người đọc chéo không phải người sửa chính.

| Phần | File | Cần kiểm gì | Sửa chính | Đọc chéo |
| --- | --- | --- | --- | --- |
| Abstract, Introduction | `00`, `01` | Ba ví dụ mở bài đúng số; RQ4 mới | | |
| Background, Related Work | `02`, `03` | Đoạn định nghĩa tương đương (mới); Bảng 1; bốn công trình gần nhất | | |
| Method | `04`, `figures/selection-flow.tex` | Bảng số theo hội nghị, sơ đồ chọn bài (mới); 4.451 / 430 / 431 / 51; đoạn full text đã sửa 10 → 18 | | |
| Results RQ1, RQ2 | `05` (5.1–5.3), `figures/oracle-freq.tex` | Bảng kết hợp oracle, bảng nguồn gốc oracle (mới): đối chiếu cột mới trong xlsx | | |
| Results RQ3 | `05` (5.4), `figures/compile-gap.tex` | Từng số bất đồng; đoạn "oracle dùng lại trong kỹ thuật" (mới) | | |
| Discussion | `06` | 6.1 RQ4: sáu khoảng trống G1–G6 (mới), mỗi số đối chiếu Results | | |
| Threats, Conclusion | `07`, `08` | Điền calibration; chọn bản Data availability | | |
| Tài liệu tham khảo, phụ lục | `refs.bib`, `09` | Tên venue thống nhất; mã từng bài trong phụ lục | | |

## Việc còn mở

- Tên, đơn vị, email của 5 tác giả trong **cả hai** file `main.tex` và `main-ease.tex`.
- Calibration 5 bài (đoạn viết sẵn ở Threats).
- Data availability: chọn bản A (link GitHub) hoặc bản B (không công khai) ở cuối `08-conclusion.tex`.
- Repo GitHub `llm-code-migration-oracles`: đã có nội dung, chưa license, chưa release. Các bước còn lại ghi ở `claude/Repo_Release_Checklist.md` trong Project.
- `refs.bib`: tên hội nghị lấy nguyên từ Crossref nên chưa thống nhất.
- Bản EASE: cắt về 10 trang khi nộp (phụ lục và một số bảng có thể chuyển sang replication package).

## Script sinh dữ liệu (nằm ngoài zip, trong thư mục làm việc của Claude)

- `make_bib.py`: sinh `refs.bib` từ Crossref/DataCite.
- `make_appendix.py`: sinh `sections/09-appendix.tex` từ dữ liệu mã hoá (cùng nguồn với sheet "Mã hoá tổng hợp").
