import sqlite3
 
# Connecting to sqlite
# connection object to connect to a database
# If it doesn't exist a new one will be created
connection = sqlite3.connect('ebookstore.db')

# cursor object
# Used to interact with the database with sql commands
cursor = connection.cursor()

# Drop the books table if already exists.
cursor.execute("DROP TABLE IF EXISTS Books")

# Creating table
table = """ CREATE TABLE Books (
    ID int(4) NOT NULL,
    Title varchar(30),
    Author varchar(15),
    Qty int(2),
    PRIMARY KEY (ID)
        ); """

cursor.execute(table)
print("Table is Ready")

# Add to Books table
cursor.execute("""INSERT INTO Books VALUES (3001, 'A Tale of Two Cities', 'Charles Dickens', 30)""")
cursor.execute("""INSERT INTO Books VALUES (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40)""")
cursor.execute("""INSERT INTO Books VALUES (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25)""")
cursor.execute("""INSERT INTO Books VALUES (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37)""")
cursor.execute("""INSERT INTO Books VALUES (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)""")

def enter_book(ID, title, author, qty):
    # More pythonic way of ensuring a connection object is closed
    with connection:
        # Using a dictionary method to input variable names instead of using .format
        cursor.execute("""INSERT INTO Books VALUES (:ID, :title, :author, :qty)""", {'ID': ID, 'title': title,
        'author': author, 'qty': qty})

def update_book_qty(ID, qty):
    with connection:
        cursor.execute("""UPDATE Books SET Qty = :qty
        WHERE ID = :ID""", {'Qty': qty, 'ID': ID})

def delete_book(ID):
    with connection:
        cursor.execute("""DELETE from Books WHERE ID = :ID""", {'ID': ID})

def search_book(title):
    cursor.execute("""SELECT * from Books WHERE Title = :title""", {'title': title})
    return cursor.fetchall()

while True:
    # Error assertion for choosing the correct option
    while True:
        try:
            choice = int(input("""What would you like to do?
            1. Enter Book
            2. Update Book
            3. Delete Book
            4. Search Book
            0. Exit\n"""))
            break
        except ValueError:
            print('Please enter a valid integer (1, 2, 3, 4 or 0)')

    if choice == 1:
        print('Input book ID, title, author and quantity')
        while True:
            try:
                new_id = int(input('Please enter the book ID: '))
                break
            except ValueError:
                print('Please enter a valid integer')
        new_title = input('Please enter the book title: ')
        new_author = input('Please enter the book author: ')
        while True:
            try:
                new_qty = int(input('Please enter the book quantity: '))
                break
            except ValueError:
                print('Please enter a valid integer')
        enter_book(new_id, new_title, new_author, new_qty)

    elif choice == 2:
        update_id = int(input('Please enter the book ID you want to update: '))
        update_qty = int(input('Please enter the new quantity of the book: '))
        update_book_qty(update_id, update_qty)

    elif choice == 3:
        delete_id = int(input('Please enter the book ID of book you want to delete: '))
        delete_book(delete_id)

    elif choice == 4:
        search_title = input('Please enter the title of the book you want to search: ')
        print(search_book(search_title))

    elif choice == 0:
        break
    else:
        print('Please enter a valid choice')

# Print results
cursor.execute('SELECT * FROM Books')
results = cursor.fetchall()
print(results)
# Close the connection
connection.close()