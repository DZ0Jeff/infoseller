from src.shopee import shopee_scrapper_search, shopee_scrapper_sellers
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename='status/debug.log', filemode='a')


def main():
    store_ids = shopee_scrapper_search('carregadores')
    for store_id in store_ids:
        shopee_scrapper_sellers(store_id)
        

if __name__ == '__main__':
    print('Starting infoseller...')
    main()
    print('Done!')
