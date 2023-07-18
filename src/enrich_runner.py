import threading
from langchain import OpenAI
import schedule
import time
import os

from weekly_newsletter.news_db_airtable import NewsLinksDB
from weekly_newsletter.enricher import Enricher
from agents.reading_agent import ReadingAgent

from weekly_newsletter.draft_logger import setup_log

from dotenv import load_dotenv
load_dotenv()

# Tokens
BOT_TOKEN_NEWS = os.environ.get('BOT_TOKEN_NEWS')
OPEN_AI_KEY = os.environ.get('OPEN_AI_KEY')

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
BASE_ID = os.environ.get('BASE_ID')
TABLE_NAME = 'Weekly newsletter'

# LLMs
llm = OpenAI(temperature=0, openai_api_key=OPEN_AI_KEY)

# DB
news_links_db = NewsLinksDB(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)

# Logger
logger = setup_log('enrichment')

# Agents
reader = ReadingAgent(llm, logger)

# Enricher
enricher = Enricher(news_links_db, reader, logger)


def run_enrichment():
  enricher.enrich_news()


def enricher_process():
  p = threading.Thread(target=run_enrichment)
  p.start()
  p.join()


schedule.every(10).minutes.do(enricher_process)
print("Enricher is scheduled.\n")

while True:
  schedule.run_pending()
  time.sleep(1)
