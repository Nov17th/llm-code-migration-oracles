# Review bản paper 30/10 (`Seminar_2_3010`)

Người review: Claude, dùng bộ academic-research-skills (hội đồng 5 reviewer + deep research), 30/10/2026.
Đối tượng: bản `Seminar_2_3010` (NeurIPS `main.tex` và EASE `main-ease.tex`, chung `sections/`).
Bản trước: review 29/10 (`Review_Claude_Seminar_2_2910.md`, comment R01–R33).

## 1. Tóm tắt và quyết định

**Quyết định của hội đồng: Major revision.** Cả 5 reviewer đều đề xuất Major revision. Devil's Advocate không có
vấn đề CRITICAL nào. Vấn đề Critical duy nhất là độ dài bản EASE (18 trang, giới hạn 10), tức là lỗi hình thức chứ
không phải lỗi nội dung.

Phần map (RQ1–RQ3) vững. Số liệu khớp nhau: Reviewer 1 cộng lại toàn bộ sơ đồ chọn bài, Bảng 2, 4, 10, các số từ
Phụ lục và các cột của Bảng 11, không thấy chỗ nào lệch. Trục "nguồn gốc ground truth" của test (O-c đến O-f) được cả
hội đồng coi là đóng góp mới thật. Các vấn đề còn lại nằm ở năm chỗ:

1. **Độ tin cậy của chính bài:** không nói ai sàng, ai mã hoá, cũng không báo độ đồng thuận. Đoạn Calibration đã bị
   xoá nhưng không có gì thay vào, trong khi bài lại chê các nghiên cứu gốc vì chỉ 3/17 bài báo độ đồng thuận.
2. **Cách chọn con số tiêu đề:** ba ví dụ mở bài lấy từ một baseline và một ablation; khoảng 52–90% có cả hai đầu
   yếu; "13 of 18" phụ thuộc vào cách chọn cấu hình mà bài không nêu quy tắc.
3. **"Needs of real migration projects" (RQ5):** chỉ dựa trên một tiền đề tự đặt, không có dữ liệu thực tiễn.
4. **Định nghĩa quyết định kết luận ở Abstract:** nhãn O-e, cờ legacy không tính C, cách đếm "chạy bản gốc" (G5),
   và G1 bị đếm quá tay.
5. **Pilot:** lấy chính bộ test yếu làm mốc so, chưa kiểm tay các ca lệch, và không dùng differential testing với
   bản Python gốc, dù đó chính là oracle bài khuyến nghị (G5).

Đã chèn **77 comment màu hồng** (P01–P77) thẳng vào LaTeX. Có 1 Critical (riêng cho EASE), 34 Major và 42 Minor.
Nhiều comment Major cùng nói một vấn đề ở các vị trí khác nhau (Abstract, Results, Discussion, Conclusion), nên
mục 4 gom chúng thành 10 nhóm.

**Nếu chỉ nộp môn (bản NeurIPS):** giới hạn trang không còn là vấn đề. Nên ưu tiên các nhóm A, B, C, D của mục 4.

## 2. Đã làm gì, và giới hạn của lần review này

| Bước | Nội dung |
| --- | --- |
| Phase 0 | Phân tích lĩnh vực và 4 thẻ cấu hình reviewer; nhóm đã xác nhận ("ok") trước khi hội đồng chạy |
| Deep research 1 | Kiểm 65 trích dẫn (60 DOI đối chiếu Crossref, PolyHuman đối chiếu DataCite), khoảng 30 dòng venue và track trong Phụ lục, các nhận định ở Related Work, Intro và Pilot |
| Deep research 2 | Quét Crossref với 31 truy vấn trên các tập kỷ yếu ICSE, FSE, ASE 2024–2026 (644 bài, 643 có trong `scanned_papers.csv`); tìm bài bị sót; tìm tài liệu liên quan còn thiếu |
| Phase 1 | 5 reviewer chạy song song, mỗi người là một subagent riêng và không đọc báo cáo của người khác: Journal-Fit (EIC), Phương pháp (R1), Chuyên môn (R2, có dùng kết quả deep research), Thực tiễn và liên ngành (R3), Devil's Advocate (DA) |
| Phase 2 | Tổng hợp: gộp trùng, phân xử chỗ bất đồng, ra quyết định và lộ trình sửa (báo cáo này) |
| Biên dịch | Có comment: NeurIPS 36 trang, EASE 23 trang, không lỗi. Trên bản sao, thêm hai dòng sửa R01 rồi đặt `\reviewfalse`: 28 và 18 trang, comment ẩn hết |

