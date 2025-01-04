import json
import supabase

import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')


client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# Load the JSON file
with open('news.json', 'r') as file:
    news_data = json.load(file)

# Insert news data into the database
for item in news_data:
    response = client.table('news').insert({
        "title": item["title"],
        "description": item["description"],
        "url": item["url"],
        "category": item["category"],
        "date": item["date"],
    }).execute()
    print(response)
