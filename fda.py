import sys
import requests
import codecs
from lxml import html
import psycopg2
import sys

#INFO TO CONNECT TO THE DATABASE
conn_string = "host='ec2-54-163-234-140.compute-1.amazonaws.com' dbname='dbqfq1r2oh3rqt' user='jjxeooatlaeltg' password='9798b1db4634c90f0433c2abe9272c8e3390463e780b8584aa96106626c2b744'"
conn = psycopg2.connect(conn_string)
database = conn.cursor()


def main():
    #[('id',), ('password',), ('last_login',), ('is_superuser',), ('username',), ('first_name',), ('last_name',), ('email',), ('is_staff',), ('is_active',), ('date_joined',)]
    user_data = login()
    user_type = get_user_type(user_data)
    groups = get_group_data(user_data)
    initial_prompt(user_data, groups)


def login():
    print("Welcome to the Lokahi Crowdfunding file download application! "
       "Here you can view available reports and download their attached file(s). "
      "Begin by logging in with your username and password.\n")

    login1 = 'http://cs3240.herokuapp.com/login/'
    login2 = 'http://cs3240.herokuapp.com/login/?next=/reports/'

    username = input("Username: ")
    password = input("Password: ")

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

    print("\nLogin successful!\n")
    database.execute("SELECT * FROM auth_user WHERE username='" + username + "'")
    user_data = database.fetchall()[0]
    return user_data

def get_group_data(user_data):
    groups = []
    user_id = user_data[0]
    database.execute("SELECT * FROM auth_user_groups")
    groups_auth_data = database.fetchall()
    database.execute("SELECT * FROM auth_group")
    groups_data = database.fetchall()
    for g_auth in groups_auth_data:
        if g_auth[1] == user_id:
            for g in groups_data:
                if g[0] == g_auth[2]:
                    groups.append((g[0], g[1]))
    return groups

def get_user_type(user_data):
    database.execute("SELECT * FROM app_profile")
    app_profile_data = database.fetchall()
    print (app_profile_data)

def initial_prompt(user_data, groups):
    while True:
        print("Please enter L see list of Reports")
        print("Please enter a Report ID to select a Report")
        print("Please enter Q to quit")
        choice = input("Choice: ")
        if not(choice == 'Q' or choice == 'L'):
            print("Invalid Choice")

    #[('id',), ('name',), ('company_name',), ('company_ceo',), ('company_phone',), ('company_email',), ('company_location',), ('company_country',), ('isprivate',), ('release_date',), ('industry_id',), ('sector_id',), ('group_id',)]
        reports = []
        if choice == 'L':
            database.execute("SELECT * FROM reports_report")
            reports_data = database.fetchall()
            for r in reports_data:
                for group in groups:
                    if r[9] == 0:
                        reports.append((r[0], r[1]))
                    elif r[12] == group[0]:
                        reports.append((r[0],r[1]))
            print("\n\nHere is a list of Reports by Report ID and Report Name")
            for report in reports:
                print ("ID: " + str(report[0]) + " Name: " + report[1])
            print("\n")

        if choice == 'Q':
            quit()






main()
