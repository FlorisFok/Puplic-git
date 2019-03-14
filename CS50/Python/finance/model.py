from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash


class User(object):
    '''
    USER data base handeling
    '''
    def __init__ (self, source="sqlite:///finance.db"):
        self.db = SQL(source)

    def __str__(self):
        '''
        Returns the length of the database
        '''
        rows = self.db.execute("SELECT * FROM users")
        return f'User database contains {len(rows)} users'

    def get_user(self, user_id):
        '''
        returns the username corresponding to an ID number
        '''
        user_info = self.db.execute("SELECT username FROM users WHERE id = :username",
                          username=user_id)
        return user_info

    def get_hash(self, user_id):
        '''
        Returns the hash corresponding to an ID number
        '''
        hashy = self.db.execute("SELECT hash FROM users WHERE id = :username",
                          username=user_id)
        return hashy[0]['hash']

    def get_cash(self, user_id):
        '''
        returns the cash corresponding to an ID number
        '''
        cashy = self.db.execute("SELECT cash FROM users WHERE id = :username",
                          username=user_id)
        return cashy[0]["cash"]

    def set_cash(self, user_id, cash):
        '''
        Updates the cash of the row of a certain ID
        '''
        self.db.execute("UPDATE users SET cash = cash + :cash WHERE id = :username",
                        username = user_id,
                        cash = cash)
        return True

    def get_id(self, user):
        '''
        Returns a ID corresponding to a username
        '''
        user_id = self.db.execute("SELECT id FROM users WHERE username = :username",
                          username=user)
        return user_id[0]['id']

    def username_taken(self, user):
        '''
        Checks if username is taken
        '''
        user_info = self.db.execute("SELECT id FROM users WHERE username = :username",
                          username=user)
        if len(user_info) > 0:
            return True
        else:
            return False

    def check(self, username, password):
        '''
        Checks if password is correct of a certain username
        '''
        if not self.username_taken(username):
            return False

        user_id = self.get_id(username)
        sql_hash = self.get_hash(user_id)

        if check_password_hash(sql_hash, password):
            return True

        return False

    def add_user(self, user, password):
        '''
        Adds a user to the database
        '''
        uhash = generate_password_hash(password)
        self.db.execute("INSERT INTO users (username, hash)"
                   "VALUES (:username, "
                   ":uhash)",
                   username=user,
                   uhash=uhash)
        return True

class Stock(object):
    '''
    Stock database handeling
    '''

    def __init__ (self, source="sqlite:///finance.db"):
        self.db = SQL(source)

    def __str__(self):
        '''
        Returns the total amount of stocks in a string
        '''
        rows = self.db.execute("SELECT * FROM stocks")
        total = 0
        for row in rows:
            total += row["amount"]
        return f'Stock database contains {total} stocks'

    def get_stocks(self, user_id):
        '''
        Returns a list of stocks corresponding to an ID number
        '''
        all_stocks = self.db.execute("SELECT stock FROM stocks WHERE id = :username",
                          username=user_id)
        list_stocks = []
        for stock in all_stocks:
            list_stocks.append(stock['stock'])
        return list_stocks

    def get_portfolio(self, user_id):
        '''
        Returns the row in JSON of a user
        '''
        all_stocks = self.db.execute("SELECT * FROM stocks WHERE id = :username",
                          username=user_id)
        return all_stocks

    def get_amount(self, user_id, stock):
        '''
        Returns amount of stocks corresponding to an ID, if NONE returns 0.
        '''
        stock = stock.upper()
        amount = self.db.execute("SELECT amount FROM stocks WHERE id = :username AND stock = :stock",
                          username=user_id,
                          stock = stock)
        if amount:
            return amount[0]['amount']
        else:
            return 0

    def stock_zero(self, user_id, stock):
        '''
        Checks if Stock is None/empty
        '''
        stock_info = self.db.execute("SELECT amount FROM stocks WHERE id = :username AND stock = :stock",
                          username=user_id,
                          stock = stock)
        if len(stock_info) > 0:
            return False
        else:
            return True

    def delete_stock(self, user_id, stock):
        '''
        Deletes stock of user.
        '''
        self.db.execute("Delete FROM stocks WHERE id = :username and stock = :stock",
                         username=user_id,
                         stock = stock)
        return True

    def add_stock(self, user_id, stock, amount):
        '''
        Adds stock of user
        '''
        self.db.execute("INSERT INTO stocks (id, stock, amount)"
                   "VALUES (:username, :stock ,:amount)",
                   username=user_id,
                   stock = stock,
                   amount = amount)
        return True

    def set_stock(self, user_id, stock, amount):
        '''
        Updates stock of user
        '''
        old_amount = self.db.execute("SELECT amount FROM stocks "
                                     "WHERE id = :username AND stock = :stock",
                                     username = user_id,
                                     stock = stock)

        amount = old_amount[0]["amount"] + amount
        self.db.execute("UPDATE stocks SET amount = :amount "
                        "WHERE id = :username AND stock = :stock",
                        amount = amount,
                        username = user_id,
                        stock = stock)
        return True

class History(object):
    '''
    Transaction History handeling
    '''

    def __init__ (self, source="sqlite:///finance.db"):
        self.db = SQL(source)

    def __str__(self):
        '''
        Returns length of database
        '''
        rows = self.db.execute("SELECT * FROM history")
        return f'Transaction database contains {len(rows)} transactions'

    def get_history(self, user_id):
        '''
        Returns JSON of all users transactions
        '''
        all_transactions = self.db.execute("SELECT * FROM history WHERE id = :username",
                          username=user_id)
        return all_transactions

    def add_transaction(self, user_id, stock, amount, cash):
        '''
        Adds a transaction
        '''
        self.db.execute("INSERT INTO history (id, stock, amount, cash)"
                   "VALUES (:username, :stock, :amount, :cash)",
                   username = user_id,
                   stock = stock,
                   amount = amount,
                   cash = cash)