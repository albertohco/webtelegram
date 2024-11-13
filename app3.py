import requests
from bs4 import BeautifulSoup
import time


def featch_page(url):
    response = requests.get(url)
    return response.text


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_name = soup.find('h1', class_='ui-pdp-title').get_text()
    prices: list = soup.find_all('span', class_='andes-money-amount__fraction')
    old_price: int = int(prices[0].get_text().replace('.', ''))
    new_price: int = int(prices[1].get_text().replace('.', ''))
    installment_price: int = int(prices[2].get_text().replace('.', ''))
    return {
        'product_name': product_name,
        'old_price': old_price,
        'new_price': new_price,
        'installment_price': installment_price,
    }


if __name__ == "__main__":
    while True:
        url1 = "https://www.mercadolivre.com.br/apple-iphone-16-pro-1-tb-titnio-preto-distribuidor-autorizado/p/MLB1040287851#polycard_client=search-nordic&wid=MLB5054621110&sid=search&searchVariation=MLB1040287851&position=7&search_layout=stack&type=product&tracking_id=2f09cb15-c0ae-46a4-bc37-83d79de4dc36"
        page_content1 = featch_page(url1)
        produto_info = parse_page(page_content1)
        print(produto_info)
        time.sleep(10)
