import sqlite3
import os
from tableDrawer import *
import time
import msvcrt

#the initial creation of the tables and the database
con = sqlite3.connect("OnlineShop.db")
cur = con.cursor()
cur.execute("""create table if not exists customer(username text, password text, email text, adminIndex BOOLEAN)""")
cur.execute("""create table if not exists shoppingLog(username text, productID int, quantity int, totalPrice real, purchaseDate text)""")
cur.execute("""create table if not exists shoppingCart(username text, productID int)""")
cur.execute("""create table if not exists products(productID int, productName text, category text, inStock int, price real)""")
cur.execute("""create table if not exists sellersProducts(sellerID text, productID int)""")



def waitForKeyPress():
    print("Press any key to continue...")
    msvcrt.getch()


def showAllProductsSeller(username):
    os.system("cls")
    with sqlite3.connect('OnlineShop.db') as conn: 
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        if not products:
            print("There are no products in the database.")
            time.sleep(3)
            adminPanel(username)

        else:
            printTable('products')
            waitForKeyPress()
            if username:
                adminPanel(username)
            else:
                guestPanel()


def addProductToList(username):
    categories = ['Clothes', 'Appliances', 'Electronics', 'Books', 'Toys', 'Furniture', 'Sports', 'Beauty', 'Automotive', 'Groceries']
    os.system("cls")
    print("Please enter the relevant information: ")
    name = input("Product name: ")
    num = 1
    print("Categories: ")
    for category in categories:
        print( str(num) + '. ' +category)
        num += 1
    category = categories[int(input("Choose one: "))-1]
    number = int(input("Number in-stock: "))
    price = int(input("Price: "))

    with sqlite3.connect('OnlineShop.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productID FROM products')
        idNum = cur.fetchall()
        cur.execute('INSERT INTO products VALUES( ?, ?, ?, ?, ?)',(len(idNum)+1, name, category, number, price))
        conn.commit()
        cur.execute('INSERT INTO sellersProducts VALUES(?, ?)', (username, len(idNum)+1))
        conn.commit()
        print("Product has been added.")
        time.sleep(2)
        showSellerProducts(username)


def editProduct(username):
    product = int(input("Which product would you like to edit? "))
    columnNames = ["productName", "category", "inStock", "price"]
    columns = map(int, input("Which columns would you like to edit? (write like so: 1,2,3...)\n1. Product name\t2. Category\t3. InStock \t4. Price").split(','))
    with sqlite3.connect('OnlineShop.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT products.*
            FROM products
            JOIN sellersProducts ON products.productID = sellersProducts.productID
            WHERE products.productID = ? AND sellersProducts.sellerID = ?''', (product, username))
        itemToBeEdited = cur.fetchone()
        if not itemToBeEdited:
            print("This product does not belong to you.")
            time.sleep(2)
            showSellerProducts(username)
        else:
            for columnIndex in columns:
                columnName = columnNames[columnIndex-1]
                value = input(f"Enter new value for {columnName}: ")
                cur.execute(f'UPDATE products SET {columnName} = ? WHERE productID = ?', (value, product))
                conn.commit()
            print("Product has been updated.")
            time.sleep(2)
            showSellerProducts(username)


def deleteProduct(username):
    product = int(input("Which product would you like to delete? "))
    with sqlite3.connect('OnlineShop.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT products.*
            FROM products
            JOIN sellersProducts ON products.productID = sellersProducts.productID
            WHERE products.productID = ? AND sellersProducts.sellerID = ?''', (product, username))
        itemToBeEdited = cur.fetchone()
        if not itemToBeEdited:
            print("This product does not belong to you.")
            time.sleep(2)
            showSellerProducts(username)
        else:
            cur.execute('DELETE FROM products WHERE productID = ?', (product,))
            conn.commit()
            cur.execute('DELETE FROM sellersProducts WHERE productID = ?', (product,))
            conn.commit()
            cur.execute('DELETE FROM shoppingCart WHERE productID = ?', (product,))
            conn.commit()
            cur.execute('UPDATE products SET productID = productID - 1 WHERE productID > ?', (product,))
            conn.commit()
            cur.execute('UPDATE sellersProducts SET productID = productID - 1 WHERE productID > ?', (product,))
            conn.commit()
            cur.execute('UPDATE shoppingCart SET productID = productID - 1 WHERE productID > ?', (product,))
            conn.commit()
            print("Product has been deleted.")
            time.sleep(2)
            showSellerProducts(username)


def showSellerProducts(username):
    os.system("cls")
    with sqlite3.connect('OnlineShop.db') as conn: 
        cur = conn.cursor()
        cur.execute('''
            SELECT products.*
            FROM products
            JOIN sellersProducts ON products.productID = sellersProducts.productID
            WHERE sellersProducts.sellerID = ? ''', (username,))
        products = cur.fetchall()
        if not products:
            print("There are no products in the database.")

        else:
            columns = [desc[0] for desc in cur.description]
            printTable(products, columns)

        ans = int(input("What would you like to do?\n1. Add a product\n2. Edit a product\n3. Delete a product\n4. Back\n"))
        if ans == 1:
            addProductToList(username)
        elif ans == 2:
            editProduct(username)
        elif ans == 3:
            deleteProduct(username)
        elif ans == 4:
            adminPanel(username)
        else:
            print("Invalid input.")
            time.sleep(2)
            showSellerProducts(username)


