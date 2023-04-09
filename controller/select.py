from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from repositories import select

import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def create_item():
    return select.create_item()


def get_items_on_country():
    return select.get_items_on_country()


def insert_items_on_country(values):
    count = -1
    for a in values:
        name = a["name"]
        flag = a["flag"]
        population = a["population"]
        count = count + 1
        result = select.insert_items_on_country(count, name, flag, population)
    return result


def update_item(values):
    old_name = values[0]["old_name"]
    new_name = values[0]["new_name"]
    if str == type(old_name) and str == type(new_name) and select.update_item(old_name, new_name):
        return True

    else:
        return False


def country_name(username):
    result = select.country_name(username)
    if result:
        return result
    else:
        return "please enter correct values"


# random joke code

def create_randomJoke():
    return str(select.create_randomJoke())


def random_joke(values):
    print(values)
    joke = values["value"]
    if len(select.select_last_id()) == 0:
        id = 1
    else:
        max_value = select.select_last_id_randomJoke()[0]["id"]
        print(max_value)
        id = max_value + 1
    result = select.random_joke(id, joke)
    return result


# login and registration

def registration(values):
    name = values['name']
    email = values['email']
    password = values['password']
    password1 = values['password1']
    password_hash = generate_password_hash(password)
    if password == password1:
        id = 0
        if len(select.select_last_id()) == 0:
            id = 1
        else:
            max_value = select.select_last_id()[0]["id"]
            id = max_value + 1
        print(re.fullmatch(regex, email))
        if re.fullmatch(regex, email):
            result = select.insert_item(id, name, email, password_hash)
            return "successfully inserted"
        else:
            return "please enter valid email"
    else:
        return 'please enter correct password'


def get_item(email, password):
    return select.get_item(email)
