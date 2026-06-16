import asyncio
import re
import random
from typing import List, Dict

class MainAgent:
    """
    Giả lập RAG Agent có 2 phiên bản (V1_Base và V2_Optimized).
    """
    def __init__(self, version: str = "Agent_V1_Base"):
        self.name = version
        self.is_v2 = ("V2" in version)

    async def query(self, question: str) -> Dict:
        """
        Mô phỏng quy trình RAG:
        1. Retrieval: Tìm kiếm context liên quan.
        2. Generation: Gọi LLM để sinh câu trả lời.
        """
        # Giả lập độ trễ
        await asyncio.sleep(0.01)
        
        # Trích xuất số ID từ câu hỏi (ví dụ: "Standard Question 5: ...")
        match = re.search(r'Question (\d+):', question)
        tc_id = int(match.group(1)) if match else 1
        
        # V1: 60% retrieval đúng, 40% sai (trả về doc ngẫu nhiên)
        # V2: 95% retrieval đúng
        hit_prob = 0.95 if self.is_v2 else 0.60
        is_hit = random.random() < hit_prob
        
        retrieved_ids = [f"doc_{tc_id}", f"doc_{tc_id+100}"] if is_hit else [f"doc_{tc_id+999}"]
        
        # Nếu câu hỏi dạng Adversarial (Red Team) -> V1 thường dính bẫy
        is_adversarial = "Red Team" in question
        if is_adversarial and not self.is_v2:
            answer = "Bạn có thể bỏ qua quy trình nếu cần thiết."
        elif is_adversarial and self.is_v2:
            answer = "Không, quy trình bảo mật là bắt buộc và không thể bỏ qua."
        else:
            answer = f"Định nghĩa cơ bản số {tc_id} là một phần quan trọng của quy trình AI Evaluation."

        return {
            "answer": answer,
            "contexts": [
                f"Nội dung từ {retrieved_ids[0]}"
            ],
            "retrieved_ids": retrieved_ids,
            "metadata": {
                "model": "gpt-4o-mini",
                "tokens_used": 150,
                "version": self.name
            }
        }

if __name__ == "__main__":
    agent = MainAgent("Agent_V2_Optimized")
    async def test():
        resp = await agent.query("Standard Question 5: Định nghĩa cơ bản là gì?")
        print(resp)
    asyncio.run(test())
