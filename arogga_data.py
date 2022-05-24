from sqlalchemy.orm import sessionmaker
import requests
import csv
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import sys
# import pandas as pd
import openpyxl
# import mysql.connector
import json
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy import insert
import pymysql
import logging

logging.basicConfig(level=logging.DEBUG, filename='/home/trenza/Documents/arogga/logt.log', filemode='w',
                    format="{asctime} {levelname:<8} {message}", style='{',)
# logger = logging.getLogger('ftpuploader')
# hdlr = logging.FileHandler('/home/trenza/Documents/arogga/logt.log')
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr)
# logger.setLevel(logging.INFO)

pymysql.install_as_MySQLdb()
engine = create_engine('mysql://root:@localhost/web_data')
conn = engine.connect()
# metadata = db.MetaData()
meta = MetaData()
products = db.Table('arogga', meta, autoload=True, autoload_with=engine)
db_sku = []
########################################## for count ##############################
Session = sessionmaker(bind=engine)
session = Session()
cnt = session.query(products).count()
# print("Count:", result)
if cnt == 0:
    n = 37000
else:
    s = products.select().limit(1)
    myresult = conn.execute(s)
    for x in myresult:
        db_sku.append(x[0])
        n = x[0]
        n = n-1
# print("n=", n)
sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', options=options)
driver.set_window_size(1920, 1080)
# n = 36629
m = n-20
# print('m= ', m)
# url = [];
url_prefix = "https://www.arogga.com/brand/"
while n > m:
    time.sleep(3)
    # print('n=', n)
#     start_time = time.time()
#     url.append(url_prefix+str(n)+"/")
    url = url_prefix+str(n)+"/"
#     print(n)
    datas = []
    disc = []
    error = []
    u = url
#     for u in url:
    # print(u)
    try:
        status = requests.get(u)
        st_code = status.status_code
        # print(st_code)
        if st_code == 200:
            all_data = dict()
            all_data['product_images'] = ''
            all_data['main_img'] = ''
            all_data['medicine_name'] = ''
            all_data['med_gram'] = ''
            all_data['mtype'] = ''
            all_data['mcompany'] = ''
            all_data['people_view'] = ''
            all_data['generic'] = ''
            all_data['best_price_amount'] = ''
            all_data['previous_price_amount'] = ''
            all_data['cart'] = ''
            all_data['offer_title'] = ''
            all_data['additional_offers'] = ''
            all_data['other_desciption'] = ''
            all_data['alternative_brands'] = ''
            all_data['product_references'] = ''
            all_data['disclaimer'] = ''
            driver.get(u)
            r = driver.page_source
            soup = BeautifulSoup(r, "html.parser")
            all_data['url'] = u
