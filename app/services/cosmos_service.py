from azure.cosmos import CosmosClient
from app.core.config import Config

class CosmosService:
    def __init__(self):
        self.client = CosmosClient(Config.COSMOS_URL, credential=Config.COSMOS_KEY)
        self.db = self.client.get_database_client(Config.COSMOS_DB_NAME)

        self.city = self.db.get_container_client(Config.CONTAINER_CITY)
        self.cluster = self.db.get_container_client(Config.CONTAINER_CLUSTER)
        self.town = self.db.get_container_client(Config.CONTAINER_TOWN)

    # 사용자 질문 기반 동/도시 검색
    def search_town(self, keyword: str):
        keyword = keyword.strip()
        query = """
                SELECT *
                FROM c
                WHERE CONTAINS(c.city, @keyword, true)
                   OR CONTAINS(c.town, @keyword, true)
                """
        params = [{"name": "@keyword", "value": keyword}]
        items = list(
            self.town.query_items(
                query=query,
                parameters=params,
                enable_cross_partition_query=True
            )
        )
        return items

    # 군집 추가 조회 기능
    def get_cluster(self, cluster_id: int):
        query = "SELECT * FROM c WHERE c.cluster_id = @cid"
        params = [{"name": "@cid", "value": cluster_id}]
        return list(
            self.cluster.query_items(
                query=query,
                parameters=params,
                enable_cross_partition_query=True
            )
        )

    # 도시 단위 검색
    def search_city(self, city: str):
        query = "SELECT * FROM c WHERE c.city = @city"
        params = [{"name": "@city", "value": city}]
        return list(
            self.city.query_items(
                query=query,
                parameters=params,
                enable_cross_partition_query=True
            )
        )

    # 서울 전체 검색
    def search_all(self):
        query = "SELECT * FROM c"
        return list(self.town.query_items(
            query=query,
            enable_cross_partition_query=True
        ))