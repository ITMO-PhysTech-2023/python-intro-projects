import sqlite3

class Message:
    def __init__(self, text = '', sender = '', receiver = '', header = ''):
        self.text, self.sender, self.receiver, self.header = text, sender, receiver, header

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return f"{self.text};{self.header};{self.sender};{self.receiver}"
        
    def set_all(self, text = '', sender = '', header = '', receiver = ''):
        
        if text != '': self.text = text 
        if sender != '': self.sender = sender
        if header != '': self.header = header
        if receiver != '': self.receiver = receiver

def adapt_message(message):
    return f"({message.text};{message.header};{message.sender};{message.receiver};)"


def adapt_list(List):
    return '{List}'.format(List = List)

class User_Database:
    def __init__(self, filename = 'users.db'):
        self.filename = filename
        sqlite3.register_adapter(Message, adapt_message)
        sqlite3.register_adapter(list, adapt_list)
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()


        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        received_messages List,
        sent_messages List,
        password TEXT NOT NULL
        )
        ''')

        cursor.execute('SELECT * FROM Users')

        self.users = cursor.fetchall()
        connection.commit()
        connection.close()

    def fetch(self):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM Users')

        self.users = cursor.fetchall()

        connection.commit()
        connection.close()

        return self.users

    def add_user(self, username = '@', email = '@', sent_messages = None, received_messages = None, password = '123'):
        connection = sqlite3.connect(self.filename)
        global user_db

        cursor = connection.cursor()
        if user_db.find_username(username) or username == '@':
            return 'User already exists'
        else:
            cursor.execute('INSERT INTO Users (username, email, sent_messages, received_messages, password) VALUES (?, ?, ?, ?, ?)', (username, email, sent_messages, received_messages, password,))

        connection.commit()
        connection.close()

    def delete_user(self, id = 0, username = ''):

        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        if id != 0:
            cursor.execute('DELETE FROM Users WHERE id = ?', (id,))
        elif username != '':
            cursor.execute('DELETE FROM Users WHERE username = ?', (username,))

        connection.commit()
        connection.close()

    def push_sent_message(self, username, message_id):

        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('SELECT sent_messages FROM Users WHERE username = ?', (username,))
        sent_messages = cursor.fetchall()
        #print(sent_messages)
        if sent_messages == [(None,)]:
            sent_messages = [message_id]
        else:
            s = list(int(i) for i in sent_messages[0][0][1:-1].split(', '))
            #print(s)
            s.append(message_id)
            sent_messages = s

        cursor.execute('UPDATE Users SET sent_messages = ? WHERE username = ?', (sent_messages, username))
        
        connection.commit()
        connection.close()

    def push_received_message(self, username, message_id):

        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('SELECT received_messages FROM Users WHERE username = ?', (username,))
        received_messages = cursor.fetchall()
        print(received_messages)
        if received_messages == [(None,)]:
            received_messages = [message_id]
        else:
            s = list(int(i) for i in received_messages[0][0][1:-1].split(', '))
            print(s)
            s.append(message_id)
            received_messages = s

        cursor.execute('UPDATE Users SET received_messages = ? WHERE username = ?', (received_messages, username))
        
        connection.commit()
        connection.close()

    def find_username(self, username):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
        
        user = cursor.fetchone()
        
        connection.commit()
        connection.close()

        return user
    
    def view_sent_messages(self, username, message_db_filename):
        connection = sqlite3.connect(message_db_filename)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Messages WHERE sender_username = ?', (username,))
        
        messages = cursor.fetchall()
        
        connection.commit()
        connection.close() 

        return messages
    
    def view_received_messages(self, username, message_db_filename):
        connection = sqlite3.connect(message_db_filename)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Messages WHERE receiver_username = ?', (username,))
        
        messages = cursor.fetchall()
        
        connection.commit()
        connection.close() 

        return messages



class Message_Database:
    def __init__(self, filename = 'messages.db'):
        self.filename = filename
        
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()


        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Messages (
        id INTEGER PRIMARY KEY,
        header TEXT NOT NULL,
        sender_username TEXT NOT NULL,
        sender_id INTEGER,
        receiver_username TEXT NOT NULL,
        receiver_id INTEGER,
        text TEXT,
        time TEXT
        )
        ''')

        cursor.execute('SELECT * FROM Messages')

        self.messages = cursor.fetchall()
        connection.commit()
        connection.close()

    def fetch(self):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM Messages')

        self.messages = cursor.fetchall()

        connection.commit()
        connection.close()

        return self.messages

    def add_message(self, sender_username = '', receiver_username = '', header = '', text = ''):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Messages (sender_username, receiver_username, header, text) VALUES (?, ?, ?, ?)', (sender_username, receiver_username, header, text))

        cursor.execute('SELECT id from Messages')

        message_id = cursor.fetchall()[-1]

        connection.commit()
        connection.close()
        return int(message_id[0])


    def delete_message(self, id = 0):

        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()

        if id != 0:
            cursor.execute('DELETE FROM Messages WHERE id = ?', (id,))

        connection.commit()
        connection.close()
