import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import sqlite3


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
    timestamp = time.strftime('%Y-%m-%d %H:%m:%S')
    return {
        'product_name': product_name,
        'old_price': old_price,
        'new_price': new_price,
        'installment_price': installment_price,
        'timestamp': timestamp
    }

def save_to_dataframe(product_info, df):
    new_row = pd.DataFrame([product_info])
    df = pd.concat([df, new_row], ignore_index=True)
    return df

def create_connection(db_name='iphone_prices.db'):
    """Cria uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(db_name)
    return conn

def setup_database(conn):
    """Cria a tabela de preços se ela não existir."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            old_price INTEGER,
            new_price INTEGER,
            installment_price INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()

def save_to_database(conn, data):
    """Salva uma linha de dados no banco de dados SQLite usando pandas."""
    df = pd.DataFrame([data])  # Converte o dicionário em um DataFrame de uma linha
    df.to_sql('prices', conn, if_exists='append', index=False)  # Salva no banco de dados

if __name__ == "__main__":
    
    # Configuração do banco de dados
    conn = create_connection()
    setup_database(conn)
    
    while True:
        url1 = "https://www.mercadolivre.com.br/apple-iphone-16-pro-1-tb-titnio-preto-distribuidor-autorizado/p/MLB1040287851#polycard_client=search-nordic&wid=MLB5054621110&sid=search&searchVariation=MLB1040287851&position=7&search_layout=stack&type=product&tracking_id=2f09cb15-c0ae-46a4-bc37-83d79de4dc36"
        page_content1 = featch_page(url1)
        produto_info = parse_page(page_content1)
    
        # Salva os dados no banco de dados SQLite
        save_to_database(conn, produto_info)
        print("Dados salvos no banco:", produto_info)
        
        # Aguarda 10 segundos antes da próxima execução
        time.sleep(10)

    # Fecha a conexão com o banco de dados
    conn.close()
