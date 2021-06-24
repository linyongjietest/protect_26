#需求：
"""
1.创建查询和修改的方法
2.把上面创建的方法抽象一个类，专门做数据库的操作
"""
"""
cursor用来执行命令的方法:
1.callproc(self, procname, args):用来执行存储过程,接收的参数为存储过程名和参数列表,返回值为受影响的行数
2.execute(self, query, args):执行单条sql语句,接收的参数为sql语句本身和使用的参数列表,返回值为受影响的行数
3.executemany(self, query, args):执行单条sql语句,但是重复执行参数列表里的参数,返回值为受影响的行数
4.nextset(self):移动到下一个结果集
"""
import pymysql                      #用于连接python与mysql的包，已通过pip install pymysql命令安装
from setting import DB_CONFIG       #调用setting.py中DB-CONFIG字典   

class Mysql(object):

    def __init__(self):
    #创建数据库对象
        self.conn = pymysql.connect(**DB_CONFIG)            #mysql连接信息存储在DB-CONFIG字典中

    #实现查询方法
    def get_all(self,sql):
        try:
            #cursor= self.conn.cursor();
            #cursor：通过cursor实现对数据库的操作
            with self.conn.cursor() as cursor:    # with创建连接的时候也会把连接自动关闭，所以finally下cursor.close()可以省略不写
                cursor.execute(sql)               #执行sql语句
                result = cursor.fetchall()   #fetchall():查询所有数据,返回数据集
                return result
        except Exception as e:
            print(e)
        finally:
            if self.conn:       #判断：当连接self.conn创建成功才能close
            #cursor.close()     #前面使用with方法，此处可以省略
               self.conn.close()   #关闭数据库连接

    #实现修改方法：需要提交
    def update(self,sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                #手工提交   commit（）
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()     #回滚，执行多条sql语句只要一条失败就回滚到原来的状态
            print(e)
        finally:
                if self.conn:
                    self.conn.close()

if __name__ == '__main__':    #main方法：代码执行入口，代表从这执行
    sql = "select *from students where age = 30"
    # sql1 = "update students set age=52 where studentNo = 4"
    m=Mysql()
    print(m.get_all(sql))
    # m.update(sql1)