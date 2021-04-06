import pymysql
from config.readConfig import ReadConfig
from tools.report import log_tool


class myDB:
    global host,username,password,port,database,config
    host =ReadConfig().get_db("host")
    username = ReadConfig().get_db("username")
    password = ReadConfig().get_db("password")
    database = ReadConfig().get_db("database")
    port =ReadConfig().get_db("port")
    config ={
        'host':str(host),
        'user':username,
        'password': password,
        'port':int(port),
        'database':database
    }
    def __init__(self):
        self.db = None
        self.cursor =None

    def connectDB(self):
        try:
            #连接数据库
            self.db=pymysql.connect(**config)
            #创建游标
            self.cursor=self.db.cursor()
            log_tool.info("连接数据成功")
        except ConnectionError as e:
            log_tool.error(str(e))

    def executeSQL(self,sql,params):
         self.connectDB()
         #游标下执行sql
         self.cursor.execute(sql,params)
         #提交游标数据到数据库
         self.db.commit()
         return self.cursor

    def get_one(self,cursor):
        value=cursor.fetchone()[0]
        return value

    def get_all(self,cursor):
        value=cursor.fetchall()
        return value

    def closeDB(self):
        self.db.close()
        log_tool.info("数据库关闭")

if __name__=="__main__":

    # sql="select id from order_case where code=%s"
    # params="2103250200000001"
    # a=myDB().excuteSQL(sql,params=params)
    # res=myDB.get_one(a)
    # print(res)

    test = myDB()

    sql="SELECT id FROM order_case LEFT JOIN event ON order_case.event_id=event.event_id WHERE event.code=%s"
    params ="2103250200000001"
    a = myDB().executeSQL(sql=sql,params=params)
    res=myDB().get_one(a)
    print(res)