import sys
import time

import requests
from bs4 import BeautifulSoup
from push import push_message

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "cookie": "__mmapiwsid=018f00d2-fea1-7853-aeec-74e60ded414b:dfeee073829af5e1928aa8ae6c89c3316bcb2ce2; HBAffiliate=38%3A173917%3A888ac8d450cf5ba9add065da33577705; leftmenu_hide=; SESSID778d=gqh7rhqdnqe0f9f92uclgs8v5o"
}
if __name__ == '__main__':
    url = "https://clients.zgovps.com/index.php?/cart/special-offer/"
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('div', class_='col-md-6 col-12 mt-4')

        for product in products:
            product_name = product.find('strong').text.strip()
            price_element = product.select_one('select[name="cycle"] option')
            price = price_element.text.strip()
            stock_button = product.select_one('button.btn')
            stock = "Out of stock!" if stock_button.text.strip() == "Out of stock!" else "In stock"
            last_li = product.find_all('div', class_='my-3')[0].find_all('li')[-1].text.strip()
            # print("产品名:", product_name)
            print(f"{last_li} | {price} | {stock}")
            # print("品名:", last_li)
            # print("价格:", price)
            # print("库存:", stock)
            if stock == "In stock" and price != "$52.00 USD 年付":
                print("开始抢购吧!\nhttps://clients.zgovps.com/index.php?/cart/special-offer/")
                push_message("活动开始了", "开始抢购吧!\nhttps://clients.zgovps.com/index.php?/cart/special-offer/")
            print()
        time.sleep(1)
    except Exception as e:
        push_message("抢购脚本出错了", f"{str(e)}")
        print(str(e))
