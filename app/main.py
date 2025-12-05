from fastapi import FastAPI
from app.core.cors import setup_cors
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.cosmos_service import CosmosService
from app.services.openai_service import OpenAIService
from app.services.prompt_service import PromptService
from app.utils.location_extractor import extract_location

app = FastAPI(
    title="The Spot Chatbot API",
    descrption="2025-02 숙명여대 인공지능산업체특강 최종 프로젝트",
    version="1.0.0"
)

setup_cors(app)

cosmos = CosmosService()
prompt_service = PromptService()
openai_service = OpenAIService()

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # 1. 질문에서 지역 추출
    locations = extract_location(req.question)

    town_records = []

    # 2. 서울 전체 요청인 경우
    if "__SEOUL__" in locations:
        town_records = cosmos.search_all()

    # 3. 구/동 단위 요청 처리
    else:
        for loc in locations:
            result = cosmos.search_town(loc)
            town_records.extend(result)

    # 4. 검색된 데이터 없음 처리
    if not town_records:
        return ChatResponse(answer="해당 지역에 대한 상권 데이터가 없습니다.")

    # 4. 프롬프트 생성
    messages = prompt_service.build(req.question, town_records)

    # 5. OpenAI 호출
    answer = openai_service.ask(messages)

    return ChatResponse(answer=answer)