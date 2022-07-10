from os import getenv, path
from pandas import DataFrame
from datetime import date, timedelta
from re import compile
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

DATA_PATH = path.join(path.dirname(__file__), "../../data")
WEB_DRIVER = getenv("WEB_DRIVER")
_driver_service = Service(WEB_DRIVER)
_options = Options()
_options.add_argument("--headless")
_driver = webdriver.Firefox(options=_options, service=_driver_service)


class WSJCrawler:
    def __init__(self, max_headlines=20):
        self.driver = _driver
        self.max_headlines = max_headlines
        self.headlines = {}

    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            print("Webdriver already closed")

    def crawl(self, start: date, end: date):
        """
        Grabs the headlines from the pages by the specified date.
        Only works while WSJ website uses current methods to index archived articles
        (/year/month/day) and styled with current classes

        Assumes installation of geckodriver (Firefox) in path or in env as WEB_DRIVER

        start: date\t the date to start searching from
        end: date\t the date to stop at
        returns: list\t List of headlines html tags
        """
        headlines = {}
        while start <= end:
            print(f"Getting articles for {start.strftime('%Y-%m-%d')}")
            page_source = self._crawl(start)
            if page_source is not None:
                headlines[
                    start.strftime("%Y-%m-%d")
                ] = self._extract_headlines_from_source(page_source)
            start = start + timedelta(1)
        self.headlines = headlines
        return headlines

    def save_headlines(self, name: str):
        if self.headlines is None:
            print("There are no headlines to save")
            return
        d = dict()
        for key, values in self.headlines.items():
            articles = values[: self.max_headlines]
            while len(articles) < self.max_headlines:
                articles.append("")
            d[key] = articles
        df = DataFrame.from_dict(d)
        file_path = DATA_PATH + f"/{name}"
        df.to_csv(file_path, index=False)

    def _extract_headlines_from_source(self, page_source: str):
        """
        Returns a list of strings of headlines from the page source

        page_source: str\t HTML page source
        """
        soup = BeautifulSoup(page_source, "html.parser")
        regex = compile(".*headlineText.*")
        spans = soup.find_all("span", class_=regex)
        return [tag.string for tag in spans]

    def _crawl(self, start: date):
        url = self._url_template(
            start.strftime("%Y"), start.strftime("%m"), start.strftime("%d")
        )
        page_source = None
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(1)
            page_source = self.driver.page_source
        except Exception:
            print(f"Error: Could not get the page source from the url: {url}")
        return page_source

    def _url_template(self, year, month, day):
        """
        Returns the URL to get the headlines from the given date

        year: str\t year
        month: str\t month
        day: str\t day
        returns: str\t url for grabbing the headlines
        """
        url_template = f"https://www.wsj.com/news/archive/{year}/{month}/{day}"
        return url_template
