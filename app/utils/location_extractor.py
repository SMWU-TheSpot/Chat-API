import re

def extract_location(question: str):
    # 패턴: OOO구 / OOO동 / OOO1동 / OO2동 등
    city_pattern = r"[가-힣]+구"
    town_pattern = r"[가-힣]+[0-9]*동"

    found_city = re.findall(city_pattern, question)
    found_town = re.findall(town_pattern, question)

    city = found_city[0] if found_city else None
    town = found_town[0] if found_town else None

    # town이 가장 중요 - TownSummary 검색은 town 기준
    if town:
        return town
    if city:
        return city

    # 둘 다 없으면 전체 문장을 그대로 반환 (fallback)
    return question.strip()