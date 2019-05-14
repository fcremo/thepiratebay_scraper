#!/usr/bin/env python
import sys
import urllib.parse
from functools import lru_cache

import transmissionrpc
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@lru_cache()
def get_results_page(query, page):
    query = urllib.parse.quote_plus(query)
    URL = "https://thepiratebay.org/search/{}/{}/99/0".format(query, page)
    logger.info("Getting page {} for \"{}\"", page, query)
    logger.debug("Getting {}", URL)
    driver.get(URL)

    pages = len(driver.find_elements_by_css_selector("#content > div:nth-child(3) > a"))
    elements = driver.find_elements_by_css_selector("#searchResult > tbody > tr > td:nth-child(2) > a ")
    magnets = [e.get_property("href") for e in elements]

    return magnets, pages


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("headless")
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/74.0.3729.108 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')

    if len(sys.argv) < 2:
        logger.error("Usage: scraper.py <query>")
        exit()

    query = " ".join(sys.argv[1:])

    driver = webdriver.Chrome(options=chrome_options)
    logger.info("Initialized chrome headless")

    tc = transmissionrpc.Client('localhost', port=9091)
    logger.info("Initialized transmissionrpc client")

    page = 0

    _, pages = get_results_page(query, page)

    logger.info("Got {} pages", pages)

    magnets = []
    for page in range(pages - 1):
        logger.info("Getting page {}", page)
        page_magnets, _ = get_results_page(query, page)
        magnets = magnets + page_magnets

    driver.close()

    logger.info("Got {} magnets", len(magnets))

    for magnet in magnets:
        try:
            tc.add_torrent(magnet)
        except Exception as e:
            logger.exception(e)

    logger.info("Added all torrents!")