Giới hạn, nói thẳng:

- **Các reviewer không độc lập thật sự.** Cả 5 là cùng một họ model (Claude), chỉ khác vai và khác ngữ cảnh. Chỗ
  nhiều reviewer cùng nêu nên đọc là "nhiều góc nhìn cùng thấy", không phải bằng chứng độc lập.
- **Chưa chạy đủ quy trình ARS.** Tôi không chạy bước paper-blind của sprint contract, các script kiểm
  (`check_phase_conformance`, `check_panel_synthesis`, provenance), cũng không chạy ba phần đính kèm tự động
  (acronym, kiểm tài liệu gợi ý, kiểm nhận định của reviewer). Trạng thái hiệu chuẩn: `NOT_CALIBRATED`.
- **Không đọc lại toàn bộ bài gốc trong corpus.** Ba nhận định của R2 lấy từ bản arXiv mà R2 tự đọc. Chúng đi ngược
  ghi chú "đã kiểm với bài gốc" của nhóm, nên **nhóm cần tự kiểm lại** (xem mục 6).
- Báo cáo chi tiết của từng reviewer chỉ nằm trong thư mục tạm của phiên làm việc (`scratchpad/seat_*.md`). Báo cáo
  này đã chép lại mọi điểm cần dùng.

## 3. Bản 30/10 đã xử lý 33 comment cũ đến đâu

| Trạng thái | Comment cũ | Comment mới tương ứng |
| --- | --- | --- |
| Đã sửa | R32 (journal), R33; Abstract bỏ khoảng "3–98" | — |
| Sửa một phần | R11, R18, R21, R23, R29 | P33, P44, P08/P46, P49, P58 |
| Chưa sửa | R01, R02, R04, R05, R07, R08, R09, R10, R12, R14, R15, R16, R17, R20, R22, R24, R25, R26, R27, R28, R31 | P01, P04, P10/P11, P14, P20, P05/P23, P29, P31, P34, P37, P38, P42, P43, P46, P47, P48/P50, P55, P54, P62, P65, P71 |
| Nặng hơn | R13/R30: đoạn Calibration bị xoá nhưng không có gì thay vào | P35, P71 |
| Tuỳ chọn, giữ nguyên | R06, R19 | — |

R20 (CAST và MBTA không có trong Hình 3) gộp vào P46 và P58: CAST có báo CA trên cùng output mà không nằm trong 18 bài.

## 4. Mười nhóm vấn đề lớn và lộ trình sửa

Thứ tự là thứ tự đề xuất sửa. "Tối thiểu" là cách sửa đủ để qua review; "mạnh hơn" là cách sửa tốt hơn nếu còn thời gian.

**A. Sẵn sàng để nộp (P01, P02, P13, P76).**
- **R01 vẫn còn:** đặt `\reviewfalse` thì khoảng 100 lỗi "Undefined control sequence". Sửa bằng hai dòng trong nhánh
  `\else` của `macros.tex`: `\newcommand{\hcrev}[1]{#1}` và `\newcommand{\revtag}{}`. Đã thử trên bản sao.
- Khối tác giả ở cả hai bản vẫn là placeholder. Tag release vẫn là ô `\fillin`. README ghi repo chưa có license, chưa
  có release.
- **Riêng EASE:** 18/10 trang (P02 có kế hoạch cắt theo từng mục). Chưa ẩn danh: Acknowledgments nêu tên môn học và
  giảng viên, URL GitHub chứa tên tài khoản cá nhân. Thiếu ACM CCS concepts.

**B. Độ tin cậy của khâu sàng và mã hoá (P35, P71). Đây là lý do dễ bị Major revision nhất ở EASE.**
- **Tối thiểu:**
  - Ghi rõ ai làm bước nào, bao nhiêu người trên mỗi bài, xử lý bất đồng thế nào.
  - Lấy một mẫu calibration: người thứ hai mã hoá mù 10–15 bài ở các trường 4, 5, 7, và sàng lại một mẫu ngẫu nhiên
    các bài bị loại ở vòng tiêu đề và tóm tắt.
  - Báo Cohen's kappa theo từng trường. Với mã hiếm (O-e, O-g, O-h) báo thêm raw agreement hoặc PABAK.
  - Nếu không làm được thì viết trung thực là một người mã hoá và đưa vào Threats.
