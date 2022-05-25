from datetime import date
import logging
import time
import requests
from scrapper_boilerplate import dataToCSV
from scrapper_boilerplate.parser_handler import remove_duplicates_on_list
import logging


def shopee_scrapper_search(keyword):
    """
    This function is used to search for products on shopee.
    args:
        keyword: the keyword to search for.
    """

    request = requests.get(f'https://shopee.com.br/api/v4/search/search_items?by=relevancy&keyword=carregadores&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2')

    if request.status_code != 200:
        print('Error:', request.status_code)
        return

    data = request.json()
    store_ids = []

    for item in data["items"]:
        store_ids.append(item['item_basic']['shopid'])

    store_ids = remove_duplicates_on_list(store_ids)

    [ print(store_id) for store_id in store_ids ]
    print('Total:', len(store_ids))

    return store_ids
    #define the number of ads published.



def shopee_scrapper_sellers(seller_shopee_id):
    #print date to help users to track down when the file was generated.
    
    logging.info('Starting shopee crawler...')
    data = date.today()
    current_day = str(data.strftime("%d/%m/%Y")).replace('/', '-')
    data1 = date.today()

    #asks for seller id.
    seller_shopee_id = str(seller_shopee_id) #input('Type in the seller id: \n')

    logging.info(f'> [{seller_shopee_id}] consulting the api...')
    url_api_request = 'https://shopee.com.br/api/v4/recommend/recommend?bundle=shop_page_product_tab_main&limit=999&offset=0&section=shop_page_product_tab_main_sec&shopid=' + seller_shopee_id
    r = requests.get(url_api_request)

    #define the number of ads published.
    logging.info(f'> [{seller_shopee_id}] defining the number of ads...')
    num_ads = (r.json()['data']['sections'][0]['data']['item'])
    list_size = len(num_ads)

    logging.info(f'> [{seller_shopee_id}] defining the list of products...')
    #creates a while statement using the number of ads created. Since the (index) json file stars with 0, the while statment starts with -1. 
    creat_while = -1
    while creat_while < list_size - 1:
        creat_while += 1
        
        product = {}
        #store the information displayed inside the json file. It's possible to extract even more data, you only need to add the exact json's children path you're interested in. The scrapper will sleep for 1 second and then get the next ad's information.
        product['ad_id'] = (r.json()['data']['sections'][0]['data']['item'][creat_while]['itemid'])
        product['title'] = (r.json()['data']['sections'][0]['data']['item'][creat_while]['name'])
        product['stock'] = (r.json()['data']['sections'][0]['data']['item'][creat_while]['stock'])
        product['sales'] = (r.json()['data']['sections'][0]['data']['item'][creat_while]['historical_sold'])
        product['likes'] = (r.json()['data']['sections'][0]['data']['item'][creat_while]['liked_count'])
        product['views'] = (r.json()['data']['sections'][0]['data']['item'][creat_while]['view_count'])
        product['price'] = (r.json()['data']['sections'][0]['data']['item'][creat_while]['price'])
        product['rating'] = (r.json()['data']['sections'][0]['data']['item'][creat_while]['item_rating']['rating_count'][0])
        time.sleep(1)

        #you've to set where you wanna save the csv file. If you run the code without changing the directory settings, you'll get no data.
        compressed_data = { key: [value] for key, value in product.items() }
        dataToCSV(compressed_data, f"data/{current_day}-shopee.csv")

    print('The scrapper is done. Your CSV file is ready!')
