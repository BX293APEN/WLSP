import os, sqlite3, copy

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


if __name__ == "__main__":
    with open(f"{os.getcwd()}/bunruidb.txt", encoding="shift-jis")as f:
        data = f.read().split("\n")

    with MySQLite(
        db              = f"{os.getcwd()}/char5.db",
        table           = "words", 
        doInit          = True, 
        profile         = [
            {
                "column" : "word",
                "format" : "TEXT",
                "attribute" : ""
            }
        ]
    ) as db:
        for record in data:
            field = record.split(",")
            try:
                addWord = field[13]
                if len(addWord) == 5:
                    db.send_sql(f"""INSERT INTO words(word) VALUES("{addWord}");""")
            except Exception as e:
                print(e)
