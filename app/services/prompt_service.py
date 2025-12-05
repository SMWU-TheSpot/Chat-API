import json
from collections import defaultdict

class PromptService:
    SYSTEM_PROMPT = """
    당신은 한국 상권 분석 전문가입니다.

    규칙:
    1. 입력 데이터는 '동 단위 데이터'이며, 여러 동이 제공되면 자동으로 집계해 '구 단위 분석'을 수행한다.
    2. 동 목록을 불필요하게 나열하지 말고, 패턴·특징 중심으로 요약한다.
    3. 단, 사용자가 '어디가 좋을지', '어디에 차려야 할지', '입지 추천'과 같이 **입지 선택을 요구하는 질문을 한 경우**, 
       데이터 기반으로 1~3개의 동을 구체적으로 제안할 수 있다. (허용)
    4. 분석 근거는 반드시 데이터 내 값만 사용한다. (임의 정보 생성 금지)
       - 상권 유형(dom_cluster_label)
       - 총 점포 수(total_town_store_count)
       - 클러스터 점포 수(dom_cluster_store_count)
    5. 구 단위 분석은 대표 상권 유형, 점포 규모, 특징 비교를 중심으로 한다.
    6. 동 단위 분석은 상권 유형, 점포 구성, description_ko를 활용해 상세하게 설명한다.

    사용자 질문이 '입지 추천'을 포함할 경우 실제 동 단위 후보를 제안하라.
    """

    def aggregate_by_city(self, data: list):
        city_map = defaultdict(lambda: {
            "total_store_sum": 0,  # 전체 점포 수 총합
            "cluster_store_sum": 0,  # 클러스터 점포 수 총합
            "count": 0,
            "cluster_count": defaultdict(int),
        })

        for d in data:
            city = d.get("city")
            if not city:
                continue

            # 동 단위 데이터의 필드명 적용
            total_store = d.get("total_town_store_count", 0)
            cluster_store = d.get("dom_cluster_store_count", 0)
            cluster_label = d.get("dom_cluster_label")  # 상권 유형

            city_map[city]["total_store_sum"] += total_store
            city_map[city]["cluster_store_sum"] += cluster_store
            city_map[city]["count"] += 1

            if cluster_label:
                city_map[city]["cluster_count"][cluster_label] += 1

        # 집계 결과 변환
        result = []
        for city, v in city_map.items():
            if v["cluster_count"]:
                dominant_cluster = max(v["cluster_count"], key=v["cluster_count"].get)
            else:
                dominant_cluster = "미분류"

            result.append({
                "city": city,
                "total_store_count": v["total_store_sum"],
                "avg_store_count": round(v["total_store_sum"] / v["count"], 2),
                "dominant_cluster": dominant_cluster
            })
        return result

    def build(self, question: str, data: list):
        aggregated = self.aggregate_by_city(data)
        payload_json = json.dumps(aggregated, ensure_ascii=False)

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": f"사용자 질문: {question}"},
            {"role": "user", "content": f"구 단위 상권 요약(JSON):\n{payload_json}"}
        ]