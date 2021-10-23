from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict
from pandas import read_excel
from datetime import datetime

now = datetime.now()
winery_age = now.year - 1920

excel_df = read_excel('wine3.xlsx', keep_default_na='')
wines_list = excel_df.to_dict('records')

wines_dict = defaultdict(list)
for wine in wines_list:
    category = wine.pop('Категория')
    wines_dict[category].append(wine)

categories = list(wines_dict)
categories.sort()

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
rendered_page = template.render(winery_age=winery_age, wine_dict=wines_dict, categories=categories)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
