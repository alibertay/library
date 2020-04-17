import sqlite3
import datetime
import time
import random

con = sqlite3.connect("library.db")
cursor = con.cursor()

# CREATING TABLE
def create_table_user():
    cursor.execute("CREATE TABLE IF NOT EXISTS users (nickname TEXT, password TEXT)")
    con.commit()

def create_table_books():
    cursor.execute("CREATE TABLE IF NOT EXISTS books (book_name TEXT, writer TEXT, page INT, book_number INT, publisher TEXT, available TEXT)")
    con.commit()

# FOR BOOKS
def add_book():
    book_name_input = input("Book name: ")
    writer_input = input("Writer: ")
    page_input = int(input("Number of pages: "))
    book_number_input = random.randrange(0,10000)
    publisher_input = input("Publisher: ")
    cursor.execute("INSERT INTO books VALUES(?,?,?,?,?,'yes')", (book_name_input, writer_input, page_input, book_number_input, publisher_input))
    con.commit()
    print("Book number: "+ str(book_number_input))

def delete_book():
    book_name_input = input("Book name: ")
    cursor.execute("DELETE FROM books WHERE book_name = '"+book_name_input+"'")
    con.commit()

def search_book():
    book_number_input = input("Barkod: ")
    output = cursor.execute("SELECT * FROM books WHERE book_number = '"+book_number_input+"'")
    output = cursor.fetchall()
    print(output)
    con.commit()

# FOR USERS
def register():
    nickname_input = input("Nickname: ")
    password_input = input("Password: ")
    cursor.execute("INSERT INTO users VALUES(?,?)",(nickname_input, password_input))
    cursor.execute("CREATE TABLE IF NOT EXISTS '"+nickname_input+"' (taken_book TEXT, taken_date TEXT, giving_date TEXT)")
    con.commit()

def login():
    global nck

    nck = input("Nickname for login: ")
    password_input = input("Password for login: ")

    if (len(nck) != 0 and len(password_input) != 0):
        auth = cursor.execute(
            "SELECT count(*) as 'nickname' FROM users WHERE nickname='" + nck + "' and password='" + password_input + "'")
        for i in auth.fetchall():
            login = i[0]
        if (login == 1):
            menu()

        elif (login == 0):
            print("Wrong nickname or password.")

def take_book():
    book_number_input = int(input("Book number: "))

    time_now = time.time()
    date = datetime.datetime.fromtimestamp(time_now).strftime('%Y-%m-%d-%H-%M-%S')

    cursor.execute("UPDATE books SET available = 'no' WHERE book_number = '"+ str(book_number_input)+"'")
    cursor.execute("INSERT INTO '"+nck+"' VALUES(?,?,?)",(str(book_number_input),'null','null'))
    cursor.execute("UPDATE '"+nck+"' SET taken_date ='"+date+"' WHERE taken_book = '"+str(book_number_input)+"'")
    cursor.execute("UPDATE '"+nck+"' SET giving_date = 'not given' WHERE taken_book = '"+str(book_number_input)+"'")
    con.commit()
    print("Succesfully done! Dear " +nck+ " please take care of book :)")

def give_book():
    book_number_input = int(input("Book number: "))

    time_now = time.time()
    date = str(datetime.datetime.fromtimestamp(time_now).strftime('%Y-%m-%d-%H-%M-%S'))

    cursor.execute("UPDATE books SET available = 'yes' WHERE book_number = "+str(book_number_input)+"")
    cursor.execute("UPDATE '"+nck+"' SET giving_date = '"+date+"' WHERE taken_book = '" +str(book_number_input) + "'")
    con.commit()
    print("Succesfully done!")

# MENU
def menu():
    while True:
        choise_input = input("Q - Quit, S - Searching book, A - Adding book, T - Taking book, G - Giving book, D - Delete book")

        if choise_input == "Q" or choise_input == "q":
            login()

        elif choise_input == "S" or choise_input == "s":
            search_book()

        elif choise_input == "A" or choise_input == "a":
            add_book()

        elif choise_input == "T" or choise_input == "t":
            take_book()

        elif choise_input == "D" or choise_input == "d":
            delete_book()

        elif choise_input == "G" or choise_input == "g":
            give_book()

        else:
            print("Not valid")
            menu()