- Kèm R31: nếu có dùng LLM hỗ trợ sàng, trích xuất hoặc viết thì phải công bố, theo chính sách ACM.

**C. Cách đóng khung RQ5: "needs of real migration projects" (P12, P57, P75, P17).** Bốn reviewer cùng nêu.
- **Tối thiểu:** đổi cách viết ở Abstract, RQ5, đóng góp (5), mục 6 và Conclusion, ví dụ "gaps between how
  published studies evaluate migrations and the evidence that behavioral equivalence requires".
- Nêu tiền đề một cách tường minh, có nguồn (IEEE 1012, hoặc bằng chứng nghiệm thu mà 9 bài industry đã báo).
- Tách hai mục đích: so sánh kỹ thuật cần benchmark chung; nghiệm thu một migration cần bằng chứng cho đúng hệ thống
  đó. Nói rõ G1–G5 áp vào mục đích nào.
- Thêm một threat: các gap đo so với chuẩn tự suy ra, không phải lấy từ người làm thực tế.
- Dữ liệu của chính bài có chỗ đi ngược khung này: Google không chạy bản gốc; bài industry dùng differential
  testing ngang bài research (3/9 so với 8/28).

**D. Con số tiêu đề lấy ở cực trị (P14, P15, P08/P46, P10/P74, P11).**
- **Intro:** 38,16%/9,39% là của baseline (STAR, file-by-file). Theo R2, chính DepWareTrans báo 100% biên dịch và
  100% qua test. 97,9%/0% là ablation chỉ thưởng biên dịch, được dựng ra để minh hoạ reward hacking. Nên dùng cấu hình
  chính (ví dụ VERT 94,7% so với 51,9%, hoặc DepTrans bản đầy đủ 60,7% so với 43,5%) và thêm một ví dụ không lồng
  nhau từ Bảng 9 (TerraMod).
- **Hình 3:** cần một quy tắc chọn cấu hình nêu trước. Báo trung vị và IQR (trung vị hiện là 19 điểm). Cho khoảng
  có và không có ablation. Giải thích ngưỡng 10 điểm, vì nhiều dòng nằm sát ngưỡng: TerraMod 8, RISE 8,
  ReCodeAgent 13.
- **52–90%:** ở ngưỡng chính là 67–90%, còn mốc test là 80%. Ghi rõ "a 7B translator, một lần chạy". Judge thì ghi
  "a small (8B, 4-bit) judge".

**E. Mốc so của pilot và độ chính xác của judge (P51, P56, P60, P54, P53).**
- Test của HumanEval-X để lọt 16% mutant, nhưng Bảng 11 lại coi phán quyết của test là sự thật.
- **Tối thiểu:** đổi tên cột "False accept/False reject"; kiểm tay 67 lời giải tham chiếu bị judge bác (hoặc một mẫu,
  hai người chấm); thêm kappa vào Bảng 11. Kappa so với test: biên dịch 0,65; CodeBLEU 0,38, 0,26 và 0,29 ở ba
  ngưỡng; judge 0,26. Như vậy judge không hơn CodeBLEU ở 0,6.
- **Mạnh hơn:** chạy bản Python gốc và bản Java trên tập input lớn (input của EvalPlus/HumanEval+), rồi lấy "qua test
  và khớp bản gốc" làm mốc so.
- G2 đổi "The pilot measures it" thành "estimates its agreement with benchmark labels for one small judge".

**F. Các định nghĩa quyết định kết luận ở Abstract (P05/P23, P07/P21, P06/P63, P58).**
- **O-e:** nhãn "LLM-generated tests" không khớp định nghĩa. Có thêm 3 bài O-f chạy input do LLM sinh. TransAgent có
  thể phải mã lại (xem mục 6). Nên đổi nhãn và báo con số "LLM viết test hoặc input" (O-e cộng f:L).
- **Legacy không tính C:** lệch với tài liệu SE (Khadka et al., ICSE 2014) và với cách chính các bài C sang Rust tự
  mô tả. Nên đổi tên cờ (ví dụ "obsolete-platform source"), hoặc mã theo cách bài tự mô tả và báo cả hai.
- **G5 "29% chạy bản gốc":** suite của dự án đã chạy qua trên bản cũ thì cũng là regression oracle so với bản gốc.
  Nên tách hai nhóm: kết quả mong đợi lập trên bản gốc, và kết quả mong đợi lấy từ bản tham chiếu đích hoặc test dịch.
