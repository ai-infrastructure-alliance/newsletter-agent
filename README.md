# AIIA Newsletter Agent

This is an intelligent AI-driven assistant that simplifies writing newsletters.

The workflow is as follows:

* Over the week (or the month) you collect links to interesting articles, papers, projects, etc. 
in a Telegram group (see [new-bot](https://github.com/ai-infrastructure-alliance/news-bot)) 
or directly in an Airtable base.
* The background worker (enricher) reads the links and enriches them with the title and summary.
* When you want to get a newsletter draft, you use the web interface to select the news you want 
to include in the newsletter and generate the text.
* As a last step, you should review the text and publish it on a platform of choice.

This code is tailored towards AI-related newsletters, but it can be easily adapted to other domains.
You just need to edit the prompts of agents in the `agents` folder accordingly.

## How to use it

### Setup the AirTable base

Unfortunately, AirTable doesn't provide an API to create a base, so you'll have to do it manually.

1. Create a new [AirTable](https://airtable.com/) base
2. Create an AirTable table `Weekly newsletter` in that base with the following fields:
    - `URL` (Primary, URL)
    - `Type` (Single select: 'post', 'paper', 'project', 'youtube', 'twitter', 'reddit')
    - `Title` (Single line text)
    - `Summary` (Long text)
    - `Comment` (Long text)
3. If you prefer to call your table differently, change the name in the `news_bot_runner.py` file.

### Setup the project

1. If you plan to test it locally, create a `.env` file with the following content:
```
OPEN_AI_KEY=<your OpenAI API key>
AIRTABLE_API_KEY=<API key in Airtable>
BASE_ID=<Base ID in Airtable; to get it, click Help | API Documentation in your base>
```

2. The project is designed to be deployed on Heroku. Add the corresponding environment variables to your Heroku app.
See the [DEV_NOTES.md](DEV_NOTES.md) file for more details on how to deploy it on Heroku.

### Run the background worker locally

```
python src/enrich_runner.py
```

### Run the web interface locally

```
streamlit run src/weekly_newsletter_ui.py
```

## Models

* Enrichment (i.e. reading and summarizing articles) uses GPT-3.5 by default. You can replace it with GPT-4 in [enrich_runner.py](src/enrich_runner.py), but it's not recommended: the quality of summarization is pretty much the same, but GPT-4 is much slower.
* Newsletter writer uses GPT-4 by default. You can replace it with GPT-3.5 in [weekly_newsletter_ui.py](src/weekly_newsletter_ui.py). GPT-4 is generally better for complex propmts like the ones used for writing a draft. 
