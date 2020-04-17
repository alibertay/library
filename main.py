import functions as fc

fc.create_table_books()
fc.create_table_user()

while True:
    choise = input("R - Register, L - Login: ")

    if choise == "R" or choise == "r":
        fc.register()

    elif choise == "L" or choise == "l":
        fc.login()

    else:
        print("Not valid!")