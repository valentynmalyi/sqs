import requests
from bs4 import BeautifulSoup
import os

headers = {'User-Agent': "*"}


def get_info(url: str, proxy: dict = None, timeout=60) -> dict:
    proxy = proxy or {}
    response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
    soup = BeautifulSoup(response.content, features="lxml")

    title_ = soup.select("#productTitle")
    if len(title_):
        title = title_[0].get_text().strip()
    else:
        title = None

    stars_ = soup.find_all('i', attrs={'data-hook': 'average-star-rating'})
    if len(stars_):
        stars = stars_[0].get_text().strip()
    else:
        stars = None
    reviews = []

    for div_tags in soup.find_all('div', attrs={'data-hook': 'review-collapsed'}):
        review = div_tags.text.strip()
        reviews.append(review)

    return {"title": title, "stars": stars, "reviews": reviews}


if __name__ == '__main__':
    urls = ["https://www.amazon.com/dp/B079RQJGVH",
            "https://www.amazon.com/Amazon-Essentials-Womens-Crewneck-Sweater/dp/B079RF5S8T",
            "https://www.amazon.com/dp/B07XZWYNGF", "https://www.amazon.com/dp/B07R63BC12"]
    for url in urls:
        print(get_info(url=url, proxy={'https': "101.108.108.213:8080"}))
