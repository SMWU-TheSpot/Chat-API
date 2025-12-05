import re

def extract_location(question: str):
    city_pattern = r"[가-힣]+구"
    town_pattern = r"[가-힣]+[0-9]*동"

    cities = re.findall(city_pattern, question)
    towns = re.findall(town_pattern, question)

    # 동이 있으면 동 기준
    if towns:
        return list(set(towns))

    # 구가 여러 개이면 그대로 반환
    if len(cities) >= 1:
        return list(set(cities))

    # 서울이 포함될 경우, 전체 조회
    if "서울" in question:
        return ["__SEOUL__"]

    # 아무것도 없으면 문장 전체
    return [question.strip()]