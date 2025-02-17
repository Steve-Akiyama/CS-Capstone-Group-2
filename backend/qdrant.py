from qdrant_client import QdrantClient, models

class QdrantConnect:
    def __init__(self, host: str, api_key: str):

        self.host = host
        self.api_key = api_key
        self.qdrant_client = QdrantClient(
            url=host,
            api_key=api_key,
        )

    def get_subchapter_from_section(self, collection_name: str, section: str):
        records, next_token = self.qdrant_client.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="section",
                        match=models.MatchValue(value=section),
                    ),
                ]
            ),
        )
        text = records[0].payload.get("text")
        return text

    def get_subchapter_from_title(self, collection_name: str, title: str):
        records, next_token = self.qdrant_client.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="title",
                        match=models.MatchValue(value=title),
                    ),
                ]
            ),
        )
        text = records[0].payload.get("text")
        return text
    
    def get_chapter_from_chapter(self, collection_name: str, title: str):
        records, next_token = self.qdrant_client.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="chapter",
                        match=models.MatchValue(value=title),
                    ),
                ]
            ),
        )
        text = records[0].payload.get("text")
        return text