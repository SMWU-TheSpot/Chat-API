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
    keyword = extract_location(req.question)

    town_records = cosmos.search_town(keyword)

    messages = prompt_service.build(req.question, town_records)

    answer = openai_service.ask(messages)

    return ChatResponse(answer=answer)