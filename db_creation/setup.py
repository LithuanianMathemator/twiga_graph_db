import numpy as np
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

class Graph_DB:
    
    def __init__(self, url, user, password, openai_api_key):
        
        self.driver = GraphDatabase.driver()
        self.driver = GraphDatabase.driver(url, auth=(user, password))
        openai.api_key = openai_api_key
        self.schema = self.generate_schema()

    def add_node():
        pass

    def generate_schema():
        pass

if __name__ == "__main__":

    load_dotenv()
    db = Graph_DB(
        url=os.getenv("DB_URL"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )