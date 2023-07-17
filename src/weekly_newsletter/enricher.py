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

  def enrich_news_titles(self):
    news = self.db.get_news_with_empty_title()
    n = 0
    for row in news:
      row.title = self.reader.define_title_by_link(row.link)
      n += 1
    self.db.update_news_from_list(news)
    return n

  def enrich_news_summaries(self):
    news = self.db.get_news_with_empty_summary()
    n = 0
    for row in news:
      row.summary = self.reader.define_summary_by_link(row.link)
      n += 1
    self.db.update_news_from_list(news)
    return n

  def enrich_news(self):
    self.logger.info("[Enricher] Enriching news...")

    self.logger.info("[Enricher] Enriching types...")
    n = self.enrich_news_types()
    self.logger.info(f"[Enricher] {n} types enriched")

    self.logger.info("[Enricher] Enriching titles...")
    n = self.enrich_news_titles()
    self.logger.info(f"[Enricher] {n} titles enriched")

    self.logger.info("[Enricher] Enriching summaries...")
    n = self.enrich_news_summaries()
    self.logger.info(f"[Enricher] {n} summaries enriched")

    self.logger.info("[Enricher] Enrichment is complete.")
