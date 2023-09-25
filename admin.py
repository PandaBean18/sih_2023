import psycopg2
from user import User
class Admin(User):
    def __init__(self, username, password, mail, phone, user_type, password_digest=None, session_token=None):
        super().__init__(username, password, mail, phone, user_type, password_digest, session_token)
        if self.user_type != 'admin':
            raise('User is not admin')

    def delete_user(self, user_session_token):
        connection = psycopg2.connect('dbname=sih_2023')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users WHERE session_token = \'{}\' AND type != \'admin\''.format(user_session_token))
        connection.commit()
        connection.close()

    def change_user_privilege(self, session_token):
        user = User.find_by_session_token(session_token)
        new_status = None
        if user.user_type == 'educator':
            new_status = 'curriculum designer'
        else:
            new_status = 'educator'
        connection = psycopg2.connect('dbname=sih_2023')
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET type = \'{}\' WHERE session_token = \'{}\' AND type != \'admin\''.format(new_status, session_token))
        connection.commit()
        connection.close() 

    def find_by_username(self, username):
        connection = psycopg2.connect('dbname=sih_2023')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = \'{}\' AND type != \'admin\''.format(username))
        results = cursor.fetchall()
        if not results: 
            return False

        return User.create_user_object(results[0])

    def users(self):
        connection = psycopg2.connect('dbname=sih_2023')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        results = cursor.fetchall()
        if not results: 
            return False

        users = []

        for result in results:
            users.append(result[0])

        return users