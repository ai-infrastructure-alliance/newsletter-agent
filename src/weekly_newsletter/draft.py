import pickle
import datetime
import pypandoc
import os
import time

from weekly_newsletter.news_db_airtable import News, NewsState


class Section:

  def __init__(self, link, title, summaries):
    self.link = link
    self.title = title
    self.summaries = summaries
    self.best_summary = None
    self.prime = False


class DraftData:

  def __init__(self):
    self.start_date = None
    self.news = []
    self.sections = []
    self.last_iteration = 0


class Draft:

  def __init__(self, db, reviewer, writer, top_writer, refiner, logger):
    self.db = db
    self.reviewer = reviewer
    self.writer = writer
    self.top_writer = top_writer
    self.refiner = refiner
    self.logger = logger
    self.data = DraftData()

  def load_data(self):
    try:
      with open('draft.pkl', 'rb') as f:
        self.data = pickle.load(f)
    except FileNotFoundError:
      pass

  def save_data(self):
    with open('draft.pkl', 'wb') as f:
      pickle.dump(self.data, f)

  def set_frame_start(self, date):
    self.data.start_date = date
    self.data.news = self.db.retrieve_from(date)
    if len(self.data.news) % 2 == 1:
      self.data.news.append(self._fake_news())
    self.logger.info(f"Draft is set to start at {date}.")

  def _fake_news(self):
    return News("https://news.com", None, "Nothing happens",
                "Nothing interesting here", None)

  def inc_iteration(self):
    self.data.last_iteration += 1
    self.logger.info(f"Running iteration #{self.data.last_iteration}...")

  def run_iteration(self):
    self.reviewer.run_one_round(self.data.news)
    self.logger.info(f"Iteration #{self.data.last_iteration} is finished.")

  def finish_tournament(self):
    self.data.news.sort(key=lambda x: x.score, reverse=True)
    for pick in self.data.news[0:7]:
      pick.state = NewsState.PICK
    self.logger.info("Tournament is finished.")

  def get_picks(self):
    return [item for item in self.data.news if item.state == NewsState.PICK]

  def get_primes(self):
    return [item for item in self.data.news if item.state == NewsState.PRIME]

  def get_unpicks(self):
    return [item for item in self.data.news if item.state == NewsState.UNPICK]

  def init_sections_generation(self):
    self.logger.info("Generating sections...")

  def generate_sections(self):
    picks = self.get_picks()
    for pick in picks:
      generated_sections = [
        section for section in self.data.sections
        if section.link == pick.link and pick.state == NewsState.PICK
      ]
      if len(generated_sections) == 0:
        new_title, new_summaries = self.writer.rewrite_summary(
          pick.title, pick.summary, pick.comment)
        if new_title[0] == "\"": new_title = new_title[1:-1]
        section = Section(pick.link, new_title, new_summaries)
        self.data.sections.append(section)
        time.sleep(30)
    primes = self.get_primes()
    for pick in primes:
      generated_sections = [
        section for section in self.data.sections
        if section.link == pick.link and pick.state == NewsState.PRIME
      ]
      if len(generated_sections) == 0:
        new_title, new_summaries = self.top_writer.rewrite_summary(
          pick.title, pick.summary, pick.comment)
        section = Section(pick.link, new_title, new_summaries)
        section.prime = True
        self.data.sections.append(section)
        time.sleep(30)
    self.logger.info("Sections are generated.")

  def init_sections_refinement(self):
    self.logger.info("Refining sections...")

  def refine_sections(self):
    sections = self.data.sections
    for section in sections:
      if not section.best_summary:
        section.best_summary = self.refiner.refine_summary(
          section.title, section.summaries)
    self.logger.info("Sections are refined.")

  def init_generation_docx_unref(self):
    self.logger.info("Generating unrefined DOCX draft...")

  def generate_draft_docx_unrefined(self):
    markdown_content = ""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    self.data.sections.sort(key=lambda x: x.prime, reverse=True)
    for section in self.data.sections:
      markdown_content += f"# [{section.title}]({section.link})\n\n"
      for i, summary in enumerate(section.summaries, start=1):
        markdown_content += f"#### _Option {i}_\n"
        markdown_content += f"{summary}\n\n"
      markdown_content += "\n\n"
    markdown_content += "# Also this week:\n\n"
    for pick in self.get_unpicks():
      markdown_content += f"- [{pick.title}]({pick.link})\n"
    markdown_content += "\n\n"

    filename_md = f"draft_{current_time}.md"
    filename_docx = f"draft_{current_time}.docx"

    with open(filename_md, "w") as f:
      f.write(markdown_content)
    pypandoc.convert_file(filename_md, 'docx', outputfile=filename_docx)
    os.remove(filename_md)
    self.logger.info(f"Raw draft DOCX {filename_docx} is generated.")
    return filename_docx

  def generate_draft_docx_refined(self):
    markdown_content = ""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    self.data.sections.sort(key=lambda x: x.prime, reverse=True)
    for section in self.data.sections:
      markdown_content += f"# [{section.title}]({section.link})\n\n"
      markdown_content += f"{section.best_summary}\n\n"
    markdown_content += "# Also this week:\n\n"
    for pick in self.get_unpicks():
      markdown_content += f"- [{pick.title}]({pick.link})\n"
    markdown_content += "\n\n"

    filename_md = f"refined_draft_{current_time}.md"
    filename_docx = f"refined_draft_{current_time}.docx"

    with open(filename_md, "w") as f:
      f.write(markdown_content)
    pypandoc.convert_file(filename_md, 'docx', outputfile=filename_docx)
    os.remove(filename_md)
    self.logger.info(f"Refined draft DOCX {filename_docx} is generated.")
    return filename_docx