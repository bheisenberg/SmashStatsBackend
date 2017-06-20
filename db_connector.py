import pymysql

user = 'root'
password = ''
db = 'smashstats'
testdb = 'test'
charset = 'utf8mb4'


def connection():
    conn = pymysql.connect(user=user, password=password, database=db)
    conn.set_charset(charset)
    return conn

def test_connection():
    conn = pymysql.connect(user=user, password=password, database=testdb)
    conn.set_charset(charset)
    return conn