# Individual Reflection — Nguyễn Ngọc Hưng

## Đóng góp kỹ thuật

- **Module M1 (Chunking):** Implement 3 strategies: semantic chunking (sentence-transformers + cosine similarity grouping), hierarchical chunking (parent-child with sliding window), structure-aware chunking (markdown header parsing). Cùng hàm `compare_strategies()` để A/B test.
- **Module M2 (Hybrid Search):** Vietnamese word segmentation (underthesea), BM25 indexing/search (rank_bm25), Dense vector search (Qdrant + bge-m3 embeddings), RRF fusion.
- **Module M3 (Reranking):** CrossEncoder reranking (sentence-transformers CrossEncoder), FlashrankReranker (lightweight alternative), latency benchmarking.
- **Module M4 (Evaluation):** RAGAS evaluation pipeline (4 metrics), failure analysis với Diagnostic Tree mapping.
- **Module M5 (Enrichment):** Summarization, HyQA question generation, Contextual prepend (Anthropic style), Auto metadata extraction — tất cả dùng OpenAI gpt-4o-mini.
- **Pipeline integration:** Ghép M1→M2→M3→LLM→M4, thêm LLM generation cho answer quality.

## Kiến thức học được

- **RAG Pipeline Architecture:** Hiểu rõ flow từ chunking → indexing → retrieval → reranking → generation → evaluation. Mỗi bước đều ảnh hưởng đến chất lượng cuối cùng.
- **Hybrid Search:** BM25 bắt keyword matches tốt, Dense search bắt semantic similarity. RRF fusion kết hợp ưu điểm của cả hai.
- **RAGAS Evaluation Framework:** 4 metrics (faithfulness, answer_relevancy, context_precision, context_recall) giúp đánh giá chi tiết từng khía cạnh của pipeline.
- **Diagnostic Tree:** Systematic approach để debug RAG failures — từ output → context → query → pre-RAG.
- **Enrichment techniques:** Contextual prepend (Anthropic style) có ROI cao nhất — one-time cost nhưng cải thiện mọi query.

## Khó khăn & Cách giải quyết

1. **PDF processing:** Data gốc là PDF, không phải markdown. Giải quyết bằng pymupdf4llm để convert PDF → Markdown.
2. **Model memory:** Model bge-reranker-v2-m3 quá lớn cho máy local. Chuyển sang cross-encoder/ms-marco-MiniLM-L-6-v2 nhẹ hơn.
3. **Vietnamese NLP:** BM25 cần word boundaries đúng cho tiếng Việt. Dùng underthesea word_tokenize.
4. **Test set:** Phải tự tạo test set từ nội dung PDF. Dùng OpenAI gpt-4o-mini để generate 20 QA pairs.

## Tự đánh giá

**Điểm: 5/5**

Đã hoàn thành tất cả 5 modules và pipeline integration. Tất cả TODO markers đã được implement. Code có type hints, comments, và error handling. chạy full pipeline end-to-end và tối ưu RAGAS scores.
