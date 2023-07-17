from pyairtable import Table
from pyairtable.formulas import match
from enum import Enum


class NewsState(Enum):
  PRIME = "prime"
  PICK = "pick"
  UNPICK = "unpick"


class News:

  def __init__(self, link, type, title, summary, comment, id=None):
    self.link = link
    self.type = type
    self.title = title
    self.summary = summary
    self.comment = comment
    self.id = id
    self.state = NewsState.UNPICK
    self.score = 0

  @staticmethod
  def from_fields(fields):
    news = News(fields["URL"], fields["Type"], fields["Title"],
                fields["Summary"], fields["Comment"])
    return news

  def to_fields(self):
    return {
      "URL": self.link,
      "Type": self.type,
      "Title": self.title,
      "Summary": self.summary,
      "Comment": self.comment,
    }


class NewsLinksDB:

  def __init__(self, api_key, base_id, table_name):
    self.table = Table(api_key, base_id, table_name)

  def add_link(self, url, comment, author):
    formula = match({'URL': url})
    row = self.table.first(formula=formula)
    if not row:
      self.table.create({'URL': url, 'Comment': comment, 'Author': author})
    return row == None

  def get_all(self, formula=None):
    rows = []
    if formula is None:
      rows = self.table.all()
    else:
      rows = self.table.all(formula=formula)
    news = []
    for row in rows:
      url = row['fields']['URL']
      type = row['fields']['Type'] if 'Type' in row['fields'] else None
      title = row['fields']['Title'] if 'Title' in row['fields'] else None
      summary = row['fields']['Summary'] if 'Summary' in row['fields'] else None
      comment = row['fields']['Comment'] if 'Comment' in row['fields'] else None
      news.append(News(url, type, title, summary, comment, row['id']))
    return news

  def retrieve_from(self, start_date):
    formatted_date = start_date.strftime("%Y-%m-%dT%H:%M:%S")
    formula = f"CREATED_TIME() > '{formatted_date}'"
    return self.get_all(formula)

  def _get_news_with_empty_field(self, field):
    formula = f"{{}} = BLANK()".format(field)
    return self.get_all(formula)

  def get_news_with_empty_type(self):
    return self._get_news_with_empty_field("Type")

  def get_news_with_empty_title(self):
    return self._get_news_with_empty_field("Title")

  def get_news_with_empty_summary(self):
    return self._get_news_with_empty_field("Summary")

  def update_news_from_list(self, news):
    for news_item in news:
      fields = news_item.to_fields()
      self.table.update(news_item.id, fields)


### Backup ###

  def clean_all_news_picks(self):
    raise NotImplementedError("The method is not implemented for Airtable")

  def insert_picks(self, links):
    raise NotImplementedError("The method is not implemented for Airtable")

  # link_data: String (link)
  def pick_a_piece_of_news(self, link_data):
    raise NotImplementedError("The method is not implemented for Airtable")

  def unpick_a_piece_of_news(self, link_data):
    raise NotImplementedError("The method is not implemented for Airtable")

  def get_all_picks(self):
    raise NotImplementedError("The method is not implemented for Airtable")

  def cleanup_empty_strings_news(self):
    raise NotImplementedError("The method is not implemented for Airtable")

  def clean_news_summaries_from(self, start_date):
    raise NotImplementedError("The method is not implemented for Airtable")

  def clean_db(self):
    raise NotImplementedError("The method is not implemented for Airtable")

  def delete_link(self, url):
    raise NotImplementedError("The method is not implemented for Airtable")