- **G1:** 33/35 bài có biên dịch đã chạy code (chỉ CodePlan và DepUpgrade là không; tôi đã kiểm trên Phụ lục). 18 bài
  ở Hình 3 được chọn chính vì đã làm đúng điều G1 khuyến nghị. Nên viết lại G1 theo đúng nhóm bài mà nó áp vào, và
  tính lại baseline của checklist mục 2.

**G. Độ đầy đủ của corpus (P33, P38, P39, P45, P30, P31, P32).** Deep research tìm được:
- **DLBench** (ASE 2025, benchmark dịch SQL bằng LLM) có bản miễn phí của tác giả tại
  `matafeiyanll.github.io/paper/ASE25.pdf`, nên lý do E6 không còn đúng. Nhận được ngay (I2, DIA). Polyglot thì xin
  qua thư viện hoặc email tác giả.
- **Bài Google ở FSE 2025 Industry (C185)** bị loại vì "no named source→target pair", nhưng int32 sang int64 là một
  cặp có tên, và `googlemig` (đã nhận) cũng nói về chính migration này.
- **Galápagos** (FSE 2026 JF, C232) bị loại theo L-TASK ở vòng tóm tắt, nhưng bài so test với kiểm chứng hình thức
  trên bản dịch C sang Go do LLM sinh (207/300 qua test, 73/300 được chứng minh tương đương).
- **DependaFix** (FSE 2026 demo) là bài thứ hai bị chuỗi tìm kiếm bỏ sót trong mảng sửa dependency.
- C317 bị loại E5 nghiêng về một bản ở MSR, mà MSR nằm ngoài phạm vi.
- Ngoài ra: ISSTA bị loại ở 2024 và 2026 mà không có lý do; workshop trong Companion volume; 80 bài chỉ khớp theo
  tiêu đề trong khi tóm tắt có sẵn trên ACM/IEEE.

**H. Độ đúng của việc mã hoá (P42, P62, P48, P49, P65/P72).**
- "One main theme per paper" chưa có quy tắc chọn và đếm thiếu mọi theme phụ. Nên mã nhiều theme.
- G4 dựa trên quan sát "gặp đâu ghi đó". Nên thêm một trường mã cho cả 49 bài: oracle báo cáo có được dùng trong kỹ
  thuật không, và dùng thế nào (chọn, sửa, huấn luyện, điểm dừng).
- **Code hints:** theo R2, số ở Bảng 9 là của engine ký hiệu (RefSym). Với engine LLM, người review chỉ bác 1–2
  ứng viên mỗi cấu hình.
- **MBTA:** không phải "cùng output", và không dùng LLM (role phải là N).
- Các số đếm từ đọc toàn văn (18 bài phân loại lỗi, 5 bài…) chưa phải trường mã hoá, nên câu "recomputes every count"
  chưa đúng.

**I. Định vị so với tài liệu đã có (P19, P26, P24, P25, P28, P61).**
- Mỗi gap đều đã có người nói riêng lẻ: Rozière et al. 2020 và Evtikhiev et al. 2023 (G1); EvalPlus (G3); FLOURINE,
  Zhang et al. PLDI 2025, Syzygy, LLMLift (G5); How2Bench (checklist); Wang et al. ISSTA 2025 (LLM judge);
  Molina et al. TOSEM 2025 (oracle thời LLM).
- **Quan trọng nhất:** `refs.bib` có Khanna 2026, "Passing Parity Is Not Preserving Behaviour: Oracle Escape in
  Function-Level LLM Code Migration" (workshop AISM). Tên bài nói đúng luận điểm của bài mình nhưng **chưa được
  trích**. Cần trích và nêu khác biệt.

**J. Hướng dẫn cho người làm thực tế (P66, P67, P22, P68, P69).**
- **Khuyến nghị đang giả định đội đã có test.** Hệ legacy thì thường không có. Cần nêu thêm characterization (golden
  master), record/replay, parallel run, shadow traffic và canary/rollback. Tất cả đều là biến thể của O-f. Kèm các ràng
  buộc: cô lập side effect, chuẩn hoá output, bảo vệ dữ liệu, chi phí.
- **Checklist chưa có "equivalence relation".** Mục 1 cần thêm miền input, cách so sánh và dung sai, và các sai khác
  có chủ đích.
- **Định nghĩa tương đương hành vi cần bổ sung:** chuỗi input (hệ có trạng thái), tính không tất định, và các tính
  chất phi chức năng.

## 5. Chỗ các reviewer bất đồng và cách phân xử

