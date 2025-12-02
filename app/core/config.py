import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Cosmos DB connection
    COSMOS_URL = os.getenv("COSMOS_URL")
    COSMOS_KEY = os.getenv("COSMOS_KEY")
    COSMOS_DB_NAME = "thespotDB"

    # Containers inside the-spot DB
    CONTAINER_CITY = "ClusterCitySummary"
    CONTAINER_CLUSTER = "ClusterSummary"
    CONTAINER_TOWN = "TownSummary"

    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
    AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")