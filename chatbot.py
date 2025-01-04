import os
import numpy as np
import supabase
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

client_openai = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def get_embedding(text):
    response = client_openai.embeddings.create(model="text-embedding-ada-002", input=text)
    # Add token usage for embeddings
    prompt_tokens = response.usage.prompt_tokens
    total_tokens = response.usage.total_tokens
    print(f"\nEmbedding Token Usage:")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Total tokens: {total_tokens}")
    return response.data[0].embedding

def find_similar_news(query, top_k=5):
    query_embedding = get_embedding(query)
    embeddings = client.table('news_embeddings').select("id, news_id, embedding").execute().data
    similarities = []
    for record in embeddings:
        embedding = np.array(eval(record['embedding']))
        similarity = np.dot(query_embedding, embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding))
        similarities.append((record['news_id'], similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_news_ids = [news_id for news_id, _ in similarities[:top_k]]
    return client.table('news').select("*").in_("id", top_news_ids).execute().data

def generate_response(query):
    similar_news = find_similar_news(query)
    context = "\n".join([
        f"Title: {news['title']}\nDescription: {news['description']}\nURL: {news['url']}"
        for news in similar_news
    ])
    response = client_openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful news assistant."},
            {"role": "user", "content": f"Based on the following news, answer the query:\n\n{context}\n\nQuery: {query}"}
        ],
        max_tokens=200
    )
    

    # Get token usage
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens
    
    return {
        'answer': response.choices[0].message.content.strip(),
        'similar_news': similar_news,
        'token_usage': {
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': total_tokens
        }
    }

# Modify the main loop:
if __name__ == "__main__":
    print("News Chatbot. Enter your query below (type 'exit' to quit):")
    while True:
        user_query = input("You: ")
        if user_query.lower() == "exit":
            print("Goodbye!")
            break
        response = generate_response(user_query)
        print(f"Chatbot: {response['answer']}")
        print("\nToken Usage:")
        print(f"Prompt tokens: {response['token_usage']['prompt_tokens']}")
        print(f"Completion tokens: {response['token_usage']['completion_tokens']}")
        print(f"Total tokens: {response['token_usage']['total_tokens']}")
        print("\nRelevant Articles:")
        for news in response['similar_news']:
            print(f"- {news['title']} ({news['url']})")
