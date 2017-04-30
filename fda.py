import sys
import requests
import codecs
from lxml import html
import psycopg2
import sys
import os
import urllib
import hashlib, random, struct
from django.core.files import File
from Crypto.Cipher import AES
from tempfile import TemporaryFile
import hashlib, random, struct


#INFO TO CONNECT TO THE DATABASE
conn_string = "host='ec2-54-163-234-140.compute-1.amazonaws.com' dbname='dbqfq1r2oh3rqt' user='jjxeooatlaeltg' password='9798b1db4634c90f0433c2abe9272c8e3390463e780b8584aa96106626c2b744'"
conn = psycopg2.connect(conn_string)
database = conn.cursor()


def main():
    #[('id',), ('password',), ('last_login',), ('is_superuser',), ('username',), ('first_name',), ('last_name',), ('email',), ('is_staff',), ('is_active',), ('date_joined',)]
    user_data = login()
    user_type = get_user_type(user_data)
    groups = get_group_data(user_data)
    reports = get_reports(user_data, user_type, groups)
    initial_prompt(user_data, groups, reports)


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
        print("\nInvalid username or password. Please try again.\n")
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
    database.execute("SELECT user_type FROM app_profile WHERE id=" + str(user_data[0]))
    user_type = database.fetchall()
    return user_type[0][0]

def get_reports(user_data, user_type, groups):
    reports = []
    #[('id',), ('name',), ('company_name',), ('company_ceo',), ('company_phone',), ('company_email',), ('company_location',), ('company_country',), ('isprivate',), ('release_date',), ('industry_id',), ('sector_id',), ('group_id',)]
    database.execute("SELECT * FROM reports_report")
    reports_data = database.fetchall()
    for r in reports_data:
        if user_type == 'site_manager':
            reports.append(r)
        elif r[8] == 0:
            #Is not private
            reports.append(r)
        else:
            for group in groups:
                #Group Id matches
                if r[12] == group[0]:
                    reports.append(r)
    return reports

def initial_prompt(user_data, groups, reports):
    while True:
        print("Please enter L see list of Reports")
        print("Please enter a Report ID to select a Report")
        print("Please enter Q to quit")
        print("Please enter E to encrypt a File")
        choice = input("Choice: ")
        if not(choice == 'Q' or choice == 'L' or choice == 'E' or choice.isdigit()):
            print("\nInvalid Choice\n")
        elif choice == 'L':
            print("\nHere is a list of Reports by Report ID and Report Name")
            for report in reports:
                print ("ID: " + str(report[0]) + " Name: " + report[1])
            print("")

        elif choice == 'Q':
            print("\nGoodbye")
            quit()

        elif choice == 'E':
            loop = True
            while (loop):
                print("\nPlease enter the name of the File you would like encrypt:")
                file_name = input("File Name: ")
                if os.path.isfile(file_name):
                    infile = open(file_name, 'rb')
                    outfile = open(file_name + ".enc", 'wb')
                    encrypt_file(infile, outfile)
                    loop = False
                else:
                    print ("Invalid File Name\n")

        else:
            choice = int(choice)
            valid_selection = False
            for report in reports:
                if choice == int(report[0]):
                    valid_selection = True
                    select_report(user_data, groups, report, reports)
                    quit()
            if not valid_selection:
                print("\nInvalid Choice\n")


