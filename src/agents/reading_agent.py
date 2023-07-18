from enum import Enum
from agent_reader import summarize

class LinkType(Enum):
  PROJECT = "project"
  PAPER = "paper"
  TWEET = "tweet"
  REDDIT = "reddit"
  YOUTUBE = "youtube"
  POST = "post"

  @staticmethod
  def get_type_from_link(link):
    if "github.com" in link:
      return LinkType.PROJECT
    elif "arxiv.org" in link:
      return LinkType.PAPER
    elif "twitter.com" in link:
      return LinkType.TWEET
    elif "reddit.com" in link:
      return LinkType.REDDIT
    elif "youtube.com" in link:
      return LinkType.YOUTUBE
    else:
      return LinkType.POST


class ReadingAgent:

  def __init__(self, model, logger):
    self.model = model
    self.logger = logger

  def define_type_by_link(self, link):
    link_type = LinkType.get_type_from_link(link)
    return link_type

  def define_title_and_summary_by_link(self, link):
    self.logger.info(f"[Reader] Getting content from a link: {link}...")
    try:
      result = summarize(link, self.model)
      self.logger.info(f"[Reader] Content from {link} is retrieved.")
      return result
    except Exception as e:
      self.logger.error(f"[Reader] Failed to load {link}: {e}")
      return None
