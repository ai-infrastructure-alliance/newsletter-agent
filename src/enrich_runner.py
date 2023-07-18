import threading
import schedule
import time
import os

from agent_reader import get_model, ModelType

from weekly_newsletter.news_db_airtable import NewsLinksDB
from weekly_newsletter.enricher import Enricher
from agents.reading_agent import ReadingAgent

from weekly_newsletter.draft_logger import setup_log

from dotenv import load_dotenv
load_dotenv()

# Tokens
OPEN_AI_KEY = os.environ.get('OPEN_AI_KEY')
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
BASE_ID = os.environ.get('BASE_ID')
TABLE_NAME = 'Weekly newsletter'

# DB
news_links_db = NewsLinksDB(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)

# Logger
logger = setup_log('enrichment')

# Reader
model = get_model(ModelType.OPENAI_GPT35, OPEN_AI_KEY)
reader = ReadingAgent(model, logger)

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
