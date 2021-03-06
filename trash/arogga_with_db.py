{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 25,
   "id": "de11fff0",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "m=  36628\n",
      "\n",
      "INSERT INTO arogga (sku, url, product_images, main_img, medicine_name, medicine_weight, medicine_type, medicine_company, people_view, generic, best_price_amount, previous_price_amount, cart, offer_title, additional_offers, other_desciption, alternative_brands, product_references, disclaimer, cat_id, status) VALUES (:sku, :url, :product_images, :main_img, :medicine_name, :medicine_weight, :medicine_type, :medicine_company, :people_view, :generic, :best_price_amount, :previous_price_amount, :cart, :offer_title, :additional_offers, :other_desciption, :alternative_brands, :product_references, :disclaimer, :cat_id, :status)\n"
     ]
    }
   ],
   "source": [
    "import requests\n",
    "import csv\n",
    "import time\n",
    "from selenium import webdriver\n",
    "from bs4 import BeautifulSoup\n",
    "import sys\n",
    "import pandas as pd\n",
    "import openpyxl\n",
    "# import mysql.connector\n",
    "import json\n",
    "import sqlalchemy as db\n",
    "from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String\n",
    "from sqlalchemy import insert\n",
    "import pymysql\n",
    "\n",
    "pymysql.install_as_MySQLdb()\n",
    "engine = create_engine('mysql://root:@localhost/web_data')\n",
    "conn = engine.connect()\n",
    "# metadata = db.MetaData()\n",
    "meta = MetaData()\n",
    "products = db.Table('arogga', meta, autoload=True, autoload_with=engine)\n",
    "db_sku = [];\n",
    "########################################## for count ##############################\n",
    "from sqlalchemy.orm import sessionmaker\n",
    "Session = sessionmaker(bind = engine)\n",
    "session = Session()\n",
    "cnt = session.query(products).count() \n",
    "# print(\"Count:\", result)\n",
    "if cnt == 0:\n",
    "    n = 37000\n",
    "else:    \n",
    "    s = products.select().limit(1)\n",
    "    myresult = conn.execute(s)\n",
    "    for x in myresult:\n",
    "        db_sku.append(x[0])\n",
    "        n = x[0]\n",
    "        n= n-1\n",
    "# print(\"n=\", n)\n",
    "sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')\n",
    "\n",
    "options = webdriver.ChromeOptions()\n",
    "options.add_argument('--headless')\n",
    "options.add_argument('--no-sandbox')\n",
    "options.add_argument('--disable-dev-shm-usage')\n",
    "driver = webdriver.Chrome('chromedriver',options=options)\n",
    "driver.set_window_size(1920, 1080)\n",
    "# n = 36629\n",
    "m = n-1 \n",
    "print('m= ', m)\n",
    "url = [];\n",
    "url_prefix = \"https://www.arogga.com/brand/\";    \n",
    "while n > m:\n",
    "    time.sleep(3)\n",
    "#     print('while')\n",
    "    start_time = time.time()\n",
    "    url.append(url_prefix+str(n)+\"/\") \n",
    "#     print(n)\n",
    "    datas = [];\n",
    "    disc = [];\n",
    "    error = [];\n",
    "    for u in url:\n",
    "#         print(u)\n",
    "        try:\n",
    "            status = requests.get(u)        \n",
    "            st_code = status.status_code        \n",
    "            print(st_code)                               \n",
    "            if st_code == 200:            \n",
    "                all_data = dict()\n",
    "                all_data['product_images'] = ''\n",
    "                all_data['main_img'] = ''\n",
    "                all_data['medicine_name'] = ''\n",
    "                all_data['med_gram'] = ''\n",
    "                all_data['mtype']  = ''\n",
    "                all_data['mcompany'] = ''\n",
    "                all_data['people_view'] = ''\n",
    "                all_data['generic'] = ''\n",
    "                all_data['best_price_amount'] = ''\n",
    "                all_data['previous_price_amount'] = ''\n",
    "                all_data['cart'] = ''\n",
    "                all_data['offer_title'] = ''\n",
    "                all_data['additional_offers'] = ''\n",
    "                all_data['other_desciption'] = ''\n",
    "                all_data['alternative_brands'] = ''\n",
    "                all_data['product_references'] = ''\n",
    "                all_data['disclaimer'] = ''\n",
    "                driver.get(u)\n",
    "                r = driver.page_source\n",
    "                soup = BeautifulSoup(r, \"html.parser\")             \n",
    "                all_data['url'] = u\n",
    "#                 print(all_data['url'])\n",
    "#                 break;\n",
    "                data_sku = json.loads(soup.find('script', type=\"application/ld+json\").text)\n",
    "                all_data['sku'] = data_sku['sku']\n",
    "                sku = data_sku['sku']\n",
    "                sk = int(sku)\n",
    "                data_cat_id = json.loads(soup.find('script', id=\"__NEXT_DATA__\").text)\n",
    "                all_data['cat_id'] = data_cat_id[\"props\"][\"pageProps\"][\"product\"][\"data\"][\"medicine\"][\"cat_id\"]\n",
    "                img_arr =[]\n",
    "        #       ########################## selector image #######################\n",
    "                sdiv_img = soup.find('div', {'class': 'selectors'})\n",
    "                for simg in sdiv_img.find_all('a'):\n",
    "                    img_arr.append(simg.get('href'))  \n",
    "                all_data['product_images'] = img_arr\n",
    "\n",
    "        #        ########################## main image ###########################\n",
    "                main_img = soup.find('div', {'class' : 'updateClass'})\n",
    "                all_data['main_img'] = main_img.a['href']\n",
    "\n",
    "        #             ########################## med name ###########################\n",
    "                for med_name in soup.find_all('h1', {'class': 'MuiTypography-root jss2 MuiTypography-h1'}):\n",
    "                    for mgram in med_name.find_all('span', {'class':'jss3'}):\n",
    "                        all_data['med_gram'] = mgram.text\n",
    "                    med_name.find('span').extract()\n",
    "                    all_data['medicine_name'] = med_name.text\n",
    "\n",
    "        #       ############# med type and company ###########################\n",
    "                med = soup.find_all('div', {'class': 'MuiGrid-root jss23 MuiGrid-item MuiGrid-grid-lg-6'})\n",
    "                count = 0\n",
    "                y = []\n",
    "                for med in soup.find_all('h6'):\n",
    "                    x = med.text\n",
    "                    y.append(x)\n",
    "                all_data['mtype'] = y[0];\n",
    "                all_data['mcompany'] = y[1];\n",
    "\n",
    "        #       ########################### Generic Name #############################\n",
    "                for span_search in soup.find_all('div',{'class':'MuiGrid-root jss23 MuiGrid-item MuiGrid-grid-lg-6'}):\n",
    "                    span_text_jss23 = []\n",
    "                    for z in span_search.find_all('div'):\n",
    "                        span_text = z.text\n",
    "                        span_text_jss23.append(span_text)\n",
    "                    for d in span_search.find_all('div', {'class':'jss6'}):\n",
    "                            for dd in d.find_all('div', {'class':'jss7'}):\n",
    "                                for pv in dd.find_all('span'):\n",
    "                                    all_data['people_view'] = pv.text\n",
    "                all_data['generic'] = span_text_jss23[1]\n",
    "\n",
    "        #       ########################## med price ###########################\n",
    "                med_price = soup.find_all('div', {'class':'jss8'})\n",
    "                price = []\n",
    "                for med_price in soup.find_all('div', {'class':'jss8'}):\n",
    "                    link = med_price.find_all('div')\n",
    "                    for l in link:\n",
    "                        price.append(l.text)\n",
    "\n",
    "                if len(price) > 2:\n",
    "                    all_data['best_price_title'] = price[0]\n",
    "                    all_data['best_price_amount'] = price[1]\n",
    "                    all_data['previous_price_title'] = price[2]\n",
    "                    all_data['previous_price_amount'] = price[3]\n",
    "                else:\n",
    "                    all_data['best_price_title'] = price[0]\n",
    "                    all_data['best_price_amount'] = price[1]\n",
    "                    all_data['previous_price_title'] = 0\n",
    "                    all_data['previous_price_amount'] = 0\n",
    "\n",
    "        #             ########################## cart ###########################\n",
    "                all_data['cart'] = soup.find('span', {'class': 'MuiButton-label'}).text\n",
    "\n",
    "        #             ########################## offers ###########################\n",
    "                offers = dict();\n",
    "                offer_title = soup.find('h2', {'class':'jss11'}).text\n",
    "                all_data['offer_title'] = offer_title\n",
    "                offer_details = []\n",
    "                for all_offers in soup.find_all('div', {'class':'jss14 jss22'}):    \n",
    "                    offer_details.append(all_offers.text)\n",
    "                all_data['additional_offers'] = offer_details\n",
    "\n",
    "        #       ########################## other description ###########################\n",
    "                for other in soup.find_all('div', {'class': 'jss90'}):\n",
    "                    other_desc = other.find_all('div', {'class': 'jss69'})\n",
    "                    for ot in other_desc: \n",
    "                        all_data['other_desciption'] = ot;\n",
    "#                     print(all_data['other_desciption'])\n",
    "#                         for ot_li in ot.find_all('li'):\n",
    "#                             other_Des = str(ot_li)\n",
    "#                             other_Des = other_Des.encode(\"utf-8\")\n",
    "# #                             print(other_Des)\n",
    "#                             other = other_Des.replace(\"/\",\" \")\n",
    "#                             other_Des = preg_replace('/[0-9\\@\\.\\;\\\" \"]+/', '', other_Des)\n",
    "#                         print(other)\n",
    "\n",
    "                       \n",
    "        #             ########################## disclaimer ###########################    \n",
    "                disc.append(soup.find('div', {'class':'jss89'}).p.text)\n",
    "                all_data['disclaimer'] = disc[0];\n",
    "        #             ########################## alternative products ###########################\n",
    "                product_references = []\n",
    "                for alt in soup.find_all('div', {'class': 'jss69'}):\n",
    "                    for brn in alt.find_all('div', {'class':'jss93'}):\n",
    "                        all_data['alternative_brands'] = brn    \n",
    "    #                     print(all_data['alternative_brands'])\n",
    "                        for nav_elem in brn.find_all('div', {'class': 'MuiButtonBase-root MuiListItem-root jss133 MuiListItem-gutters MuiListItem-button'}):                                \n",
    "                            for pro_ref in nav_elem.find_all('a'):\n",
    "                                product_references.append(pro_ref.get('href'))   \n",
    "                all_data['product_references'] = product_references\n",
    "\n",
    "                datas.append(all_data)\n",
    "    #             print(all_data['alternative_brands'])\n",
    "        #             ############################# db duplicate check, insert #################################\n",
    "                if all_data['sku'] not in db_sku:            \n",
    "                    print(all_data['alternative_brands'])\n",
    "                    all_data['product_images'] = str(all_data['product_images'])\n",
    "                    all_data['main_img'] = str(all_data['main_img'])\n",
    "                    offer_details = str(offer_details)\n",
    "                    all_data['other_desciption'] = str(all_data['other_desciption'])\n",
    "#                     print(all_data['other_desciption'])\n",
    "                    all_data['alternative_brands'] = str(all_data['alternative_brands'])\n",
    "#                     print(all_data['alternative_brands'])\n",
    "                    all_data['product_references'] = str(all_data['product_references'])\n",
    "                    all_data['disclaimer'] = str(all_data['disclaimer'])\n",
    "#                     print(type(offer_details)) \n",
    "#                     print(str(all_data['cart']))\n",
    "#                     print(str(all_data['medicine_name']),str(all_data['med_gram']),str(all_data['mtype']),\n",
    "#                          str(all_data['mcompany']),str(all_data['people_view']), str(all_data['generic']),str(all_data['best_price_amount']),)\n",
    "#                     ins = products.insert().values(sku = all_data['sku'],other_desciption=str(all_data['other_desciption']))\n",
    "#                     ins = products.insert().values(sku = all_data['sku'], url = all_data['url'],\n",
    "#                                                    product_images=all_data['product_images'], \n",
    "#                                                    main_img=all_data['main_img'],\n",
    "#                                                    medicine_name=str(all_data['medicine_name']), \n",
    "#                                                    medicine_weight=str(all_data['med_gram']),\n",
    "#                                                    medicine_type=str(all_data['mtype']),\n",
    "#                                                    medicine_company=str(all_data['mcompany']),\n",
    "#                                                    people_view=str(all_data['people_view']), \n",
    "#                                                    generic=str(all_data['generic']),\n",
    "#                                                    best_price_amount=str(all_data['best_price_amount']),\n",
    "#                                                    previous_price_amount=str(all_data['previous_price_amount']), \n",
    "#                                                    cart=str(all_data['cart']),\n",
    "#                                                    offer_title=str(all_data['offer_title']), \n",
    "#                                                    additional_offers=str(offer_details),\n",
    "#                                                    other_desciption=str(all_data['other_desciption'],\n",
    "#                                                    alternative_brands=all_data['alternative_brands'], \n",
    "#                                                    product_references=all_data['product_references'],\n",
    "#                                                    disclaimer=all_data['disclaimer'], \n",
    "#                                                    cat_id=all_data['cat_id'],status=1)\n",
    "#                                                   )\n",
    "                    ins = products.insert().values(sku = all_data['sku'], url = all_data['url'],\n",
    "                                                       product_images=all_data['product_images'], main_img=all_data['main_img'],\n",
    "                                                       medicine_name=str(all_data['medicine_name']), medicine_weight=str(all_data['med_gram']),\n",
    "                                                       medicine_type=str(all_data['mtype']),medicine_company=str(all_data['mcompany']),\n",
    "                                                       people_view=str(all_data['people_view']), generic=str(all_data['generic']),\n",
    "                                                       best_price_amount=str(all_data['best_price_amount']),\n",
    "                                                       previous_price_amount=str(all_data['previous_price_amount']), \n",
    "                                                       cart=str(all_data['cart']),offer_title=str(all_data['offer_title']), \n",
    "                                                       additional_offers=str(offer_details),other_desciption=str(all_data['other_desciption']), \n",
    "                                                       alternative_brands=all_data['alternative_brands'], \n",
    "                                                       product_references=all_data['product_references'],\n",
    "                                                       disclaimer=all_data['disclaimer'], cat_id=all_data['cat_id'],status=1)\n",
    "#                     print(ins)\n",
    "                    reslt = conn.execute(ins)\n",
    "                    db_sku.append(all_data['sku'])\n",
    "    #                 print(reslt)\n",
    "            elif st_code == 404:\n",
    "                ins = products.insert().values(sku=n, status = 0)\n",
    "                reslt = conn.execute(ins)\n",
    "                db_sku.append(n)\n",
    "    #         end_time = time.time()\n",
    "            elif st_code == 308:\n",
    "                ins = products.insert().values(sku=n, status = 0)\n",
    "                reslt = conn.execute(ins)\n",
    "                db_sku.append(n)\n",
    "            else:\n",
    "                error.append(n)\n",
    "        except:\n",
    "#             ins = products.insert().values(sku=n, status = 0)\n",
    "#             reslt = conn.execute(ins)\n",
    "            db_sku.append(n)\n",
    "            break\n",
    "    n= n-1\n",
    "#     time_diff = end_time - start_time\n",
    "#     print(time_diff)\n",
    "# print(error)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "d985ed6b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(36998, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)\n",
      "Count: 3\n"
     ]
    }
   ],
   "source": [
    "import requests\n",
    "import csv\n",
    "import time\n",
    "from selenium import webdriver\n",
    "from bs4 import BeautifulSoup\n",
    "import sys\n",
    "import pandas as pd\n",
    "import openpyxl\n",
    "# import mysql.connector\n",
    "import json\n",
    "import sqlalchemy as db\n",
    "from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, func, desc\n",
    "from sqlalchemy import insert\n",
    "import pymysql\n",
    "\n",
    "pymysql.install_as_MySQLdb()\n",
    "engine = create_engine('mysql://root:@localhost/arogga_data')\n",
    "conn = engine.connect()\n",
    "# metadata = db.MetaData()\n",
    "meta = MetaData()\n",
    "products = db.Table('products', meta, autoload=True, autoload_with=engine)\n",
    "db_sku = [];\n",
    "\n",
    "s = products.select().limit(1)\n",
    "myresult = conn.execute(s)\n",
    "for sr in myresult:\n",
    "    print(sr)\n",
    "# CREATE A SESSION OBJECT TO INITIATE QUERY IN DATABASE\n",
    "from sqlalchemy.orm import sessionmaker\n",
    "Session = sessionmaker(bind = engine)\n",
    "session = Session()\n",
    " \n",
    "# SELECT COUNT(*) FROM Actor\n",
    "result = session.query(products).count()\n",
    " \n",
    "print(\"Count:\", result)\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
