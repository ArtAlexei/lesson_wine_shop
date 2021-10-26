import os
from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pandas import read_excel


def main():
    load_dotenv()
    FOUNDATION_YEAR = int(os.getenv('FOUNDATION_YEAR', default=1920))
    PATH_TO_WINES_FILE = os.getenv('PATH_TO_WINES_FILE')

    now_date = datetime.now()
    winery_age = now_date.year - FOUNDATION_YEAR

    wines = read_excel(PATH_TO_WINES_FILE, keep_default_na='')
    wines_dict = wines.to_dict('records')

    wines = defaultdict(list)
    for wine in wines_dict:
        category = wine.pop('Категория')
        wines[category].append(wine)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    rendered_page = template.render(winery_age=winery_age, wines=wines)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
