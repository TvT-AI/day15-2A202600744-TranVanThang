# Báo cáo Cá nhân (Individual Reflection)

**Họ và tên:** Trần Văn Thắng
**Vai trò trong nhóm:** AI/Backend Engineer

## 1. Đóng góp kỹ thuật (Engineering Contribution)
- Phát triển module `synthetic_gen.py` để sinh ra bộ Golden Dataset gồm 50 test cases, bao gồm cả các câu hỏi Red Teaming nhằm đánh lừa hệ thống.
- Xây dựng Multi-Judge Engine trong `llm_judge.py` tích hợp logic phân xử (Consensus) khi điểm số từ các mô hình bị lệch.
- Triển khai thuật toán tính toán Hit Rate và MRR trong `retrieval_eval.py` để đánh giá chính xác chất lượng của Vector DB.
- Tối ưu hóa quá trình Benchmark bằng `asyncio.gather` giúp hệ thống chạy đa luồng nhanh chóng.

## 2. Chiều sâu kỹ thuật (Technical Depth)
- **MRR (Mean Reciprocal Rank):** Hiểu rõ tầm quan trọng của thứ hạng tài liệu trả về. Nếu tài liệu đúng nằm ở top 1, MRR là 1. Nếu nằm ở top 2, MRR là 0.5. Điều này giúp đánh giá sát thực tế hơn so với Hit Rate đơn thuần.
- **Multi-Judge Consensus:** Nhận thức được rủi ro khi chỉ dùng 1 LLM làm giám khảo (có thể có Position Bias hoặc Model Bias). Việc kết hợp 2 model và dùng model thứ 3 để giải quyết mâu thuẫn giúp kết quả khách quan hơn.

## 3. Khó khăn & Khắc phục (Problem Solving)
- **Vấn đề:** Khi tăng số lượng test cases lên 50, hệ thống chạy tuần tự mất quá nhiều thời gian và dễ gặp lỗi Rate Limit từ API.
- **Khắc phục:** Chuyển đổi toàn bộ pipeline sang Asynchronous (bất đồng bộ) với giới hạn `batch_size` trong `runner.py` để chạy song song 5 cases một lúc, vừa tăng tốc vừa đảm bảo không vượt quá hạn mức API.
