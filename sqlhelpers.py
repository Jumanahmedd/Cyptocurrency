from app import mysql, session
from Blockchain import Block, Blockchain

#costum exceptions for transaction errors
class InvalidTransactionException(Exception): pass
class InsufficientFundsException(Exception): pass

#-------------------------------Table class--------------------------------------
class Table():

    def __init__(self,table_name, *args):
        self.table = table_name
        #using the join function to arrange the columns
        self.columns = "(%s)"%",".join(args)
        self.columnsList = args

        #if the table does not exist creat it using the isnewtable function whiich is defined below
        if isnewtable(table_name):
            create_data = ""
            for column in self.columnsList:
                create_data += "%s varchar(100)," %column

            #creating the cursor object using the cursor method
            cursor_object = mysql.connection.cursor()
            #the execute method accepts a mysql query as a parameter and executes it
            cursor_object.execute("CREATE TABLE %s(%s)" %(self.table,create_data[:len(create_data)-1]))#this creates a table with the table name specified above and will include the columns specified in the self.column variable
            # the close() method will close the current cusor object
            cursor_object.close()


    #function to get all values from the table
    def getall(self):
        cursor_object = mysql.connection.cursor()
        result = cursor_object.execute("SELECT * FROM %s" %self.table)
        data = cursor_object.fetchall();
        return data

    #function to get one value based on a search value
    def getone(self, search, value):
        data = {}; cursor_object = mysql.connection.cursor()
        #this execurtes the sql command looks in the table for the search value
        result = cursor_object.execute("SELECT * FROM %s WHERE %s = \"%s\"" %(self.table, search, value))
        if result > 0: data = cursor_object.fetchone()
        cursor_object.close();
        return data

    #function to delet a row from the table
    def deletone(self, search,value):
        cursor_object = mysql.connection.cursor()
        cursor_object.execute("DELETE from %s where %s = \"%s\"" %(self.table, search, value))
        mysql.connection.commit(); cursor_object.close()

    #function to delete the whole table from mysql
    def drop(self):
        cursor_object = mysql.connection.cursor()
        cursor_object.execute("DROP TABLE %s" %self.table)
        cursor_object.close()

    #funcrtion to delete all the values in the table
    def deleteall(self):
        self.drop()
        self.__init__(self.table, *self.columnsList)

    #funtion to insert data into the table
    def insert(self, *args):
        data = ""
        for arg in args:
            data += "\"%s\"," %(arg)

        cursor_object = mysql.connection.cursor()
        cursor_object.execute("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns, data[:len(data)-1]))
        mysql.connection.commit()
        cursor_object.close()
#--------------------------------------------------------------------------------

#execute mysql code from python
def sql_raw(execution):
    cursor_object = mysql.connection.cursor()
    cursor_object.execute(execution)
    mysql.connection.commit()
    cursor_object.close()

#tis function checks if a table exists using the table's name
def isnewtable(tableName):
    cursor_object = mysql.connection.cursor()
    #this makes sure that the table exists by attempting to get data from the table
    try:
        result = cursor_object.execute("SELECT * from %s" %tableName)
        cursor_object.close()
    except:
        return True #incase an error occurs because the table doesnt exist
    else:
        return False #if there were no error because the table exists

#--------------------------------------------------------------------------------
#function to check if a user exists
def isnewuser(username):
    users = Table("users","name","email","username","password")
    data = users.getall()
    usernames = [user.get('username') for user in data]

    if username in usernames:
        return False
    else:
        return True

#a function for a user to send money to another user
def send_money(sender,recipient, amount):
    try:#making sure the amount's value is a float or integer
        amount = float(amount)
    except ValueError:
        raise InvalidTransactionException("Invalid Transaction")

    #makes sure the sender has enough money for the transaction
    if amount > get_balance(sender) and sender != "BANK":
        raise InvalidTransactionException("Insufficient Funds")
    elif sender == recipient or amount <= 0.00:#making sure amout is more than 0 and sender is not  sending to themselves
        raise InvalidTransactionException("Invalid Transaction.")
    elif isnewuser(recipient):#verify the existance of the recipient
        raise InvalidTransactionException("User Does Not Exist")

    #update and save the blockchain to the database
    blockchain = get_blockchain()
    number = len(blockchain.chain) + 1
    data = "%s --> %s --> %s" %(sender, recipient, amount)
    blockchain.mine(Block(number, data=data))
    sync_blockchain(blockchain)

#get balance of the user to update it after transaction
def get_balance(username):
    balance = 0.00
    blockchain = get_blockchain()

    #this will loop through the blockchain to get the sender's and recipient's usernames to update their balance
    for block in blockchain.chain:
        data = block.data.split("-->")
        if username == data[0]:
            balance -= float(data[2])
            print(balance)
        elif username == data[1]:
            balance += float(data[2])
            print(balance)
    return balance

#retrieve the blockchain from mysql to create a blockchain object of each row
def get_blockchain():
    blockchain = Blockchain()
    blockchain_sql = Table("blockchain","number","hash","previous","data","nonce")
    for b in blockchain_sql.getall():
        blockchain.add(Block(int(b.get('number')), b.get('previous'), b.get('data'), int(b.get('nonce'))))

    return blockchain

#delete the mysql table and then insert each row again with the updated data
def sync_blockchain(blockchain):
    blockchain_sql = Table("blockchain", "number", "hash", "previous", "data", "nonce")
    blockchain_sql.deleteall()

    for block in blockchain.chain:
        blockchain_sql.insert(str(block.number),block.hash(), block.previous_hash,block.data, block.nonce)

