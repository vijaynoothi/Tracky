import sqlite3

con = sqlite3.connect("fleets.db")
print("Database opened successfully")

con.commit()

con.close()