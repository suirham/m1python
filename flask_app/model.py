import sqlite3
import os
from passlib.hash import scrypt



def dictionary_factory(cursor, row):
  dictionary = {}
  for index in range(len(cursor.description)):
    column_name = cursor.description[index][0]
    dictionary[column_name] = row[index]
  return dictionary


def connect(database = "database.sqlite"):
  connection = sqlite3.connect(database)
  connection.set_trace_callback(print)
  connection.execute('PRAGMA foreign_keys = 1')
  connection.row_factory = dictionary_factory
  return connection


def read_build_script():
  path = os.path.join(os.path.dirname(__file__), 'build.sql')
  file = open(path)
  script = file.read()
  file.close()
  return script


def create_database(connection):
  script = read_build_script()
  connection.executescript(script)
  connection.commit()


def fill_database(connection):
  pass


def check_password_strength(password):
  if len(password) < 12:
    raise Exception("Mot de passe trop court")
  lower = False
  upper = False
  digit = False
  special = False
  for character in password:
    if 'a' <= character <= 'z' :
      lower = True
    elif 'A' <= character <= 'Z' :
      upper = True
    elif '0' <= character <= '9' :
      digit = True
    elif character in '(~`! @#$%^&*()_-+={[}]|:;"\'<,>.?/)':
      special = True
    else:
      raise Exception("Caractère invalide")
  if not(lower and upper and digit and special):
    raise Exception('''Le mot de passe doit contenir au moins 
                    un chiffre, une minuscule, une majuscule et un caractère spécial''')


def hash_password(password):
  check_password_strength(password)
  return scrypt.using(salt_size=16).hash(password)





def get_user(connection, email, password):
  sql = '''
    SELECT * FROM users
    WHERE email = :email;
  '''
  cursor = connection.execute(sql, {'email': email})
  users = cursor.fetchall()
  if len(users)==0:
    raise Exception('Utilisateur inconnu')
  user = users[0]
  password_hash = user['password_hash']
  if not scrypt.verify(password, password_hash):
    raise Exception('Utilisateur inconnu')
  return {'id': user['id'], 'email': user['email']}


def change_password(connection, email, old_password, new_password):
  user = get_user(connection, email, old_password)
  password_hash = hash_password(new_password)
  sql = '''
    UPDATE users
    SET password_hash = :password_hash
    WHERE id = :id 
  '''
  connection.execute(sql, {
    'password_hash' : password_hash,
    'id': user['id']
  });
  connection.commit()


def update_totp_secret(connection, user_id, totp_secret):
  sql = '''
    UPDATE users
    SET totp = :totp_secret
    WHERE id = :user_id
  '''
  connection.execute(sql, {'user_id' : user_id, 'totp_secret': totp_secret})
  connection.commit()


def totp_enabled(connection, user):
  sql = '''
    SELECT * FROM users
    WHERE id = :id AND totp IS NULL
  '''
  rows = connection.execute(sql, {'id' : user['id']}).fetchall()
  return len(rows) == 0


def totp_secret(connection, user):
  sql = '''
    SELECT totp FROM users
    WHERE id = :id AND totp IS NOT NULL
  '''
  rows = connection.execute(sql, {'id' : user['id']}).fetchall()
  if len(rows) == 0:
    raise Exception("Échec de la double authentification")
  return rows[0]['totp']

def add_user(connection, email, password, activity):
  password_hash = hash_password(password)
  sql = '''
    INSERT INTO users(email, password_hash, activity)
    VALUES (:email, :password_hash, :activity);
  '''
  connection.execute(sql, {
    'email' : email,
    'password_hash': password_hash,
    'activity': activity
  })
  connection.commit()

####################################

def add_basket(connection, title, information, price, creator):
  sql = '''
    insert into basket_vegetables(title, information, price, creator)
    values (:title, :information, :price, :creator)
  '''
  connection.execute(sql, {
    'title' : title,
    'information': information,
    'price': price,
    'creator': creator
  })
  connection.commit()
  
def add_reservation(connection, sponsor, basket, quantity, jour):
  sql = 'insert into reservations(sponsor, basket, quantity, jour) values (:sponsor, :basket, :quantity, :jour)'
  connection.execute(sql, {
    'sponsor' : sponsor, 
    'basket' : basket, 
    'quantity' : quantity,
    'jour' : jour
  })
  connection.commit()

def basket_list(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM basket_vegetables"
    cursor.execute(query)
    rows = cursor.fetchall()

    result = [row for row in rows]

    return result

def user_list(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    result = [row for row in rows]

    return result

def reservation_list(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM reservations"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    result = [row for row in rows]

    return result

def get_status(connection, user):
  cursor = connection.cursor()
  query = "SELECT activity FROM users where email = :user"
  cursor.execute(query , {
    'user' : user['email']
    })
  result = cursor.fetchall()
  result = result[0]['activity']
  return result

def get_panier_user(connection, user):
  cursor = connection.cursor()
  query = "SELECT * FROM basket_vegetables where creator = :user"
  cursor.execute(query , {
    'user' : user['email']
    })
  rows = cursor.fetchall()

  result = [row for row in rows]
  return result

def get_commande_user(connection, user):
  cursor = connection.cursor()
  query = "SELECT * FROM reservations where sponsor = :user"
  cursor.execute(query , {
    'user' : user['email']
    })
  rows = cursor.fetchall()
  
  result = [row for row in rows]

  return result

def get_panier(connection, id):
    cursor = connection.cursor()
    query = "SELECT * FROM basket_vegetables WHERE id = :id"
    cursor.execute(query, {'id': id})
    row = cursor.fetchone()
    
    return row 

def get_id(connection, basket):
  cursor = connection.cursor()
  query = "SELECT id FROM basket_vegetables WHERE title = :basket"
  cursor.execute(query, {'basket': basket})
  row = cursor.fetchone()
  id = row['id']
  return id

def get_command_todo(connection, user):
  cursor = connection.cursor()
  query = '''SELECT reservations.id, reservations.sponsor, reservations.basket, reservations.quantity, reservations.jour FROM reservations, basket_vegetables 
  where basket_vegetables.creator = :user 
  and basket_vegetables.title = reservations.basket'''
  cursor.execute(query , {
    'user' : user['email']
    })
  rows = cursor.fetchall()
  
  result = [row for row in rows]
  print(result)
  return result