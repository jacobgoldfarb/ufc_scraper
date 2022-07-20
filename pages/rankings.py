from __future__ import division
from bs4 import BeautifulSoup

import downloader
from models.ranking import Ranking
from persistence.db import get_database

RANKINGS_URL = "https://www.ufc.com/rankings"

def populate_rankings():
    db = get_database()
    rankings_page = downloader.download(RANKINGS_URL)
    rankings = parse_page_for_rankings(rankings_page)
    db.add_fighter_from_rankings(rankings)

def parse_page_for_rankings(rankings_page):
    groups_html = get_html_by_group(rankings_page)
    rankings = [get_ranking_from_html(html) for html in groups_html]
    return rankings

def get_ranking_from_html(html):
    division_name = html.find_all("h4")[0].text.strip()
    fighter_divs = html.find_all("div", {"class": "views-row"})
    fighters = [fighter_div.text.strip() for fighter_div in fighter_divs]
    ranking = Ranking(division_name, fighters)
    return ranking

def get_html_by_group(rankings_page):
    RELEVANT_CLASS = "view-grouping"
    rankings_html = rankings_page.text
    soup = BeautifulSoup(rankings_html, 'html.parser')
    return soup.find_all("div", {"class": RELEVANT_CLASS})
    