import csv
import sqlite3

conn = sqlite3.connect("Luna.db")
cursor = conn.cursor()

#create a table sys_commands
# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO sys_command VALUES(null,'Instagram', 'C:\\Users\\Shreeya\\OneDrive\\Desktop\\Instagram.lnk')"
# cursor.execute(query)
# conn.commit()

#create table command
# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'GitHub', 'https://github.com/')"
# cursor.execute(query)
# conn.commit()

# cursor.execute("DELETE FROM sys_command WHERE id IN (4)")
# conn.commit()

#  Verify deletion
# cursor.execute("SELECT * FROM contacts")
# print("Remaining rows:", cursor.fetchall())

#conn.close()

# testing module
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])

# Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
#desired_columns_indices = [0, 18]

# Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#      csvreader = csv.reader(csvfile)
#      for row in csvreader:
#          selected_data = [row[i] for i in desired_columns_indices]
#          cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

#   Commit changes and close connection
# conn.commit()
# conn.close()

#Insert Single contacts (Optional)
# query = "INSERT INTO contacts VALUES (null,'Amar', '+917083776020','null')"
# cursor.execute(query)
# conn.commit()

# query = 'sanskar'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])


