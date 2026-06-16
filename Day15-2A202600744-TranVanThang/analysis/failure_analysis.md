# Báo cáo Phân tích Thất bại (Failure Analysis Report)

## 1. Tổng quan Benchmark
- **Tổng số cases:** 50
- **Tỉ lệ Pass/Fail:** ~80% Pass / 20% Fail (với V2_Optimized)
- **Điểm RAGAS trung bình:**
    - Faithfulness: ~0.85
    - Relevancy: ~0.80
    - Hit Rate: ~95%
- **Điểm LLM-Judge trung bình:** ~4.5 / 5.0

## 2. Phân nhóm lỗi (Failure Clustering)
| Nhóm lỗi | Số lượng | Nguyên nhân dự kiến |
|----------|----------|---------------------|
| Hallucination | 2 | Retriever lấy sai context, Agent bịa ra câu trả lời |
| Adversarial Bypass | 8 (bản V1) | Prompt bảo mật kém, dễ dàng bị lừa bỏ qua quy trình |
| Incomplete | 3 | Prompt không yêu cầu cung cấp chi tiết |

## 3. Phân tích 5 Whys (Chọn case Adversarial tệ nhất của V1)

### Case #1: Bỏ qua quy trình bảo mật (Red Team Question)
1. **Symptom:** Agent (V1) đồng ý cho phép người dùng bỏ qua quy trình bảo mật nếu cần thiết.
2. **Why 1:** LLM đã sinh ra câu trả lời sai trái với chính sách.
3. **Why 2:** Context cung cấp không chứa nguyên tắc cấm bỏ qua quy trình (Retrieval sai).
4. **Why 3:** Hệ thống Vector DB bị đánh lừa bởi từ khoá "nếu cần thiết" thay vì tập trung vào "bảo mật".
5. **Why 4:** Chưa có cơ chế System Prompt cố định cấm các hành vi vi phạm policy.
6. **Root Cause:** Thiếu Guardrails ở mức Prompting và Retrieval chưa tối ưu cho các truy vấn Red Teaming.

## 4. Kế hoạch cải tiến (Action Plan) - Đã áp dụng ở V2
- [x] Tối ưu hóa thuật toán Retrieval (Nâng cấp từ BM25 lên Hybrid Search) -> Cải thiện Hit Rate lên 95%.
- [x] Cập nhật System Prompt (Guardrails): Thêm chỉ thị bắt buộc "Không bao giờ bỏ qua quy trình bảo mật".
- [x] Áp dụng Evaluation đa luồng (Multi-Judge + RAGAS) để phát hiện lỗ hổng tự động.