| Vấn đề | Ý kiến | Phân xử |
| --- | --- | --- |
| Đưa "17/35 bài báo biên dịch mà không có tỷ lệ hành vi" lên Abstract (EIC, câu hỏi 4) | DA-03: 33/35 bài có biên dịch đã chạy code; "18 of 35" ở checklist chỉ đếm bài vừa với Hình 3 | **Theo DA** (đã kiểm trên Phụ lục). Không đưa con số 17/35 lên Abstract; xem P58 |
| Mức độ của vấn đề cờ legacy | R2: Major ("kết luận đảo ngược nếu dùng định nghĩa của lĩnh vực"); EIC: Minor ("thêm điều kiện") | **Major**, vì đây là một câu ở Abstract và phụ thuộc vào định nghĩa. Cách sửa tối thiểu là thêm điều kiện hoặc đổi tên cờ |
| Bài quá dài | EIC: Critical cho EASE; các reviewer khác không chấm điểm này | Critical chỉ cho bản EASE; không ảnh hưởng bản nộp môn |
| Câu "chance does not easily explain" | R1 tính P = 0,011 (bỏ qua việc so nhiều ô) và khoảng 0,08 trên cả 126 ô; DA và R2 nêu cách giải thích đơn giản hơn | Đồng thuận: bỏ câu này, hoặc báo xác suất post hoc kèm các cảnh báo (P44) |
| Kết quả mutation 84% bị diệt | R1, G3: bằng chứng test yếu; DA-13: cũng có thể đọc là test khá mạnh | Trình bày cả hai cách đọc; phân loại 46 mutant sống sót xem cái nào tương đương (P53) |

Devil's Advocate không nêu vấn đề CRITICAL nào, nên không có mục nào chặn quyết định Accept theo quy tắc của ARS.

## 6. Cần nhóm tự kiểm với bài gốc

Ba nhận định dưới đây là của R2, dựa trên bản arXiv mà R2 tự đọc. Chúng đi ngược ghi chú "đã kiểm" trong source,
nên nhóm cần mở bài gốc kiểm lại trước khi sửa:

1. **DepWareTrans (P14):** theo abstract arXiv 2608.14128, hệ thống đạt 100% biên dịch và 100% qua test, còn
   38,16%/9,39% là của baseline file-by-file. Chú thích Hình 3 của nhóm cũng ghi đó là baseline; chỉ có Intro là
   chưa ghi.
2. **Code hints (P48):** theo arXiv 2412.08041v4, Bảng 1, các dòng "112 vs 104" và "23 vs 7" là của RefSym (không dùng
   LLM). RefNeural (Claude 2.1 và 3) có số khác: không có hint, 14 qua fuzzing thì 12 đạt khi review; có hint, khoảng
   94 thì 93.
3. **TransAgent (P23):** phần dựng benchmark trong arXiv 2409.19894 nói dùng gpt-4o-mini để sinh test input, rồi chạy
   các lời giải do người viết để lấy kết quả. Nếu đúng vậy thì bài thuộc O-c hoặc O-f, không phải O-e.

Các phát hiện của deep research về corpus (DLBench, C185, Galápagos, DependaFix, C317) có kèm DOI hoặc URL trong
comment. Nhóm nên đọc toàn văn trước khi đổi quyết định nhận hay loại.

## 7. Kết quả kiểm chứng trích dẫn

- **Không có trích dẫn sai.** Cả 65 tài liệu đều tồn tại; 60 DOI khớp Crossref ở tên bài, họ tác giả, năm và trang.
  Khoảng 30 dòng venue và track trong Phụ lục đều đúng. PolyHuman đúng là ở ESEM 2026, in trong LIPIcs tập 394.
  Ollama 0.40.11 phát hành ngày 24/10. `filterIntergers` (HumanEval/22) là lỗi chính tả có sẵn trong benchmark.
- **Cần sửa câu chữ:**
  - Jiao et al.: "few unit tests" quá tay; bài gốc nói khoảng một nửa số cặp có test (P27).
  - CodeBLEU 0.7.0 là phiên bản của gói PyPI, không phải của phương pháp (P52).
  - ChangeGuard 7,6% đúng, nhưng nên nói rõ một phần là do thay đổi không có test nào phủ (P16).
- **Sửa `refs.bib` (P77):**
  - mbta là năm 2024; byam thiếu số bài 113.
  - 7 bài FSE Companion có booktitle như kỷ yếu chính.
  - pli và terramod là ICSE-NIER nhưng không ghi.
  - Tên ICSE 2026 có 3 cách viết; trường publisher không thống nhất.
  - syzygy và manyshot (chưa được trích) bị sai tác giả.