#                 print(all_data['url'])
#                 break;
            data_sku = json.loads(
                soup.find('script', type="application/ld+json").text)
            all_data['sku'] = data_sku['sku']
            sku = data_sku['sku']
            sk = int(sku)
            data_cat_id = json.loads(
                soup.find('script', id="__NEXT_DATA__").text)
            all_data['cat_id'] = data_cat_id["props"]["pageProps"]["product"]["data"]["medicine"]["cat_id"]
            img_arr = []
        #       ########################## selector image #######################
            sdiv_img = soup.find('div', {'class': 'selectors'})
            for simg in sdiv_img.find_all('a'):
                img_arr.append(simg.get('href'))
            all_data['product_images'] = img_arr

        #        ########################## main image ###########################
            main_img = soup.find('div', {'class': 'updateClass'})
            all_data['main_img'] = main_img.a['href']

        #             ########################## med name ###########################
            for med_name in soup.find_all('h1', {'class': 'MuiTypography-root jss2 MuiTypography-h1'}):
                for mgram in med_name.find_all('span', {'class': 'jss3'}):
                    all_data['med_gram'] = mgram.text
                med_name.find('span').extract()
                all_data['medicine_name'] = med_name.text

        #       ############# med type and company ###########################
            med = soup.find_all(
                'div', {'class': 'MuiGrid-root jss23 MuiGrid-item MuiGrid-grid-lg-6'})
            count = 0
            y = []
            for med in soup.find_all('h6'):
                x = med.text
                y.append(x)
                if len(y) <= 1:                   
                    all_data['mtype'] = ''
                    all_data['mcompany'] = ''
                else:
                    all_data['mtype'] = y[0]
                    all_data['mcompany'] = y[1]
            # all_data['mtype'] = y[0]
            # all_data['mcompany'] = y[1]

        #       ########################### Generic Name #############################
            for span_search in soup.find_all('div', {'class': 'MuiGrid-root jss23 MuiGrid-item MuiGrid-grid-lg-6'}):
                span_text_jss23 = []
                for z in span_search.find_all('div'):
                    span_text = z.text
                    span_text_jss23.append(span_text)
                for d in span_search.find_all('div', {'class': 'jss6'}):
                    for dd in d.find_all('div', {'class': 'jss7'}):
                        for pv in dd.find_all('span'):
                            all_data['people_view'] = pv.text
            all_data['generic'] = span_text_jss23[1]

        #       ########################## med price ###########################
            med_price = soup.find_all('div', {'class': 'jss8'})
            price = []
            for med_price in soup.find_all('div', {'class': 'jss8'}):
                link = med_price.find_all('div')
                for l in link:
                    price.append(l.text)

            if len(price) > 2:
                all_data['best_price_title'] = price[0]
                all_data['best_price_amount'] = price[1]
                all_data['previous_price_title'] = price[2]
                all_data['previous_price_amount'] = price[3]
            else:
                all_data['best_price_title'] = price[0]
                all_data['best_price_amount'] = price[1]
                all_data['previous_price_title'] = 0
                all_data['previous_price_amount'] = 0

        #             ########################## cart ###########################
            all_data['cart'] = soup.find(
                'span', {'class': 'MuiButton-label'}).text

        #             ########################## offers ###########################
            offers = dict()
            offer_title = soup.find('h2', {'class': 'jss11'}).text
            all_data['offer_title'] = offer_title
            offer_details = []
            for all_offers in soup.find_all('div', {'class': 'jss14 jss22'}):
                offer_details.append(all_offers.text)
            all_data['additional_offers'] = offer_details

        #       ########################## other description ###########################
            for other in soup.find_all('div', {'class': 'jss90'}):
                other_desc = other.find_all('div', {'class': 'jss69'})
            for ot in other_desc:
                all_data['other_desciption'] = ot
#                     print(all_data['other_desciption'])
#                         for ot_li in ot.find_all('li'):
#                             other_Des = str(ot_li)
#                             other_Des = other_Des.encode("utf-8")
# #                             print(other_Des)
#                             other = other_Des.replace("/"," ")
#                             other_Des = preg_replace('/[0-9\@\.\;\" "]+/', '', other_Des)
#                         print(other)

        #             ########################## disclaimer ###########################
            disc.append(soup.find('div', {'class': 'jss89'}).p.text)
            all_data['disclaimer'] = disc[0]
        #             ########################## alternative products ###########################
            product_references = []
            for alt in soup.find_all('div', {'class': 'jss69'}):
                for brn in alt.find_all('div', {'class': 'jss93'}):
                    all_data['alternative_brands'] = brn
    #                     print(all_data['alternative_brands'])
                    for nav_elem in brn.find_all('div', {'class': 'MuiButtonBase-root MuiListItem-root jss133 MuiListItem-gutters MuiListItem-button'}):
                        for pro_ref in nav_elem.find_all('a'):
                            product_references.append(pro_ref.get('href'))
            all_data['product_references'] = product_references

            datas.append(all_data)
    #             print(all_data['alternative_brands'])
        #             ############################# db duplicate check, insert #################################
            if all_data['sku'] not in db_sku:
                #                     print(all_data['alternative_brands'])
                all_data['product_images'] = str(all_data['product_images'])
                all_data['main_img'] = str(all_data['main_img'])
                offer_details = str(offer_details)
                all_data['other_desciption'] = str(
                    all_data['other_desciption'])
#                     print(all_data['other_desciption'])
                all_data['alternative_brands'] = str(
                    all_data['alternative_brands'])
