import pymysql

class Database():
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='gubeom',
                                  password='111111',
                                  db='testDB',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
 
    def execute(self, query):
        self.cursor.execute(query)
 
    def executeOne(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return row
 
    def executeAll(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        return row
 
    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

#CREATE TABLE user(
#    idno        INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
#    username    VARCHAR(256) NOT NULL UNIQUE,
#    password    VARCHAR(256) NOT NULL,
#    name        VARCHAR(256) NOT NULL,
#    sex         CHAR(1),
#    birth       DATE
#) CHARSET=utf8;

#INSERT INTO user (username, password, name, sex, birth)
#VALUES ('testid', '111111', '전구범', 0, '1990-09-20');