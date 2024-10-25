from flask import Flask, jsonify

app = Flask(__name__)


from bs4 import BeautifulSoup
import requests


def get_currency(in_currency, out_currency):
  url = f'https://www.x-rates.com/calculator/?from={in_currency}&to={out_currency}&amount=1'
  # grabs source code
  content = requests.get(url).text
  # print(content)

  #parse source code for just info you want

  # this creates a beautiful soup object so then you can actually parse
  soup = BeautifulSoup(content, 'html.parser')
  #query through the object of what you want, and only the text not the whole element
  rate = soup.find('span', class_="ccOutputRslt").get_text()
  rate = float(rate[0:-4])
  return rate



@app.route('/')
def home():
  return '<h1> Currency api</h1>  <p>Example URL: /api/v1/usd-eur</p>'


@app.route('/api/v1/<in_cur>-<out_cur>')
def api(in_cur, out_cur):
  rate = get_currency(in_cur, out_cur)
  result_dic = { 'input currency': in_cur, 'output currency': out_cur, 'rate': rate}
  return jsonify(result_dic)

app.run()
