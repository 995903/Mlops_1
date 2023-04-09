from .utils import execute_query, create_query, insert_query, update_query


# registration repository

def get_item(email):
    try:
        query = f'''select name,password,email from user_registration where email= '{email}' '''
        result = execute_query(query, 'all')
        return result
    except Exception as error:
        return error


def get_items_on_country():
    try:
        query = f'''select * from country_search '''
        result = execute_query(query, 'all')
        return result
    except Exception as error:
        return error


def create_item():
    try:
        query = ''' create table user_registration(
                    id INTEGER NOT NULL PRIMARY KEY,
                    name varchar(500),
                    email text,
                    password text ) '''
        result = create_query(query)
        return True
    except Exception as error:
        return False


def insert_item(id, name, email, password):
    try:
        query = f'''insert into user_registration(id,name,email,password)
                                    values({id},'{name}','{email}','{password}')'''
        result = insert_query(query)
        return result
    except Exception as error:
        return error


def insert_items_on_country(id, name, flag, population):
    try:
        query = f'''insert into country_search(id,name,flag,population)
                                    values({id},'{name}','{flag}',{population})'''
        result = insert_query(query)
        return True
    except Exception as error:
        print(error)
        return False


# commented code
def update_item(old_name, new_name):
    try:
        # checking old name available or not
        checking_oldName = f'''select name 
                    from country_search
                    where name='{old_name}' '''
        if execute_query(checking_oldName, 'all'):
            query = f''' update country_search 
                            set name ='{new_name}'
                                where name = '{old_name}' '''
            result = update_query(query)
            return True
        else:
            return False
    except Exception as error:
        return error


def country_name(username):
    try:
        query = f'''select * from country_search where name='{username}' '''
        result = execute_query(query, 'all')
        return result
    except Exception as error:
        return error


# random joke code
def create_randomJoke():
    try:
        query = f'''create table randomJoke(id int not null primary key,joke varchar(700) unique)'''
        result = create_query(query)
        return result
    except Exception as error:
        return error


def random_joke(id, joke):
    try:
        query = f'''insert into randomJoke(id,joke) values({id},"{joke}")'''
        result = insert_query(query)
        return True
    except Exception as error:
        print(error)
        return False


def select_last_id_randomJoke():
    try:
        query = f'''SELECT id
                        FROM randomJoke
                        WHERE id=(SELECT max(id) FROM randomJoke) '''
        result = execute_query(query, 'all')
        return result
    except Exception as error:
        return error


def select_last_id():
    try:
        query = f'''SELECT id
                        FROM user_registration
                        WHERE id=(SELECT max(id) FROM user_registration) '''
        result = execute_query(query, 'all')
        return result
    except Exception as error:
        return error
