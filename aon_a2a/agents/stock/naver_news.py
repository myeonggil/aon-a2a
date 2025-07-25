import requests

from dataclasses import dataclass

from aon_a2a.configs import config


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
    for item in news.items:
        print(item.title.replace(
            "<b>", "").replace(
            "</b>", "").replace(
            "&quot;", "\"").replace(
            "&lt;", "<").replace(
            "&gt;", ">")
        )
        print(item.description.replace(
            "<b>", "").replace(
            "</b>", "").replace(
            "&quot;", "\"").replace(
            "&lt;", "<").replace(
            "&gt;", ">")
        )


def search_news(query: str):
    headers = {
        "X-Naver-Client-Id": config["NAVER_NEWS_CLIENT_ID"],
        "X-Naver-Client-Secret": config["NAVER_NEWS_CLIENT_SECRET"]
    }
    params = {
        "query": query,
        "display": 10,
        "start": 1,
        "sort": "sim"
    }
    res = requests.get(
        url=config["NAVER_NEWS_DOMAIN"],
        headers=headers,
        params=params
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