def adminPanel(username):
    os.system("cls")
    print("1. See all products\n2. See your products\n3. Exit")
    ans = int(input())
    if ans == 1:
        showAllProductsSeller(username)
    elif ans == 2:
        showSellerProducts(username)
    else:
        main()


def search(username):
    filter = map(int, input("What would you like to search for? (IF multiple: 1,2,3...)\n1. Product name\n2. Category\n3. Price\n4. Back\n").split(','))
    things = {}
    for ans in filter:
        
        if ans == 1:
            name = input("Enter the name of the product: ")
            things['productName'] = name
            

        elif ans == 2:
            categories = ['Clothes', 'Appliances', 'Electronics', 'Books', 'Toys', 'Furniture', 'Sports', 'Beauty', 'Automotive', 'Groceries']
            num = 1
            print("Categories: ")
            for category in categories:
                print( str(num) + '. ' +category)
                num += 1
            category = categories[int(input("Choose one: "))-1]
            things['Category'] = category

        elif ans == 3:
            price = int(input("Price must be lower than... "))
            things['price'] = price

        elif ans == 4:
            customerPanel(username)

        else:
            print("Invalid input.")
            time.sleep(2)
            search(username)
    

    query = "SELECT * FROM products WHERE "
    conditions = []
    values = []
    for key, value in things.items():
        if key == 'price':
            conditions.append(f"{key} < ?")
        else: 
            conditions.append(f"{key} = ?")
        values.append(value)
    query += " AND ".join(conditions)

    with sqlite3.connect('OnlineShop.db') as conn:
        cur = conn.cursor()
        cur.execute(query, values)
        products = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        printTable(products, columns)
        
    waitForKeyPress()
    showAllProductsCustomer(username)


def addToCart(username):
    with sqlite3.connect('OnlineShop.db') as conn:
        cur = conn.cursor()
        itemAdded = False
        while not itemAdded:
            ans = input("Which item do you want to add to your cart? ")
            cur.execute('SELECT * FROM products WHERE productID = ?', (ans,))
            selectedItem = cur.fetchone()
            if not selectedItem:
                print("This item does not exist. Please try again.")
                time.sleep(2)
                os.system("cls")
            else:
                cur.execute('INSERT INTO shoppingCart VALUES (?, ?)', (username, selectedItem[0]))
                conn.commit()
                print("Item has been added to your cart.")
                time.sleep(2)
                customerPanel(username)
                itemAdded = True


def buyProduct(username):
    while True:
        with sqlite3.connect('OnlineShop.db') as conn: 
            cur = conn.cursor()
            ans = int(input("Which product would you like to buy or add to your shopping cart? "))
            cur.execute('SELECT * FROM products WHERE productID = ?', (ans,))
            selectedItem = cur.fetchone()
            if not selectedItem:
                print("This product does not exist. Please try again.")
                time.sleep(2)
                continue
            quant = int(input("How many? "))
            if quant > selectedItem[3]:
                print("We do not have enough in stock.")
                time.sleep(2)
            else:
                cur.execute('UPDATE products SET inStock = inStock - ? WHERE productID = ?', (quant, ans))
                conn.commit()
                cur.execute('INSERT INTO shoppingLog VALUES (?, ?, ?, ?, ?)', (username, selectedItem[0], quant, selectedItem[4]*quant, '13:50'))
                conn.commit()
                print("Product has been added to your shopping log.")
        
        ans = input("Would you like to continue? Y/N\n").upper()
        while ans not in ['Y', 'N']:
            print("Answer is not applicable.")
            time.sleep(2)
            ans = input("Would you like to continue? Y/N\n").upper()
        if ans == 'Y':
            printTable('products')
            
        elif ans == 'N':
            customerPanel(username)
            break


