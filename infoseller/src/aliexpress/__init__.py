import logging
from scrapper_boilerplate import dataToCSV


def aliexpress_crawler(request):
    request.html.render(timeout=30, scrolldown=10, sleep=5)
    html = request.html
    container = html.find('div.JIIxO', first=True)

    products = container.find('a')
    if len(products) == 0:
        return

    for product in products:
        try:
            title = product.find('h1', first=True).text
            price = product.find('.mGXnE._37W_B', first=True).text
            try:
                fullPrice = product.find('._11_8K span', first=True).text
            
            except AttributeError:
                fullPrice = '-'

            try:
                discount = product.find('._2LVIV', first=True).text
            
            except AttributeError:
                discount = '-'

            try:
                sold = product.find('._1kNf9', first=True).text
            
            except AttributeError:
                sold = '-'

            try:
                rate = product.find('.eXPaM', first=True).text
            
            except AttributeError:
                rate = '-'

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
            return True

        except AttributeError:
            logging.error('Não foi possível obter os dados...')
        
    