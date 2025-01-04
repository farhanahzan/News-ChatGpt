# Daily Mirror News Scraper and Chatbot

This project scrapes news articles from the Daily Mirror website, stores them in a Supabase database, and provides a chatbot interface to query the news articles. The chatbot uses OpenAI's API to answer queries based on news data, including relevant URLs for reference.

---

## Features

- Scrapes news articles, including their title, description, date, category, and URL.
- Stores the scraped data in a Supabase database.
- Embeds news data as vectors for similarity-based searches.
- Provides a chatbot interface that:
  - Searches similar news articles based on the query.
  - Generates human-like responses using OpenAI.
  - Includes URLs in the chatbot's responses for easy reference.

---

## Files and Their Purpose

1. **`dailymirror.py`**

   - Scrapes news articles from the Daily Mirror website.
   - Saves the scraped articles as `news.json`.

2. **`load_news_data.py`**

   - Loads the `news.json` data into the Supabase `news` table.

3. **`generate_embeddings.py`**

   - Converts the news article descriptions into embeddings and stores them in Supabase.

4. **`chatbot.py`**

   - Provides a chatbot interface for querying news data.
   - Searches similar news articles using embeddings.
   - Generates responses using OpenAI and includes article URLs in the response.

5. **`.env`**
   - Contains environment variables for accessing Supabase and OpenAI APIs.

---

## Prerequisites

- **Python 3.9+**
- **Linux OS**
- **Supabase Account**
- **OpenAI API Key**
- Required Python libraries:
  - `playwright`
  - `supabase`
  - `openai`

---

## Environment Variables

Create a `.env` file in the project directory with the following keys:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_api_key
```

---

## Database Setup

### Supabase Table Schema

Run the following SQL commands in your Supabase project:

```sql
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    date DATE NOT NULL,
    category TEXT NOT NULL
    url TEXT NOT NULL
);

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE news_embeddings (
    id SERIAL PRIMARY KEY,
    news_id INT REFERENCES news(id) ON DELETE CASCADE,
    embedding VECTOR(1536) NOT NULL
);

```

---

## Running the Project

### 1. Install Dependencies

Run the following command to install the required libraries:

```bash
pip install -r requirements.txt
```

### 2. Initialize Playwright

Run this to install the necessary browser binaries:

```bash
playwright install
```

### 3. Scrape News Data

Run the scraper to collect news articles and save them to `news.json`:

```bash
python dailymirror.py
```

### 4. Load Data into Supabase

Upload the news data from `news.json` to the Supabase `news` table:

```bash
python load_news_data.py
```

### 5. Generate Embeddings

Create embeddings for the news articles and save them in the Supabase database:

```bash
python generate_embeddings.py
```

### 6. Start the Chatbot

Run the chatbot interface to query news articles:

```bash
python chatbot.py
```

---

## How It Works

1. **Data Scraping**: `dailymirror.py` scrapes articles from the Daily Mirror website, including title, description, date, category, and URL, and saves them to `news.json`.
2. **Database Ingestion**: `load_news_data.py` uploads the scraped data to Supabase.
3. **Vectorization**: `generate_embeddings.py` converts article descriptions into vectors using OpenAI embeddings.
4. **Chatbot Interaction**: `chatbot.py`:
   - Converts user queries into vectors.
   - Finds similar news articles using Supabase vector similarity search.
   - Generates a response using OpenAI, including relevant article URLs.

---

## Example Usage

### Query

```
You: What's the latest in technology?
```

### Chatbot Response

```
Chatbot: Recent advancements in technology include breakthroughs in AI and renewable energy. Here are some relevant articles:

- AI and the Future of Work (https://example.com/ai-future)
- Green Tech Innovations in 2025 (https://example.com/green-tech-2025)
```

---

## File Execution Order

1. `dailymirror.py`: Scrape and save data to `news.json`.
2. `load_news_data.py`: Load the scraped data into Supabase.
3. `generate_embeddings.py`: Generate and save embeddings.
4. `chatbot.py`: Start the chatbot interface.

---

## Notes

- Ensure all environment variables are correctly set in the `.env` file.
- Use Playwright's Chromium browser for scraping.
- Test database connections and OpenAI API keys before running the chatbot.

---

## Future Enhancements

- Add more categories and advanced filters for chatbot queries.
- Implement rate limiting to comply with API usage policies.
- Enhance scraping logic for more robust data collection.
