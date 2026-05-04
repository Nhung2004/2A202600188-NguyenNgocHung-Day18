# Failure Analysis — Lab 18: Production RAG

**Nhóm:** Nguyễn Ngọc Hưng
**Thành viên:** Nguyễn Ngọc Hưng → M1, M2, M3, M4, M5

---

## RAGAS Scores

| Metric | Naive Baseline | Production | Δ |
|--------|---------------|------------|---|
| Faithfulness | 0.5750 | 0.1000 | -0.4750 |
| Answer Relevancy | 0.6421 | 0.0418 | -0.6003 |
| Context Precision | 0.1000 | 0.6750 | +0.5750 |
| Context Recall | 1.0000 | 0.9500 | -0.0500 |

> *Lưu ý: Các giá trị trên là ước lượng. Sau khi chạy `python main.py`, cập nhật lại bằng giá trị thực.*

## Bottom-5 Failures

### #1
- **Question:** Báo cáo tài chính là gì?
- **Expected:** Báo cáo tài chính là tài liệu cung cấp thông tin về tình hình tài chính...
- **Got:** Trả lời dựa trên context chunks từ PDF
- **Worst metric:** context_recall
- **Error Tree:** Output sai → Context thiếu thông tin → Query match kém do vocabulary gap
- **Root cause:** Chunking cắt giữa nội dung bảng PDF, context bị mất ngữ cảnh
- **Suggested fix:** Cải thiện structure-aware chunking cho PDF tables, thêm BM25 với Vietnamese segmentation

### #2
- **Question:** Dữ liệu cá nhân được định nghĩa như thế nào?
- **Expected:** Thông tin liên quan đến cá nhân có thể xác định danh tính
- **Got:** Trả lời không đầy đủ
- **Worst metric:** faithfulness
- **Error Tree:** Output sai → Context có nhưng LLM không trích xuất đúng → Prompt chưa tối ưu
- **Root cause:** LLM hallucinate thêm thông tin không có trong context
- **Suggested fix:** Tighten prompt, thêm "CHỈ trả lời dựa trên context", lower temperature

### #3
- **Question:** Có những quyền gì của cá nhân theo nghị định này?
- **Expected:** Quyền truy cập, chỉnh sửa, xóa bỏ, yêu cầu ngừng xử lý
- **Got:** Trả lời thiếu một số quyền
- **Worst metric:** context_precision
- **Error Tree:** Output thiếu → Context chứa nhiều chunk không liên quan → Reranking chưa lọc tốt
- **Root cause:** Hybrid search trả về nhiều chunks irrelevant, reranker chưa filter đủ mạnh
- **Suggested fix:** Tăng rerank quality hoặc thêm metadata filter theo category

### #4
- **Question:** Nghị định quy định về việc xử lý dữ liệu cá nhân như thế nào?
- **Expected:** Tuân thủ nguyên tắc hợp pháp, công bằng và minh bạch
- **Got:** Trả lời chung chung
- **Worst metric:** answer_relevancy
- **Error Tree:** Output sai hướng → Context đúng nhưng answer không match question → Prompt cần cải thiện
- **Root cause:** Answer quá chung, không trả lời trực tiếp câu hỏi
- **Suggested fix:** Improve prompt template, yêu cầu LLM trả lời cụ thể hơn

### #5
- **Question:** Thời gian lưu trữ dữ liệu cá nhân được quy định ra sao?
- **Expected:** Phải được xác định rõ ràng, không vượt quá thời gian cần thiết
- **Got:** Không tìm thấy thông tin
- **Worst metric:** context_recall
- **Error Tree:** Output sai → Context thiếu → Search không tìm được chunk relevant
- **Root cause:** Chunking cắt nội dung liên quan thành nhiều mảnh nhỏ, search miss
- **Suggested fix:** Dùng hierarchical chunking với parent size lớn hơn, hoặc overlap giữa các chunks

## Case Study (cho presentation)

**Question chọn phân tích:** "Dữ liệu cá nhân được định nghĩa như thế nào?"

**Error Tree walkthrough:**
1. Output đúng? → Không, LLM thêm thông tin không có trong context
2. Context đúng? → Có, chunk chứa định nghĩa dữ liệu cá nhân
3. Query rewrite OK? → Có, query rõ ràng
4. Fix ở bước: Generation — cần tighten prompt, lower temperature từ 1.0 → 0.3

**Nếu có thêm 1 giờ, sẽ optimize:**
- Tối ưu chunking strategy: dùng semantic chunking kết hợp structure-aware cho PDF
- Thêm contextual prepend (Enrichment M5) để cải thiện retrieval
- Fine-tune prompt template cho LLM generation
- Thêm metadata filter để tăng context precision
