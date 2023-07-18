class Enricher:

  def __init__(self, db, reader, logger):
    self.db = db
    self.reader = reader
    self.logger = logger

  def enrich_news_types(self):
    news = self.db.get_news_with_empty_type()
    n = 0
    for row in news:
      row.type = str(self.reader.define_type_by_link(row.link).value)
      n += 1
    self.db.update_news_from_list(news)
    return n

  def enrich_news_titles_and_summaries(self):
    news = self.db.get_news_with_empty_title()
    n = 0
    for row in news:
      result = self.reader.define_title_and_summary_by_link(row.link)
      if result is None:
        continue
      row.title = result["title"]
      row.summary = result["summary"]
      n += 1
    self.db.update_news_from_list(news)
    return n

  def enrich_news(self):
    self.logger.info("[Enricher] Enriching news...")

    self.logger.info("[Enricher] Enriching types...")
    n = self.enrich_news_types()
    self.logger.info(f"[Enricher] {n} types enriched")

    self.logger.info("[Enricher] Enriching titles & summaries...")
    n = self.enrich_news_titles_and_summaries()
    self.logger.info(f"[Enricher] {n} summaries & titles enriched")

    self.logger.info("[Enricher] Enrichment is complete.")