#                     print(all_data['alternative_brands'])
                all_data['product_references'] = str(
                    all_data['product_references'])
                all_data['disclaimer'] = str(all_data['disclaimer'])
#                     print(type(offer_details))
#                     print(str(all_data['cart']))
#                     print(str(all_data['medicine_name']),str(all_data['med_gram']),str(all_data['mtype']),
#                          str(all_data['mcompany']),str(all_data['people_view']), str(all_data['generic']),str(all_data['best_price_amount']),)
#                     ins = products.insert().values(sku = all_data['sku'],other_desciption=str(all_data['other_desciption']))
#                     ins = products.insert().values(sku = all_data['sku'], url = all_data['url'],
#                                                    product_images=all_data['product_images'],
#                                                    main_img=all_data['main_img'],
#                                                    medicine_name=str(all_data['medicine_name']),
#                                                    medicine_weight=str(all_data['med_gram']),
#                                                    medicine_type=str(all_data['mtype']),
#                                                    medicine_company=str(all_data['mcompany']),
#                                                    people_view=str(all_data['people_view']),
#                                                    generic=str(all_data['generic']),
#                                                    best_price_amount=str(all_data['best_price_amount']),
#                                                    previous_price_amount=str(all_data['previous_price_amount']),
#                                                    cart=str(all_data['cart']),
#                                                    offer_title=str(all_data['offer_title']),
#                                                    additional_offers=str(offer_details),
#                                                    other_desciption=str(all_data['other_desciption'],
#                                                    alternative_brands=all_data['alternative_brands'],
#                                                    product_references=all_data['product_references'],
#                                                    disclaimer=all_data['disclaimer'],
#                                                    cat_id=all_data['cat_id'],status=1)
#                                                   )
                ins = products.insert().values(sku=all_data['sku'], url=all_data['url'],
                                               product_images=all_data['product_images'], main_img=all_data['main_img'],
                                               medicine_name=str(all_data['medicine_name']), medicine_weight=str(all_data['med_gram']),
                                               medicine_type=str(all_data['mtype']), medicine_company=str(all_data['mcompany']),
                                               people_view=str(all_data['people_view']), generic=str(all_data['generic']),
                                               best_price_amount=str(
                                                   all_data['best_price_amount']),
                                               previous_price_amount=str(
                                                   all_data['previous_price_amount']),
                                               cart=str(all_data['cart']), offer_title=str(all_data['offer_title']),
                                               additional_offers=str(offer_details), other_desciption=str(all_data['other_desciption']),
                                               alternative_brands=all_data['alternative_brands'],
                                               product_references=all_data['product_references'],
                                               disclaimer=all_data['disclaimer'], cat_id=all_data['cat_id'], status=1)
#                     print(ins)
                # logging.debug('log1')
                reslt = conn.execute(ins)
                # logging.debug('debug')
                # logging.info('info')
                # print('log')
                logging.info(str(n) + " inserted successfully")
                db_sku.append(all_data['sku'])
    #                 print(reslt)
        elif st_code == 404:
            ins = products.insert().values(sku=n, status=0)
            reslt = conn.execute(ins)
            # logging.basicConfig(level=logging.DEBUG, filename='log_arr.log', filemode='w',
            #                     format="{asctime} {levelname:<8} {message}", style='{',)
            logging.warning(str(n) + " status 404 inserted")
            db_sku.append(n)
#             break
    #         end_time = time.time()
#             elif st_code == 308:
#                 ins = products.insert().values(sku=n, status = 0)
#                 reslt = conn.execute(ins)
#                 db_sku.append(n)
#                 break
        else:
            error.append(n)
            break
    except:
        #         print(1)
        ins = products.insert().values(sku=n, status=0)
        reslt = conn.execute(ins)
        # logging.basicConfig(filename='log_arr.log', filemode='w',
        #                     format='%(name)s - %(levelname)s - %(message)s')
        logging.error(sys.exc_info()[0])
        logging.info(str(n) + " error")
        db_sku.append(n)
#         continue
    n = n-1   
driver.close()
driver.quit()

#     time_diff = end_time - start_time
#     print(time_diff)
# print(error)