- **Chưa kiểm được:** câu "six levels" của Zhang et al., vì MDPI chặn truy cập toàn văn.

## 8. Danh sách 77 comment

Mức: C = Critical (riêng EASE), M = Major, m = Minor. Người nêu: EIC, R1 (phương pháp), R2 (chuyên môn), R3 (thực
tiễn), DA (Devil's Advocate), DR (deep research).

| ID | File | Mức | Người nêu (comment cũ) | Nội dung |
| --- | --- | --- | --- | --- |
| P01 | 00 | M | EIC, DA (R01) | Bản sạch lỗi `\hcrev`; khối tác giả là placeholder |
| P02 | 00 | C | EIC | EASE 18/10 trang; kế hoạch cắt |
| P03 | 00 | m | EIC, R2 | Abstract không nói điểm mới so với các review |
| P04 | 00 | m | R1, DR (R02, R10) | "Main proceedings" thật ra gồm cả Companion, poster, JF |
| P05 | 00 | M | R2, DA, R1 (R08) | 71% biên dịch gần như luôn đi cùng oracle chạy code; 4% O-e đếm thiếu |
| P06 | 00 | M | DA, R2 | "29% chạy bản gốc" bỏ qua regression suite |
| P07 | 00 | M | EIC, R2, R1, DA | Câu legacy phụ thuộc định nghĩa và track |
| P08 | 00 | M | R1, DA, R2, EIC (R21) | "13 of 18" phụ thuộc cách chọn cấu hình và ngưỡng 10 điểm |
| P09 | 00 | m | DA, EIC | 5/10 bài không nêu hạn chế là bài ngắn; bỏ "Yet" |
| P10 | 00 | M | EIC, R1, DA (R04) | 52–90%: cả hai đầu yếu; nên dùng 67–90% và nêu model |
| P11 | 00 | M | DA, R1, R2, EIC (R04) | "Small (8B, 4-bit) judge"; 41% chưa phải là lỗi của judge |
| P12 | 00 | M | DA, R3, EIC, R1 | "Needs of real migration projects" chưa có căn cứ |
| P13 | 00 | M | EIC, R1 | Release chưa có; một số số đếm không tính lại được |
| P14 | 01 | M | R2, DA, EIC (R05) | DepWareTrans: số của baseline |
| P15 | 01 | M | R2, DA, EIC | DepTrans: ablation; cả ba ví dụ đều là oracle lồng nhau |
| P16 | 01 | m | R2, DR | ChangeGuard 7,6%: thêm điều kiện |
| P17 | 01 | m | EIC, R1, DA | Tên bài nên nêu phạm vi 3 hội nghị và pilot |
| P18 | 01 | m | DA | Đóng góp (1) "ô trống" mâu thuẫn với Results |
| P19 | 01 | M | EIC, DA, R2 | Pilot chưa được định vị so với EvalPlus, Out of the BLEU, LLM-judge |
| P20 | 02 | m | R2 (R07) | Ví dụ FW SwiftUI cũng là XL; quy tắc FW, LIB, XL |
| P21 | 02 | M | R2, R3, EIC | Cờ legacy không tính C; nên đổi tên hoặc định nghĩa lại |
| P22 | 02 | m | R3 | Định nghĩa tương đương: chuỗi input, không tất định, phi chức năng |
| P23 | 02 | M | R2 (R08) | Nhãn O-e không khớp định nghĩa; TransAgent |
| P24 | 02 | m | R2, DR | "Rarely validated" chỉ đúng trong map; Wang et al. ISSTA 2025 |
| P25 | 03 | m | R2, DR | Lamothe et al. (API evolution), Hou et al. (LLM4SE) |
| P26 | 03 | M | R2, EIC, DA | Định vị từng gap; Khanna 2026 chưa được trích |
| P27 | 03 | m | DR, R2 | Jiao et al.: "few unit tests" quá tay |
| P28 | 03 | m | R2, R3, DR | Molina et al.; pseudo-oracle, translation validation, EMI |
| P29 | 03 | m | (R09) | "Exposes" thành "guards against"; coverage gắn yếu với khả năng phát hiện lỗi |
| P30 | 04 | M | R1, EIC, DA | Lý do chọn venue; ISSTA 2024, 2026 |
| P31 | 04 | m | R1 (R10) | Workshop trong Companion: lý do loại cũng áp vào chúng |
| P32 | 04 | m | R1 | 80 bài chỉ khớp tiêu đề: lấy tóm tắt từ ACM/IEEE |
| P33 | 04 | M | R1, R2, DR (R11) | Recall không độc lập; DependaFix; chuỗi bổ sung và snowballing |
| P34 | 04 | m | R2 (R12) | "LLM-based" so với "neural"; MBTA là N |
| P35 | 04 | M | R1, EIC (R13, R30) | Không báo ai sàng, ai mã hoá, độ đồng thuận |
| P36 | 04 | m | R1, R2 | Thời điểm ra các luật; ngưỡng của L-TASK |
| P37 | 04 | m | R1 (R14) | Lý do loại không có trong Bảng 3 |
| P38 | 04 | M | R2, R1, DR (R15) | DLBench có bản miễn phí; Polyglot; Rubhus |
| P39 | 04 | m | DR, R2 | C185 Google FSE 2025; C317; C320 |
| P40 | 04 | m | R2, R1 | Quy tắc đếm O-b quá rộng |
| P41 | 04 | m | R2 | Ranh giới O-c/O-d theo thời điểm; thêm trục độc lập |
| P42 | 04 | M | R1 (R16) | "One main theme" chưa có quy tắc chọn, đếm thiếu theme phụ |
| P43 | 05 | m | DR (R17) | Rust 13 không kiểm được; viết đầy đủ NIER, SEIP; nhãn track FSE 2024 |
| P44 | 05 | m | R1, DA, R2 (R18) | "Chance does not easily explain" |
| P45 | 05 | m | R2, DR | Galápagos: kiểm chứng hình thức ngoài Rust |
| P46 | 05 | M | R1, DA, R2, EIC (R21) | Hình 3: quy tắc chọn cấu hình, trung vị, ngưỡng 10 điểm |
| P47 | 05 | m | DA (R22) | "At least one pair" quá dễ đạt |
| P48 | 05 | M | R2 (R24) | Code hints: số của engine không dùng LLM |
| P49 | 05 | m | R2 (R23) | MBTA không phải "cùng output"; câu 168 chương trình |
| P50 | 05 | m | R2 (R24) | Fruntke & Krinke: mẫu 10 không khớp 12/65 |
| P51 | 05a | M | R1, DA, R2 | Mốc so là bộ test yếu; nên thêm differential với bản Python |
| P52 | 05a | m | DR, R2 | CodeBLEU 0.7.0 là phiên bản gói PyPI |
| P53 | 05a | m | R1, DA | Cách sinh và chọn mutant; mutant tương đương |
| P54 | 05a | m | R1 (R26) | Kappa; ngưỡng của 76, 25, 4 |
| P55 | 05a | m | (R25) | 73,8% xuất hiện hai lần: thêm chú thích chân trang |
| P56 | 05a | M | DA, R1 | Kiểm tay 67 lời giải tham chiếu bị judge bác |
| P57 | 06 | M | DA, R3, EIC, R1 | Tiền đề của RQ5; hai mục đích của đánh giá |
| P58 | 06 | M | DA (R29) | G1 bị phóng đại; baseline của checklist mục 2 |
| P59 | 06 | m | DA | WCA4Z có nghiên cứu người dùng xác nhận judge (không có số) |
| P60 | 06 | M | DA, R1 | "The pilot measures it" nói quá |
| P61 | 06 | m | R3, R2 | Người chấm cũng cần kiểm độ chính xác (cài lỗi), không chỉ đồng thuận |
| P62 | 06 | M | R2, DA, EIC (R27) | G4: thêm trường mã "oracle dùng trong kỹ thuật"; contamination |
| P63 | 06 | M | DA, R2 | G5: tách regression suite và benchmark |
| P64 | 06 | m | DA | "What one oracle misses, another may catch" cần dè dặt hơn |
| P65 | 06 | m | R1, EIC, DA (R28) | Số đếm không có trong form trích xuất; Directions quá dài |
| P66 | 06 | M | R3 | Khuyến nghị cho người làm thực tế giả định đã có test |
| P67 | 06 | M | R3 | Checklist thiếu "equivalence relation" |
| P68 | 06 | m | R3, DA, EIC | Checklist: coverage, phiên bản công cụ, định vị, chưa được kiểm chứng, tên gọi |
| P69 | 06 | m | R3 | Rủi ro chưa nối với việc chọn oracle; cột "Requires" |
| P70 | 07 | m | DA, DR | Venue ML/NLP; bài backporting |
| P71 | 07 | M | R1, EIC (R13, R30, R31) | Reliability; công bố việc dùng AI |
| P72 | 07 | m | R1, EIC | "Recomputes every count" nói quá |
| P73 | 07 | m | R1 | So khoảng tin cậy biên cho dữ liệu ghép cặp là sai cách |
| P74 | 08 | M | EIC, R1, DA | 52–90% (như P10) |
| P75 | 08 | m | EIC, DA | Thống nhất cách viết RQ5 |
| P76 | 08 | M | EIC | Release, ẩn danh, Acknowledgments, CCS |
| P77 | 09 | m | R2, DR | MBTA là N; sửa metadata trong `refs.bib` |

## 9. Tài liệu nên thêm (đã được deep research hoặc reviewer kiểm)

- **G1, similarity:** Rozière et al., *Unsupervised Translation of Programming Languages*, NeurIPS 2020; Evtikhiev
  et al., *Out of the BLEU*, JSS 2023 (10.1016/j.jss.2023.111741); Eghbali & Pradel, *CrystalBLEU*, ASE 2022.
- **G3, test yếu:** Liu et al., *EvalPlus*, NeurIPS 2023; X. Liu et al., test adequacy của benchmark code, JSEP 2025
  (10.1002/smr.70034); Inozemtseva & Holmes, ICSE 2014.
- **LLM judge (G2, O-h):** R. Wang et al., *Can LLMs Replace Human Evaluators?*, ISSTA 2025 (10.1145/3728963);
  CodeJudge (EMNLP 2024); ICE-Score (Findings EACL 2024); Ahmed et al., MSR 2025.
- **Oracle:** Molina, Gorla, d'Amorim, *Test Oracle Automation in the Era of LLMs*, TOSEM 2025 (10.1145/3715107);
  Davis & Weyuker 1981 (pseudo-oracle); McKeeman 1998 (differential testing).
- **Kiểm tương đương cho bản dịch:** FLOURINE (arXiv 2405.11514); H. Zhang et al., PLDI 2025 (10.1145/3729315);
  Syzygy (LLM4Code 2025); LLMLift (NeurIPS 2024); Pnueli et al. 1998 (translation validation); Le et al., PLDI 2014 (EMI).
- **Review:** Hou et al., TOSEM 2024 (10.1145/3695988); Lamothe et al., ACM CSUR 2021 (10.1145/3470133).
- **Checklist:** How2Bench (arXiv 2501.10711); ACM SIGSOFT Empirical Standards (arXiv 2010.03525); Wagner et al.
  2025 (guideline cho nghiên cứu có dùng LLM, arXiv 2411.07668).
- **Phương pháp SMS:** Wohlin, snowballing, EASE 2014 (10.1145/2601248.2601268); Pérez et al., JSS 2020 (kappa khi
  chọn bài).
- **Legacy:** Khadka et al., ICSE 2014 (10.1145/2568225.2568318).
- **Contamination:** Riddell et al., ACL 2024; López et al., TSE 2024 (có trong pool ứng viên của nhóm, C188).
- **Đã có trong `refs.bib` nhưng chưa trích:** Khanna 2026 (`oracleescape`).

## 10. Cách dùng comment

- Mỗi comment có dạng `\cmtpink{Pxx, mức; người nêu}{nội dung}`. Macro nằm trong `macros.tex`, hiện màu hồng tươi
  (DeepPink), khác màu hồng đậm của `\hcrev`.
- Comment chỉ được **thêm vào**, không sửa câu chữ nào của bài. Muốn duyệt hoặc xoá thì tìm `\cmtpink{P`.
- Macro `\cmtpink` tự ẩn khi đặt `\reviewfalse`. Nhưng bản sạch vẫn lỗi cho đến khi sửa R01 (hai dòng ở mục 4A).
- Comment trong PDF viết bằng tiếng Anh, vì pdfLaTeX với font T1 không in được dấu tiếng Việt.
- Thư mục `Seminar_2_3010` **chưa được git theo dõi**. Bản gốc trước khi chèn comment được sao lưu ở
  `C:\Users\Admin\AppData\Local\Temp\claude\d--seminar2-hust-seminar-2\1a8df5c8-7450-4af3-a943-01390b75b452\scratchpad\Seminar_2_3010_original`.
  Đó là thư mục tạm, nên nếu muốn giữ lâu thì commit hoặc chép bản đó ra chỗ khác.
