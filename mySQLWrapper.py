__author__ = 'melo'
import pymysql
from pymysql import cursors

class Database:
    def __init__(self):
        self.connect()
    def connect(self):
        self.con=pymysql.Connect(host="IP",user="MySQL user ID",passwd="password",db="imdb",use_unicode=True,port=3306)
        self.cur=self.con.cursor()
    def insertUser(self,uid,uname):
        if self.existUser(uid):
            #return "user exist!"
            return
        self.cur.execute('insert into imdbUser (id,username) values("'+uid+'","'+uname+'");')
        self.con.commit()
    def existUser(self,uid):
        self.cur.execute('select count(*) from imdbUser where id="'+uid+'";')
        if self.cur.fetchone()[0]==0:
            return False
        return True
    def insertMovie(self,id,title,data):
        if self.existMovie(id):
            #print "movie exist!"
            return
        self.cur.execute('insert into imdbMovie (id,title,data) values ("%s","%s","%s");' %(id,title,data))
        self.con.commit()
    def existMovie(self,id):
        self.cur.execute('select count(*) from imdbMovie where id="'+id+'";')
        if self.cur.fetchone()[0]==0:
            return False
        return True
    def insertReview(self,uid,mid,content,title,rating,useful,time=""):
        if self.existReview(uid,mid):
            #print "review exist!"
            return
        #print 'insert into imdbReview (user,movie,content,title,rating,useful,time) values ("%s","%s",%s,"%s",%d,"%s","%s");' % (uid,mid,content,title,rating,useful,time)
        self.cur.execute('insert into imdbReview (user,movie,content,title,rating,useful,time) values ("%s","%s",%s,"%s",%d,"%s","%s");' % (uid,mid,content,title,rating,useful,time))
        self.con.commit()
    def existReview(self,uid,mid):
        self.cur.execute('select count(*) from imdbReview where user="'+uid+'" and movie="'+mid+'";')
        if self.cur.fetchone()[0]==0:
            return False
        return True
    def addTask(self,str):
        if self.existTask(str):
            print "task "+str+" exist!!"
            return
        self.cur.execute('insert into taskQueue (task) values ("'+str+'");')
        self.con.commit()
    def existTask(self,str):
        self.cur.execute('select id,task,status from taskQueue where task="'+str+'";')
        if len(self.cur.fetchall())!=0:
            return True
        return False
    def popTask(self):
        self.cur.execute('select id,task from taskQueue where status = 0 limit 1')
        id,task=self.cur.fetchone()
        self.cur.execute('update taskQueue set status=1 where id='+str(id)+' and status=0;')
        self.con.commit()
        return task

db=Database()
db.addTask("tt0111161")
db.addTask("tt0343788")
db.addTask("tt0068646")
db.addTask("tt0199481")
db.addTask("tt0071562")
db.addTask("tt0118539")
db.addTask("tt0468569")
db.addTask("tt1918886")
db.addTask("tt0110912")
db.addTask("tt0119576")
db.addTask("tt0060196")
db.addTask("tt0072666")
db.addTask("tt0108052")
db.addTask("tt0106257")
db.addTask("tt0050083")
db.addTask("tt1189383")
db.addTask("tt0167260")
db.addTask("tt0105643")
db.addTask("tt0137523")
db.addTask("tt0054673")