def showAllProductsCustomer(username):
    os.system("cls")
    with sqlite3.connect('OnlineShop.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        if not products:
            print("There are no products in the database.")

        else:
            printTable('products')

        while True:
            ans = input("1. Buy product\n2. Add to Cart\n3. Search\n4. Back\n")
            if ans == '1':
                buyProduct(username)
                break
            elif ans == '2':
                addToCart(username)
                break
            elif ans == '3':
                search(username)
                break
            elif ans == '4':
                customerPanel(username)
                break
            else:
                print("Invalid input.")
                time.sleep(2)
        
    
def showPurchaseHistory(username):
    os.system("cls")
    with sqlite3.connect('OnlineShop.db') as conn: 
        cur = conn.cursor()
        cur.execute('SELECT * FROM shoppingLog where username = ?',(username,))
        log = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        printTable(log, columns)
        waitForKeyPress()
        customerPanel(username)
        

def removeFromCart(username):
    while True:
        product = int(input("Which product would you like to remove from your cart? "))
        with sqlite3.connect('OnlineShop.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM shoppingCart WHERE username = ? AND productID = ?', (username, product))
            item = cur.fetchone()
            if not item:
                print("This item does not exist in your cart.")
                time.sleep(2)
                continue
            else:
                cur.execute('DELETE FROM shoppingCart WHERE username = ? AND productID = ?', (username, product))
                conn.commit()
                print("Item has been removed from your cart.")
                time.sleep(2)
                break
    showShoppingCart(username)
        

def showShoppingCart(username):
    os.system("cls")
    with sqlite3.connect('OnlineShop.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT products.* from products JOIN shoppingCart ON products.productID = shoppingCart.productID WHERE shoppingCart.username = ?', (username,))
        products = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        printTable(products, columns)
        while True:
            ans = int(input("1. Buy a product\n2. Delete product from cart\n3. Back\n"))
            if ans == 1:
                while True:
                    with sqlite3.connect('OnlineShop.db') as conn: 
                        cur = conn.cursor()
                        ans = int(input("Which product would you like to buy from your shopping cart? "))
                        cur.execute('SELECT * FROM products WHERE productID = ?', (ans,))
                        selectedItem = cur.fetchone()
                        cur.execute('SELECT * FROM shoppingCart WHERE productID = ?', (ans,))
                        exists = cur.fetchone()
                        if not exists:
                            print("This product does not exist. Please try again.")
                            time.sleep(2)
                            continue
                        quant = int(input("How many? "))
                        if quant > selectedItem[3]:
                            print("We do not have enough in stock.")
                            time.sleep(2)
                        else:
                            cur.execute('UPDATE products SET inStock = inStock - ? WHERE productID = ?', (quant, ans))
                            conn.commit()
                            cur.execute('INSERT INTO shoppingLog VALUES (?, ?, ?, ?, ?)', (username, selectedItem[0], quant, selectedItem[4]*quant, '13:50'))
                            conn.commit()
                            cur.execute('DELETE FROM shoppingCart WHERE username = ? AND productID = ?', (username, ans))
                            conn.commit()
                            print("Product has been added to your shopping log.")
                            break
            elif ans == 2:
                removeFromCart(username)
                break
            elif ans == 3:
                customerPanel(username)
                break
            else:
                print("Invalid input.")
                time.sleep(2)
        os.system("cls")
        customerPanel(username)


def customerPanel(username):
    os.system("cls")
    print("1. See all products\n2. See purchase history\n3. See shopping cart\n4. Exit")
    ans = int(input())
    if ans == 1:
        showAllProductsCustomer(username)
    elif ans == 2:
        showPurchaseHistory(username)
    elif ans == 3:
        showShoppingCart(username)
    else:
        main()


def signUp():
    os.system("cls")
    print("<<SIGN UP>>")
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")

    while True:
        adminIndex = input("Are you a seller? Y/N: ").strip().upper()
        if adminIndex == 'Y':
            adminIndex = True
            break
        elif adminIndex == 'N':
            adminIndex = False
            break
        else:
            print("Unrecognized input. Please enter 'Y' or 'N'.")
            time.sleep(2)


    with sqlite3.connect('OnlineShop.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT username FROM customer WHERE username = ? ', (username,))
        isNOTUnique = cur.fetchone()
        if isNOTUnique:
            print("This username exists, please enter another one.")
            time.sleep(3)
            signUp()
        else:
            cur.execute('INSERT INTO customer (username, password, email, adminIndex) VALUES (?, ?, ?, ?)', (username, password, email, adminIndex))
            conn.commit()
            print("successfully added to our database!")
            time.sleep(3)
            main()
         

def signIn():
    os.system("cls")
    print("<<SIGN IN>>")
    username = input("Username: ")
    password = input("Password: ")
    userFound = False
    with sqlite3.connect('OnlineShop.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT username, password, adminIndex FROM customer')
        allInfo = cur.fetchall()
        for info in allInfo:
            if info[0] == username and info[1] == password:
                if info[2] == 0:
                    customerPanel(username)
                else:
                    adminPanel(username)
                userFound = True
                break

    if not userFound:
        print("Either username and/or password is incorrect or this user does NOT exist.")
        time.sleep(3)
        signIn()


def guestPanel():
    os.system("cls")
    print("""<<GUEST PANEL>>\n1. See all products\n2. Back""")
    ans = int(input())
    if ans == 1:
        username = None
        showAllProductsSeller(None)
    elif ans == 2:
        main()


def main():
    os.system("cls")
    print("""Welcome to our Online Shop!\n1. Sign up\n2. Sign in\n3. Enter as a guest\n4. Exit""")
    
    ans = int(input())
    if ans == 1:
        signUp()
    elif ans == 2:
        signIn()
    elif ans == 3:
        guestPanel()
    else:
        print("Thanks for using our app!")


main()

