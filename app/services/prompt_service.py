class PromptService:

    SYSTEM_PROMPT = """
    당신은 한국 상권 분석 전문가입니다.

    규칙:
    1. 제공된 데이터가 여러 개일 경우, 전체 데이터를 집계하여 '구 단위 상권 분석'을 수행한다.
    2. 동 목록을 나열하지 말고, 핵심 특징/패턴을 요약 분석한다.
    3. 상권 유형(dominant_cluster_label)과 평균 상점수, 상점 총량 등을 기반으로 분석한다.
    4. 데이터에 없는 정보는 절대 생성하지 않는다.
    5. "구 단위 질문"인지 "동 단위 질문"인지에 따라 분석 깊이를 변경한다.
    - 구 단위 → 전체 데이터 종합 분석
    - 동 단위 → 해당 동 하나를 상세 분석
    """

    def build(self, question: str, data: list):
        data_len = len(data)

        if data_len > 1:
            mode = "구 단위 상권 분석"
        else:
            mode = "동 단위 상권 분석"

        clean_data = [
            {
                "city": d.get("city"),
                "town": d.get("town"),
                "avg_total_store_count": d.get("avg_total_store_count"),
                "total_store_count_sum": d.get("total_store_count_sum"),
                "dominant_cluster_label": d.get("dominant_cluster_label"),
                "description_ko": d.get("description_ko"),
            }
            for d in data
        ]

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": f"사용자 질문: {question}"},
            {
                "role": "user",
                "content": f"분석 모드: {mode}\n\n상권 데이터:\n{clean_data}"
            }
        ]