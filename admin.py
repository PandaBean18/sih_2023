from user import User 
import psycopg2

class Admin(User):
    def create_user_object(result):
        username = result[0]
        password_digest = bytes(result[1], 'utf-8')
        mail = result[2]
        phone = result[3]
        user_type = result[4]
        session_token = result[5]
        return Admin(username, None, mail, phone, user_type, password_digest, session_token)

    def __init__(self, username, password, mail, phone, user_type, password_digest=None, session_token=None):
        super().__init__(self, username, password, mail, phone, user_type, password_digest=None, session_token=None)
        if self.type != 'admin':
            raise('User is not admin')

    def delete_user(user_mail):
        connection = psycopg2.connect('dbname=sih_2023')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users WHERE mail = \'{}\''.format(user_mail))
        connection.commit()
        connection.close()

    def change_user_privilege(user_mail, new_status):
        connection = psycopg2.connect('dbname=sih_2023')
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET type = \'{}\' WHERE mail = \'{}\''.format(new_status, user_mail))
        connection.commit()
        connection.close() 

    
        