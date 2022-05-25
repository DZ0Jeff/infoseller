from src.aliexpress import aliexpress_crawler
from requests_html import HTMLSession


def aliexpress_controller():
    session = HTMLSession()
    page =  1
    while True: 
        try:
            request = session.get(f'https://pt.aliexpress.com/category/201000006/computer-office.html?trafficChannel=main&catName=computer-office&CatId=201000006&ltype=wholesale&SortType=default&page={page}')
            if not aliexpress_crawler(request):
                break
            
            else:
                page += 1

        except KeyboardInterrupt:
            break