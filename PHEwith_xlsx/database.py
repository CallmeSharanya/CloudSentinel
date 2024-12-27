import sqlite3
#from openpyxl import load_workbook
import pandas as pd

'''workbook= load_workbook(filename=".\Database\Bank-Ledger-with-bank-details\Bankledger.xlsx")
sheet=workbook.active'''

conn=sqlite3.connect('bankexample.db')
wb=pd.read_excel('.\Database\Bank-Ledger-with-bank-details\Bankledger.xlsx', sheet_name=None)

for sheet in wb:
    wb[sheet].to_sql(sheet,conn,index=False)
conn.commit()
conn.close()    

'''cursor=conn.cursor()

cursor.execute('CREATE TABLE bankexampletable(col1 )')
for row in sheet.iter_rows'''