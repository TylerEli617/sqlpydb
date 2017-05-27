#!/usr/bin/env python3

import sqlpydb

connection = sqlpydb.connect("DSN=SPORT;UID=sa;PWD=secret")
cursor = connection.cursor()

cursor.prepare("SELECT * FROM sysobjects")
cursor.execute_prepared()
print(cursor.fetchall())

cursor.execute("SELECT @@VERSION")
row = cursor.fetchone()
print(row)

cursor.prepare("SELECT * FROM sysobjects WHERE name = ?")
cursor.execute_prepared(("sysobjects", ))
print(cursor.fetchall())

cursor.execute("SELECT ?", ("nan ren", ))
print(cursor.fetchall())

cursor.execute("SELECT ?", (1337, ))
print(cursor.fetchall())

cursor.execute("SELECT ?, ?", ("nan ren", 1337, ))
print(cursor.fetchall())

