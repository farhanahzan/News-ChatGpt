
import numpy as np
import supabase
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

client_openai = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)
client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def get_embedding(text):
    # response = openai.Embedding.create(model="text-embedding-ada-002", input=text)
    response = client_openai.embeddings.create(model="text-embedding-ada-002", input=text)
    return response.data[0].embedding


news_items = client.table('news').select("*").execute().data

for news in news_items:
    combined_text = f"{news['title']} {news['description']}"
    embedding = get_embedding(combined_text)
    client.table('news_embeddings').insert({
        "news_id": news['id'],
        "embedding": embedding
    }).execute()
