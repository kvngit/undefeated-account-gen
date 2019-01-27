import os.path
import requests
from random import randint
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
from bs4 import BeautifulSoup

print("Created by kevin#3074")
api_key = str(input("Enter API key from Anti-cap: "))
sitekey = '6LeoeSkTAAAAAA9rkZs5oS82l69OEYjKRZAiKdaF'
captcha_url = 'https://undefeated.com/challenge'

def CreateEmail(fname, lname, domain):
    email = "{}.{}{}@{}".format(fname, lname, randint(0, 99999), domain)
    return email

def SaveToFile():
    if os.path.exists("undefeated_accounts.txt"):
        text_file = open("undefeated_accounts.txt", "a")
        text_file.write("{}:{}\n".format(email, password))
        text_file.close()
    else:
        text_file = open("undefeated_accounts.txt", "w")
        text_file.write("{}:{}\n".format(email, password))
        text_file.close()

def CreateAccount(email):
    s = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Host': 'undefeated.com',
        'Origin': 'https://undefeated.com',
        'Referer': 'https://undefeated.com/account/register'
    }

    data = {
        'form_type': 'create_customer',
        'utf8': '✓',
        'customer[first_name]': fname,
        'customer[last_name]': lname,
        'customer[email]': email,
        'customer[password]': password
    }
    r1 = s.post("https://undefeated.com/account", data=data, headers=headers)

    if r1.url == captcha_url:
        print("Encountered captcha")
        soup = BeautifulSoup(r1.text, "html.parser")
        authToken = soup.find("input", {"name": "authenticity_token"})['value']
        print("Sending job to anti-captcha, please wait for it to be solved")
        print("If this is taking a long time to solve, go to https://anti-captcha.com/clients/reports/dashboard to check if it's still being solved")
        client = AnticaptchaClient(api_key)
        task = NoCaptchaTaskProxylessTask(captcha_url, sitekey)
        job = client.createTask(task)
        job.join()
        job.get_solution_response()

        headers2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Origin': 'https://undefeated.com',
            'Referer': 'https://undefeated.com/challenge'
        }

        data2 = {
            'utf8': '✓',
            'authenticity_token': authToken,
            'g-recaptcha-response': job.get_solution_response()
        }

        r1 = s.post("https://undefeated.com/account", data=data2, headers=headers2)

        if r1.url == "https://undefeated.com/":
            print("Successfully created an account with {}".format(email))
            SaveToFile()
        else:
            print("Creation unsuccessful")
    else:
        print("Successfully created an account with {}".format(email))
        SaveToFile()

acc_num = input("Enter the amount of accounts you want: ")
fname = input("Enter your first name: ")
lname = input("Enter your last name: ")
domain = input("Enter your catchall WITHOUT the @: ")
password = input("Enter the password you want: ")
print("--------------------")
counter = 1
for x in range(int(acc_num)):
    print("Starting on account number {}".format(counter))
    email = CreateEmail(fname, lname, domain)
    print("Using {}".format(email))
    CreateAccount(email)
    print("--------------------")
    counter += 1