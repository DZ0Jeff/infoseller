from requests_html import HTMLSession
from scrapper_boilerplate import dataToCSV
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename='status/debug.log', filemode='a')


def find_tag(tag, html, error_msg='Não localizado...'):
    try:
        return html.find(tag, first=True).text
    
    except:
        return error_msg


def crawler(request):
    request.html.render(timeout=30, scrolldown=10, sleep=1)
    container = request.html.find('div.JIIxO', first=True)

    for product in container.find('a'):
        try:
            title = product.find('h1', first=True).text
            price = product.find('.mGXnE._37W_B', first=True).text
            fullPrice = product.find('._11_8K span', first=True).text
            discount = product.find('._2LVIV', first=True).text
            sold = product.find('._1kNf9', first=True).text
            rate = product.find('.eXPaM', first=True).text

            data = {
                'Nome': title,
                'Preço': price,
                'Preço original': fullPrice,
                'Desconto': discount,
                'Vendidos': sold,
                'Classificação': rate
            } 

            print('\n')
            [print(f"{key}: {content}") for key, content in data.items()]
            compressed_data = { key: [value] for key, value in data.items() if value != 'Não localizado...' }
            dataToCSV(compressed_data, 'aliexpress.csv')

        except AttributeError:
            logging.error('Não foi possível obter os dados...')
    

def main():
    session = HTMLSession()
    request = session.get('https://pt.aliexpress.com/category/201000006/computer-office.html')
    crawler(request)


if __name__ == '__main__':
    main()
