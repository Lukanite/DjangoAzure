import sys
import requests
import codecs
from lxml import html
#from models import Report

print("Welcome to the Lokahi Crowdfunding file download application! "
       "Here you can view available reports and download their attached file(s). "
      "Begin by logging in with your username and password.\n")

login1 = 'http://cs3240.herokuapp.com/login/'
login2 = 'http://cs3240.herokuapp.com/login/?next=/reports/'

username = input("Username: ")
password = input("Password: ")
print("\n")

client = requests.Session()
client.auth = ('admin', 'admin')

client.get(login1)
csrftoken = client.cookies['csrftoken']
data = {'username': username, 'password': password, 'csrfmiddlewaretoken': csrftoken}

# r2 = client.get(login1)
# r2.encoding = 'cp1252'
# print (r2.text)

r = client.post(login2, data=data)
r.encoding = 'cp1252'
#print(r.url)
#print(r.text)
#print(r.cookies)

while r.url != 'http://cs3240.herokuapp.com/reports/':
    print("Invalid username or password. Please try again.\n")
    username = input("Username: ")
    password = input("Password: ")
    data = {'username': username, 'password': password, 'csrfmiddlewaretoken': csrftoken}
    r = client.post(login2, data=data)
    r.encoding = 'cp1252'

print("\nLogin successful! Enter the name of the report you would like to view.")
choice = input("Report name: ")

#print(r.headers['content-type'])
#print(r.content)
#print(r.encoding)
#r.encoding = 'cp1252'
#print (r.text)
#r.encoding = 'cp1252'
#print(r.text.encode('utf-8').decode('utf-8'))
