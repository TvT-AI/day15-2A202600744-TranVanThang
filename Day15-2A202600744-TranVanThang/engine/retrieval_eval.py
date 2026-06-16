from typing import List, Dict

class RetrievalEvaluator:
    def __init__(self):
        pass

    def calculate_hit_rate(self, expected_ids: List[str], retrieved_ids: List[str], top_k: int = 3) -> float:
        """
        TODO: Tính toán xem ít nhất 1 trong expected_ids có nằm trong top_k của retrieved_ids không.
        """
        top_retrieved = retrieved_ids[:top_k]
        hit = any(doc_id in top_retrieved for doc_id in expected_ids)
        return 1.0 if hit else 0.0

    def calculate_mrr(self, expected_ids: List[str], retrieved_ids: List[str]) -> float:
        """
        TODO: Tính Mean Reciprocal Rank.
        Tìm vị trí đầu tiên của một expected_id trong retrieved_ids.
        MRR = 1 / position (vị trí 1-indexed). Nếu không thấy thì là 0.
        """
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in expected_ids:
                return 1.0 / (i + 1)
        return 0.0

    async def score(self, test_case: Dict, agent_response: Dict) -> Dict:
        """
        Đánh giá Retrieval cho 1 câu truy vấn.
        """
        expected_ids = test_case.get("expected_retrieval_ids", [])
        retrieved_ids = agent_response.get("retrieved_ids", [])
        
        hit_rate = self.calculate_hit_rate(expected_ids, retrieved_ids)
        mrr = self.calculate_mrr(expected_ids, retrieved_ids)
        
        # Thêm điểm ảo cho faithfulness và relevancy để giả lập RAGAS
        return {
            "faithfulness": 0.9 if hit_rate > 0 else 0.4, 
            "relevancy": 0.8 if hit_rate > 0 else 0.3,
            "retrieval": {
                "hit_rate": hit_rate,
                "mrr": mrr
            }
        }
