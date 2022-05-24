import requests
import csv
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=options)
driver.set_window_size(1920, 1080)

url = [];

url.append("https://www.arogga.com/brand/36393/new-pro-ingrown-toe-nail-recover-toenail-correction-pedicure-fixer-toe-nail")
url.append("https://www.arogga.com/brand/12474/napa-500-tablet-500mg")
# print(len(url))
datas = [];
for u in url:
#     driver = webdriver.Chrome()
#     driver = webdriver.Firefox()
#     driver.get(u);
#     time.sleep(5)
#     driver.set_window_size(1500,1000);
#     client_response = Client(u)
#     source = client_response.mainFrame().toHtml()     
#     print(u)
#     URL = "https://www.arogga.com/brand/36393/new-pro-ingrown-toe-nail-recover-toenail-correction-pedicure-fixer-toe-nail"
    driver.get(u)
    r = driver.page_source
#     r = requests.get(u) 
    soup = BeautifulSoup(r, "html.parser") 
#     soup = BeautifulSoup(source, "html.parser")
    all_data = dict()
    # data = {}
    ########################## selector image #######################
    simg = soup.find('div', {'class': 'selectors'})
    # data['selector_img'] = simg.a['href']
    all_data['selector_img'] = simg.a['href']
    # print(data['selector_img']);
#     print(all_data['selector_img']);
    ########################## main image ###########################
    main_img = soup.find('div', {'class' : 'updateClass'})
    all_data['main_img'] = main_img.a['href']
#     print(all_data['main_img'])
    ########################## med name ###########################
    med_name = soup.find('h1', {'class': 'MuiTypography-root jss2 MuiTypography-h1'}).text

    all_data['med_name'] = med_name
#     print(med_name)
    ########################## med gram ###########################
    all_data['med_gram'] = soup.find('span', {'class':'jss3'}).text
#     print(all_data['med_gram'])
    # all_data['med_type'] = soup.find('div', {'class':['MuiGrid-root jss23 MuiGrid-item MuiGrid-grid-lg-6','jss4']}).h6.text
    # print(all_data['med_type'])
    # med = [];
    ########################## med type and company ###########################
    med = soup.find_all('div', {'class': 'MuiGrid-root jss23 MuiGrid-item MuiGrid-grid-lg-6'})
    count = 0
    y = []
    for med in soup.find_all('h6'):
    #     print(med.text)
        x = med.text
        y.append(x)
    #     count = count+1

    all_data['mtype'] = y[0];
    all_data['mcompany'] = y[1];
#     print(all_data['mtype'], all_data['mcompany'])
    # span_text_jss23 = []
    # for z in soup.find_all('span'):
    # #     print(z.text)
    #     span_text = z.text
    #     span_text_jss23.append(span_text)
    # # print(span_text_jss23)
    # print(span_text_jss23[10], span_text_jss23[11])
    # all_data['generic'] = span_text_jss23[10]
    # all_data['gen_type'] = span_text_jss23[11]

    ########################### Generic Name #############################
    for span_search in soup.find_all('div',{'class':'MuiGrid-root jss23 MuiGrid-item MuiGrid-grid-lg-6'}):
    #     span_t = span_search.find('span')
    #     print(span_t.text)

        span_text_jss23 = []
        for z in span_search.find_all('div'):
        #     print(z.text)
            span_text = z.text
            span_text_jss23.append(span_text)
    # print(span_text_jss23)
    # print(span_text_jss23[1])
        for d in span_search.find_all('div', {'class':'jss6'}):
                for dd in d.find_all('div', {'class':'jss7'}):
                    for pv in dd.find_all('span'):
        #                 print(pv.text)
                        all_data['people_view'] = pv.text

#     print(all_data['people_view'])

    all_data['generic'] = span_text_jss23[1]
#     print(all_data['generic'])

    # all_data['people_view'] = span_text_jss23[12]
    ########################## med price ###########################
    med_price = soup.find_all('div', {'class':'jss8'})
    price = []
    for med_price in soup.find_all('div', {'class':'jss8'}):
        link = med_price.find_all('div')
        for l in link:
    #         print(l.text)
            price.append(l.text)
    #     print(link)
    # print(price)
    all_data['best_price_title'] = price[0]
    all_data['best_price_amount'] = price[1]
    all_data['previous_price_title'] = price[2]
    all_data['previous_price_amount'] = price[3]
#     print(all_data['best_price_title'],all_data['best_price_amount'], all_data['previous_price_title'], all_data['previous_price_amount'])
    ########################## offer ###########################
    all_data['offer'] = soup.find('div',{'class': 'jss9'}).text
#     print(all_data['offer'])
    ########################## cart ###########################
    all_data['cart'] = soup.find('span', {'class': 'MuiButton-label'}).text
#     print(all_data['cart'])
    ########################## offers ###########################
    offers = dict();
    offer_title = soup.find('h2', {'class':'jss11'}).text
    all_data['offer_title'] = offer_title
    offer_details = []
#     print(offers['offer_title'])
    # offer_details_one = []
    for all_offers in soup.find_all('div', {'class':'jss14 jss22'}):    
    #     cashback = all_offers.find_all('strong', {'class': 'jss16'})
        offer_details.append(all_offers.text)
    #     print(all_offers.text)
    #     for cl in cashback:
    #         print(cl.text)
    #     print(cashback.text)
    # offer_details.append(offer_details_one)
    # print(offer_details)
    all_data['additional_offers'] = offer_details
#     print(all_data['Additional Offers'])
    ########################## other description ###########################
    for other in soup.find_all('div', {'class': 'jss90'}):
        other_desc = other.find_all('div', {'class': 'jss69'})
        for ot in other_desc:        
    #         print(ot)
            all_data['other_desciption'] = ot;
    #         title = ot.find('span').text;
    # #         print(title)
    #         safety = [title]
    # #         print(safety)
    #         count=0
    #         for safety_det in ot:
    #             s_details = safety_det.find_all('div',{'class':'jss82'})
#     print(all_data['other_desciption'])
     ########################## disclaimer ###########################    
    all_data['disclaimer']  = soup.find('div', {'class':'jss89'}).p.text
   
    datas.append(all_data)
    ########################## alternative products ###########################
    time.sleep(10)
    for alt in soup.find_all('div', {'class': 'jss69'}):
        for brn in alt.find_all('div', {'class':'jss93'}):
            all_data['alternative_brn'] = brn.nav       
   
print(all_data['other_desciption'])
# print( all_data['alternative_brn'])
#     filename="arogga_data.csv"
#     with open(filename, 'w', newline='') as f:
#         w=csv.DictWriter(f, ['selector_img', 'main_img', 'med_name', 'med_gram', 'mtype', 'mcompany', 
#                              'people_view', 'generic', 'best_price_title', 'best_price_amount', 
#                              'previous_price_title', 'previous_price_amount', 'offer', 'cart', 'offer_title',
#                             'additional_offers', 'other_desciption', 'alternative_brn', 'disclaimer'])
#         w.writeheader()
#         for all_data in datas:
#             w.writerow(all_data)