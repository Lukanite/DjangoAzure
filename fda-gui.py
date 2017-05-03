import tkinter as tk
from tkinter import ttk, StringVar, filedialog
from functools import partial
import requests
import psycopg2
import sys
import os
import urllib
from Crypto.Cipher import ARC4

# INFO TO CONNECT TO THE DATABASE
conn_string = "host='ec2-54-163-234-140.compute-1.amazonaws.com' dbname='dbqfq1r2oh3rqt' " \
              "user='jjxeooatlaeltg' password='9798b1db4634c90f0433c2abe9272c8e3390463e780b8584aa96106626c2b744'"
conn = psycopg2.connect(conn_string)
database = conn.cursor()


class Main(ttk.Frame):
    # ------ variables
    # ------
    user_data = ""
    user_type = ""
    groups = []
    reports = []

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()

    def on_quit(self):
        quit()

    def open_file(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.encrypt_window()

    def encrypt_file(self):
        if encrypt_file(self.filename, self.key_entry.get()):
            self.encrypt_frame.destroy()
        else:
            ttk.Label(self.encrypt_frame, text='Encrypt not successful.').grid(column=0, row=3)

    def encrypt_window(self):
        self.encrypt_frame = tk.Toplevel(padx=15, pady=15)
        self.encrypt_frame.title("Encrypt A File")
        self.encrypt_frame.option_add('*tearOff', 'FALSE')
        self.encrypt_frame.configure()

        ttk.Label(self.encrypt_frame, text='Filename: ').grid(column=0, row=0, sticky='w')
        ttk.Label(self.encrypt_frame, text=self.filename).grid(column=1, row=0)
        ttk.Label(self.encrypt_frame, text='Enter Encrypt key: ').grid(column=0, row=1)
        self.key_entry = ttk.Entry(self.encrypt_frame, width=25)
        self.key_entry.grid(column=1, row=1)
        tk.Button(self.encrypt_frame, text='Encrypt', command=self.encrypt_file).grid(column=1, row=2)

        for child in self.encrypt_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def login_window(self):
        self.login_frame = tk.Toplevel(padx=15, pady=15)
        self.login_frame.title("Login")
        self.login_frame.option_add('*tearOff', 'FALSE')
        self.login_frame.configure()

        ttk.Label(self.login_frame, text='Login').grid(column=0, row=0, columnspan=4)
        ttk.Label(self.login_frame, text='Username: ').grid(column=0, row=1)
        ttk.Label(self.login_frame, text='Password: ').grid(column=0, row=2)

        self.username_entry = ttk.Entry(self.login_frame, width=25)
        self.username_entry.grid(column=1, row=1)
        self.username_entry.focus_force()

        self.password_entry = ttk.Entry(self.login_frame, width=25, show="*")
        self.password_entry.grid(column=1, row=2)

        ttk.Separator(self.login_frame, orient='horizontal').grid(column=0, row=3, columnspan=4, sticky='ew')

        # Login Button
        login_button = tk.Button(self.login_frame, text='Login', command=self.try_login, width="10", height="1", bg="#ADD8E6")
        login_button.grid(column=0, row=4, columnspan=4)

        # self.password_entry.bind("<Return>", self.try_login)

        self.feedback = StringVar()
        self.feedback.set("Enter your username and password.")
        ttk.Label(self.login_frame, textvariable=self.feedback).grid(column=0, row=5, columnspan=4)

        for child in self.login_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def try_login(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        login1 = 'http://cs3240.herokuapp.com/login/'
        login2 = 'http://cs3240.herokuapp.com/login/?next=/reports/'
        client = requests.Session()
        client.auth = ('admin', 'admin')

        client.get(login1)
        csrftoken = client.cookies['csrftoken']
        data = {'username': self.username, 'password': self.password, 'csrfmiddlewaretoken': csrftoken}

        r = client.post(login2, data=data)
        r.encoding = 'cp1252'

        if r.url != 'http://cs3240.herokuapp.com/reports/':
            self.feedback.set("Invalid username or password. \nPlease try again.")

        else:
            database.execute("SELECT * FROM auth_user WHERE username='" + self.username + "'")
            self.user_data = database.fetchall()[0]
            self.user_type = get_user_type(self.user_data)
            self.groups = get_group_data(self.user_data)
            self.reports = get_reports(self.user_data, self.user_type, self.groups)
            self.update_main()
            self.login_frame.destroy()

    def view_report(self, event_object):
        curItem = self.list_of_reports.focus()
        report = self.list_of_reports.item(curItem).get('values')
        # report = self.list_of_reports.item(curItem.values)
        top = tk.Toplevel(padx=15, pady=15)
        # top.title(report[1])
        top.option_add('*tearOff', 'FALSE')
        top.configure()

        # [('id',), ('name',), ('company_name',), ('company_ceo',), ('company_phone',), ('company_email',),
        # ('company_location',), ('company_country',), ('isprivate',), ('release_date',), ('industry_id',),
        # ('sector_id',), ('group_id',), ('current_projects')]

        groups = get_group_data(self.user_data)
        industry = get_industy(report)
        sector = get_sector(report)
        attachments = get_attachments(report)
        group_name = "N/A"
        for g in groups:
            if g[0] == report[12]:
                group_name = g[1]

        ttk.Label(top, text='Report Text', font="Courier, 14").grid(column=0, row=0, sticky='w')

        ttk.Label(top, text='ID: ' + str(report[0])).grid(column=0, row=1, columnspan=4, sticky='w')
        ttk.Label(top, text='Name: ' + str(report[1])).grid(column=0, row=2, columnspan=4, sticky='w')
        ttk.Label(top, text='Company Name: ' + str(report[2])).grid(column=0, row=3, columnspan=4, sticky='w')
        ttk.Label(top, text='Company CEO: ' + str(report[3])).grid(column=0, row=4, columnspan=4, sticky='w')
        ttk.Label(top, text='Company Phone: ' + str(report[4])).grid(column=0, row=5, columnspan=4, sticky='w')
        ttk.Label(top, text='Company Email: ' + str(report[5])).grid(column=0, row=6, columnspan=4, sticky='w')
        ttk.Label(top, text='Company Location: ' + str(report[6])).grid(column=0, row=7, columnspan=4, sticky='w')
        ttk.Label(top, text='Company Country: ' + str(report[7])).grid(column=0, row=8, columnspan=4, sticky='w')
        ttk.Label(top, text='Sector: ' + sector).grid(column=0, row=9, columnspan=4, sticky='w')
        ttk.Label(top, text='Industry: ' + industry).grid(column=0, row=10, columnspan=4, sticky='w')
        ttk.Label(top, text='Group: ' + group_name).grid(column=0, row=11, columnspan=4, sticky='w')
        ttk.Label(top, text='Current Projects: ' + str(report[14]), wraplength=300, justify=tk.LEFT).grid(column=0, row=12, columnspan=4, sticky='w')
        ttk.Label(top, text='Private: ' + str(report[8])).grid(column=0, row=13, columnspan=4, sticky='w')
        ttk.Label(top, text='Release Date: ' + str(report[9])).grid(column=0, row=14, columnspan=4, sticky='w')

        ttk.Separator(top, orient='horizontal').grid(column=0, row=16, columnspan=6, sticky='ew')

        ttk.Label(top, text='Report Attachments', font="Courier, 14").grid(column=0, row=17, sticky='w')

        i = 1
        for attachment in attachments:
            ttk.Label(top, text=attachment[1]).grid(column=0, row=17+i, columnspan=4, sticky='w')
            download = partial(self.download_attachment, attachment, report)
            tk.Button(top, text='Download', command=download, width="10", height="1", bg="#ADD8E6").grid(column=1, row=17+i, columnspan=4, sticky='e')

        # Search Button
        # search_button = tk.Button(top, text='Search', command=top.destroy, width="10", height="1", bg="#55dd55")
        # search_button.grid(column=0, row=4, columnspan=4)

        for child in top.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def download_attachment(self, att, report):
        # make folder
        directory_name = "report_" + str(report[0]) + "_" + report[1] + "_attachments"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        # download attachment
        url = "http://cs3240.herokuapp.com/media/" + att[1]
        file_path = directory_name + "/" + att[1][8:]
        urllib.request.urlretrieve(url, file_path)

        # encrypted file
        if att[4]:
            self.give_key_window()
            self.get_file_path = file_path

    def give_key_window(self):
        self.give_key_frame = tk.Toplevel(padx=15, pady=15)
        self.give_key_frame.title("Encrypted File")
        self.give_key_frame.option_add('*tearOff', 'FALSE')
        self.give_key_frame.configure()

        ttk.Label(self.give_key_frame, text='Enter decrypt key: ').grid(column=0, row=0)
        self.key_entry = ttk.Entry(self.give_key_frame, width=25)
        self.key_entry.grid(column=1, row=0)
        tk.Button(self.give_key_frame, text='Decrypt', command=self.decrypt_file).grid(column=1, row=1)

        for child in self.give_key_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def decrypt_file(self):
        decrypt_file(self.get_file_path, self.key_entry.get())
        os.remove(self.get_file_path)
        self.give_key_frame.destroy()

    def update_main(self):
        i = 1
        for report in self.reports:
            self.list_of_reports.insert('', 'end', ('report' + str(i)), text=("Report #" + str(i)), values=report)
            i = i + 1
        tk.Button(self, text='Encrypt File', command=self.open_file, width="20", height="1", bg="#ADD8E6").grid(
            column=0, row=2, columnspan=4, sticky='w')
        tk.Button(self, text='Exit', command=self.on_quit, width="20", height="1", bg="#ADD8E6").grid(
            column=1, row=2, columnspan=4, sticky='e')

    def init_gui(self):
        self.root.title('Main')
        self.root.option_add('*tearOff', 'FALSE')
        self.root.configure()

        self.login_window()

        self.grid(column=0, row=0, sticky='nsew', padx=15, pady=15)

        # menu
        # menubar = tk.Menu(self.root)

        # file
        # menu_file = tk.Menu(menubar)
        # menu_file.add_command(label='Login', command=self.login_window)
        # menu_file.add_command(label='Exit', command=self.on_quit)

        # menu items/order
        # menubar.add_cascade(menu=menu_file, label='File')

        # self.root.config(menu=menubar)

        ttk.Label(self, text='Reports').grid(column=0, row=0, columnspan=4)
        self.list_of_reports = ttk.Treeview(self, columns=('ID', 'Name'))
        self.list_of_reports.column('ID', width=50)
        self.list_of_reports.heading('ID', text="ID")
        self.list_of_reports.heading('Name', text="NAME")

        self.list_of_reports.grid(column=0, row=1, columnspan=3)
        self.list_of_reports.tag_configure('ttk', background='blue')
        self.list_of_reports.bind('<Double-Button-1>', self.view_report)

        # a list of reports under the header Group #1
        # group1 = list_of_reports.insert('', 'end', text='Group #1')
        # list_of_reports.insert(group1, 'end', text='Group1: Report1')
        # list_of_reports.insert(group1, 'end', text='Group1: Report2')
        # list_of_reports.insert(group1, 'end', text='Group1: Report3')
        # list_of_reports.insert(group1, 'end', text='Group1: Report4')

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


def main():
    # [('id',), ('password',), ('last_login',), ('is_superuser',), ('username',), ('first_name',),
    # ('last_name',), ('email',), ('is_staff',), ('is_active',), ('date_joined',)]
    root = tk.Tk()
    root.resizable(width=False, height=False)
    Main(root)
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.mainloop()


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
    # [('id',), ('name',), ('company_name',), ('company_ceo',), ('company_phone',),
    # ('company_email',), ('company_location',), ('company_country',), ('isprivate',),
    # ('release_date',), ('industry_id',), ('sector_id',), ('group_id',)]
    database.execute("SELECT * FROM reports_report")
    reports_data = database.fetchall()
    for r in reports_data:
        if user_type == 'site_manager':
            reports.append(r)
        elif r[8] == 0:
            # Is not private
            reports.append(r)
        else:
            for group in groups:
                # Group Id matches
                if r[12] == group[0]:
                    reports.append(r)
    return reports


def get_industy(report):
    database.execute("SELECT name FROM reports_industry WHERE id=" + str(report[10]))
    industry = database.fetchall()[0][0]
    return industry


def get_sector(report):
    database.execute("SELECT name FROM reports_sector WHERE id=" + str(report[11]))
    sector = database.fetchall()[0][0]
    return sector


def get_attachments(report):
    # [('id',), ('attachment',), ('attachmenthash',), ('report_id',), ('isencrypted',)]
    # database.execute("SELECT column_name FROM information_schema.columns WHERE TABLE_NAME='reports_reportattachment'")
    # print (database.fetchall())
    database.execute("SELECT * FROM reports_reportattachment WHERE report_id=" + str(report[0]))
    attachment_data = database.fetchall()
    return attachment_data


def encrypt_file(file_name, symmetric_key):
    # symmetric_key = "0123456789123456"
    if os.path.isfile(file_name):
        input = open(file_name, 'rb')
        output_file_name = file_name.__add__(".enc")
        output = open(output_file_name, 'wb')

        cipher = ARC4.new(symmetric_key)
        size = sys.getsizeof(symmetric_key.encode('utf-8'), 32)
        while size < 40:
            symmetric_key = symmetric_key.__add__(' ')
            size = size + 1
        while size > 2048:
            symmetric_key = symmetric_key[:-1]
            size = size - 1
        for line in input:
            c = cipher.encrypt(line)
            output.write(c)
        input.close()
        output.close()
        return True
    else:
        return False


def decrypt_file(file_name, symmetric_key):
    # symmetric_key = "0123456789123456"
    if os.path.isfile(file_name):
        if (file_name[-4:] == ".enc"):
            input = open(file_name, 'rb')
            output_file_name = file_name
            output_file_name = output_file_name[:-4]
            output = open(output_file_name, 'wb')

            cipher = ARC4.new(symmetric_key)
            size = sys.getsizeof(symmetric_key.encode('utf-8'), 32)
            while size < 40:
                symmetric_key = symmetric_key.__add__(' ')
                size = size + 1
            while size > 2048:
                symmetric_key = symmetric_key[:-1]
                size = size - 1
            for line in input:
                c = cipher.decrypt(line)
                output.write(c)
            input.close()
            output.close()
            return True
    return False

main()

