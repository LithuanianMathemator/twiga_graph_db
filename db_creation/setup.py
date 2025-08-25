import numpy as np
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph
import asyncio
from langchain_core.documents import Document
import json

class Graph_DB:
    
    def __init__(self, url, user, password, openai_api_key):
        
        self.url = url
        self.user = user
        self.password = password
        self.driver = GraphDatabase.driver(
            url, 
            auth=(user, password)
        )
        self.openai_api_key = openai_api_key
        self.graph = Neo4jGraph(
            url=url, 
            username=user, 
            password=password, 
            refresh_schema=False
        )

    async def create_graph(self, json_path: str):
        
        llm = ChatOpenAI(temperature=1, model_name="gpt-4.1-nano")
        llm_transformer = LLMGraphTransformer(llm=llm)
        
        documents = get_doc_from_json(json_path)
        graph_documents = await llm_transformer.aconvert_to_graph_documents(documents)
        self.graph.add_graph_documents(graph_documents)

def get_doc_from_json(json_path: str):

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunk_docs = list(
        map(lambda chunk: Document(page_content=(chunk["content"])), data["chunks"][:100])
    )

    return chunk_docs

if __name__ == "__main__":

    load_dotenv()
    db = Graph_DB(
        url=os.getenv("DB_URL"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    asyncio.run(db.create_graph("./data/biology_form_4.json"))
