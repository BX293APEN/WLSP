import os, sqlite3

class MySQLite():
    def __init__(
        self, 
        db              = f"{os.path.dirname(__file__)}/sqlite3.db", 
        table           = "table", 
        doInit          = True, 
        profile         = [
            {
                "column" : "",
                "format" : "TEXT",
            }
        ]
    ):
        self.doInit     = doInit
        self.profile    = profile
        self.table      = table
        if self.doInit:
            try:
                os.remove(db)
            except:
                pass
        self.databaseHost = sqlite3.connect(database = db) # データベースとの接続
    
    def __enter__(self):
        self.database = self.databaseHost.cursor() # カーソルを作る
        if self.doInit:
            columnData = []
            for p in self.profile:
                columnData.append(f"""{p["column"]} {p.get("format", "REAL")} {p.get("attribute", "NOT NULL")}""")

            self.send_sql(f"""CREATE TABLE {self.table}({",".join(columnData)});""")
        return self
    
    def send_sql(self, sql): # SQL文送信
        self.database.execute(sql)
        self.db_commit()
        return self.database.fetchall() # タプル形式で全て取得
    
    def db_commit(self):
        self.databaseHost.commit()

    def __exit__(self, *args):
        self.db_commit()
        self.database.close()
        self.databaseHost.close()

        

class SQLiteDebug(MySQLite):
    def __init__(
        self, 
        db = f"{os.path.dirname(__file__)}/sqlite3.db"
    ):
        self.db = db
        super().__init__(
            db              = self.db,
            doInit          = False
        )
    
    def db_remove(self):
        os.remove(self.db)
    
    def db_console(self):
        searchWord = input("入力した平仮名が含まれる5文字の言葉を検索します > ")
        if searchWord.count("quit") > 0:
            return ["Bye"]
        else:
            return self.send_sql(f"""SELECT word FROM words WHERE word LIKE "%{searchWord}%";""")
            


if __name__ == "__main__":
    with SQLiteDebug(f"{os.path.dirname(__file__)}/db/char5.db") as db:
        while True:
            try:
                val = db.db_console()
                if val != ["Bye"]:
                    for rd in val:
                        print(rd[0])
                else:
                    break
            except Exception as e:
                print(e)