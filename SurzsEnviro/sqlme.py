import sqlite3

### This is an absolute nightmare for me, so i will be putting it off till we crack Marlin. Until then, remember that this is for SQLi-ing databases, similar to sqlmap. but in house :D Please only use for education and testing purposes, and not for any malicious intent. No one wants to be THAT asshole.

# TODO: - Implement basic SQLi payloads for common databases (MySQL, PostgreSQL, SQLite)
#   [ ]    - Add functionality to extract data from the database (e.g., tables, columns, data)
#   [ ]    - Add support for different types of SQLi (e.g., blind, union-based)
#   [ ]    - Create a user-friendly interface for interacting with the tool
#   [ ]    - Implement logging and reporting features
def GetDBStatus(database_path):
    """Checks the status of the database and prints out basic information."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("[*] Database Tables:")
    for table in tables:
        print(f" - {table[0]}")
    conn.close()

