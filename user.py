import psycopg2
import bcrypt
import secrets
from admin import Admin

class User:
    def create_user_object(result):
        username = result[0]
        password_digest = bytes(result[1], 'utf-8')
        mail = result[2]
        phone = result[3]
        user_type = result[4]
        session_token = result[5]
        return User(username, None, mail, phone, user_type, password_digest, session_token)
    
    def find_by_session_token(session_token):
        connection = psycopg2.connect('dbname=sih_2023')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE session_token = \'{}\''.format(session_token))
        result = cursor.fetchall()

        if not result:
            return False 

        if result[0][4] == 'admin':
            return Admin.create_admin_object(result[0])
        else:
            return User.create_user_object(result[0])

    def find_by_credentials(email, password):
        connection = psycopg2.connect('dbname=sih_2023')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE mail = \'{}\';".format(email))
        result = cursor.fetchall()
        connection.close()

        if not result:
            return False 
        
        user = User.create_user_object(result[0])
        if (user.check_password(password)):
            return user 
        else:
            return False
    
    def find(username):
        connection = psycopg2.connect('dbname=sih_2023')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE USERNAME = \'{}\';".format(username))
        results = cursor.fetchall()
        connection.commit()
        connection.close()

        if not results:
            return False 
        

        return User.create_user_object(results[0])

    def __init__(self, username, password, mail, phone, user_type, password_digest=None, session_token=None) -> None:
        self.username = username
        self.password = password 
        self.mail = mail 
        self.phone = phone 
        self.user_type = user_type
        self.password_digest = password_digest or self.__create_password_digest()
        
        if type(self.password_digest) != bytes:
            self.password_digest = None
        
        self.session_token = session_token
        self.errors = []

    def create(self):
        if self.valid():
            self.session_token = self.__generate_session_token()
            connection = psycopg2.connect('dbname=sih_2023')
            cur = connection.cursor()

            cur.execute("""INSERT INTO users VALUES(
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,  
                    %s
            );""", (self.username, self.password_digest.decode('utf-8'), self.mail, self.phone, self.user_type, self.session_token))
            connection.commit()
            connection.close()
            return User.create_user_object([self.username, self.password_digest.decode('utf-8'),  self.mail, self.phone, self.user_type, self.session_token]) 
        else:
            return False

    def valid(self):
        if type(self.username) != str:
            self.errors.append('Username must be a string.')
            return False 
        elif self.username == None:
            self.errors.append('Username can not be empty.') 
            return False
        elif len(self.password) < 6:
            self.errors.append('Password is too short.')
            return False 
        elif self.type not in ['educator', 'designer', 'admin']:
            self.errors.append('Invalid user type.')
            return False 

        return True
    
    def check_password(self, password):
        return bcrypt.checkpw(bytes(password, 'utf-8'), self.password_digest)
    
    def reset_session_token(self):
        self.session_token = self.__generate_session_token()
        connection = psycopg2.connect('dbname=sih_2023')
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET session_token = \'{}\' WHERE username = \'{}\''.format(self.session_token, self.username))
        connection.commit()
        connection.close()
        return self.session_token

    # private

    def __create_password_digest(self):
        b_password = bytes(self.password, 'utf-8')
        hashed_password = bcrypt.hashpw(b_password, bcrypt.gensalt())
        return hashed_password
    
    def __generate_session_token(self):
        return secrets.token_urlsafe(16)

# User('Raghap', 'Password', 'raghapb34n@gmail.com', '9315755933', 'educator').create()