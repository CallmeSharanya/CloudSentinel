import sqlite3

con=sqlite3.connect('bankexample.db')
cur=con.cursor()

'''cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables=cur.fetchall()
print("Tables in the database: ", tables)

cur.execute("PRAGMA table_info(Ledger);")
schema= cur.fetchall()
print("Table schema: ", schema)'''

data=(51801504487,'Kotak Bank')
query="""UPDATE Ledger SET "Bank Account Details - A/c No."=? WHERE Name=?;"""
cur.execute(query,data)

cur.execute("SELECT * FROM Ledger")
rows=cur.fetchall()
for row in rows:
    print(row)
#print(res)

con.close()