def select_report(user_data, groups, report, reports):
    print ("\nYou have selected the report ID: " + str(report[0]) + " Name: " + report[1] + '\n')
    #[('id',), ('name',), ('company_name',), ('company_ceo',), ('company_phone',), ('company_email',), ('company_location',), ('company_country',), ('isprivate',), ('release_date',), ('industry_id',), ('sector_id',), ('group_id',)]

    industry = get_industy(report)
    sector = get_sector(report)
    attachments = get_attachments(report)
    group_name = ""
    for g in groups:
        if g[0] == report[12]:
            group_name = g[1]

    while True:
        print("Please enter V to view the Report")
        print("Please enter D to download the attachments of Report")
        print("Please enter B to go back")
        print("Please enter Q to quit")
        choice = input("Choice: ")
        if choice == 'V':
            print("\nReport View\n")
            print("ID: " + str(report[0]))
            print("Name: " + report[1])
            print("Company Name: " + report[2])
            print("Company CEO: " + report[3])
            print("Company Phone: " + report[4])
            print("Company Email: " + report[5])
            print("Company Location: " + report[6])
            print("Company Country: " + report[7])
            print("Sector: " + sector)
            print("Industry: "  + industry)
            print("Group: " + group_name)
            if report[8]:
                print("Private : Yes")
            else:
                print("Private : No")
            print("Release Date: " + str(report[9]))
            i = 0
            while i < len(attachments):
                print ("Attachment " + str(i) + " "+ attachments[i][1][8:])
                i+=1
            print("")

        elif choice == 'D':
            directory_name = "report_" + str(report[0]) + "_" + report[1] + "_attachments"
            i = 1
            while os.path.exists(directory_name):
                directory_name = "report_" + str(report[0]) + "_" + report[1] + "_attachments(" + str(i) + ")"
                i += 1
            os.makedirs(directory_name)
            print("")
            for attachment in attachments:
                print("Downloading " + attachment[1][8:])
                url = "http://cs3240.herokuapp.com/media/" + attachment[1]
                file_path= directory_name + "/" + attachment[1][8:]
                urllib.request.urlretrieve(url, file_path)
                if attachment[4]:
                    loop = True
                    while loop:
                        print("This file is encrypted. Would you like to decrypt it [Y/N]")
                        choice = input("Choice: ")
                        if choice == "Y":
                            print (file_path[:-4])
                            infile = open(file_path,'rb')
                            outfile = open(file_path[:-4], 'wb')
                            decrypt_file(infile, outfile)
                            os.remove(file_path)
                            loop = False
                        elif choice == "N":
                            loop = False
            print("")


        elif choice == 'B':
            print ("\nGoing back\n")
            initial_prompt(user_data, groups, reports)

        elif choice == 'Q':
            print("\nGoodbye")
            quit()
        else:
            print("\nInvalid Choice\n")


def get_industy(report):
    database.execute("SELECT name FROM reports_industry WHERE id=" + str(report[10]))
    industry = database.fetchall()[0][0]
    return industry

def get_sector(report):
    database.execute("SELECT name FROM reports_sector WHERE id=" + str(report[11]))
    sector = database.fetchall()[0][0]
    return sector

def get_attachments(report):
    #[('id',), ('attachment',), ('attachmenthash',), ('report_id',), ('isencrypted',)]
    # database.execute("SELECT column_name FROM information_schema.columns WHERE TABLE_NAME='reports_reportattachment'")
    # print (database.fetchall())
    database.execute("SELECT * FROM reports_reportattachment WHERE report_id=" + str(report[0]))
    attachment_data = database.fetchall()
    return attachment_data

def encrypt_file(infile, outfile, chunksize=64*1024):
    key = "0123456789123456"
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = infile.size
    outfile.write(struct.pack('<Q', filesize))
    outfile.write(iv)

    while True:
        chunk = infile.read(chunksize)
        if len(chunk) == 0:
            break
        elif len(chunk) % 16 != 0:
            chunk += ' ' * (16 - len(chunk) % 16)

        outfile.write(encryptor.encrypt(chunk))
    return outfile

def decrypt_file(infile, outfile, chunksize=64*1024):
    key = "0123456789123456"
    origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
    iv = infile.read(16)
    decryptor = AES.new(key, AES.MODE_CBC, iv)
    while True:
        chunk = infile.read(chunksize)
        if len(chunk) == 0:
            break
        outfile.write(decryptor.decrypt(chunk))
    outfile.truncate(origsize)
    return outfile



main()
