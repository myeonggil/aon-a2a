import requests

from dataclasses import dataclass

from aon_a2a.configs import config


CLIENT_ID = config["NAVER_NEWS_CLIENT_ID"]
CLIENT_SECRET = config["NAVER_NEWS_CLIENT_SECRET"]
NAVER_DOMAIN = config["NAVER_NEWS_DOMAIN"]


@dataclass
class SearchRequest:
    query: str = "삼성전자"
    display: int = 10
    start: int = 1
    sort: str = "sim"   # sim is accuracy, date is sort by recent date


@dataclass
class SearchItem:
    description: str
    link: str
    originallink: str
    pubDate: str
    title: str


@dataclass
class SearchResponse:
    display: int
    items: list[SearchItem]


def parse_searched_news(news: SearchResponse):
    pass


def search_news():
    query = "삼성전자"
    url = f"{NAVER_DOMAIN}query={query}&display=10&start=1&sort=sim"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    res = requests.get(
        url=url,
        headers=headers
    )
    news: SearchResponse = None
    try:
        results = res.json()
        display = results["display"]
        items = results["items"]
        search_items: list[SearchItem] = []
        for item in items:
            search_item = SearchItem(
                description=item["description"],
                link=item["link"],
                originallink=item["originallink"],
                pubDate=item["pubDate"],
                title=item["title"]
            )
            search_items.append(search_item)
        news = SearchResponse(
            display=display,
            items=search_items
        )
    except Exception as err:
        print(err)
    return news
