IMDBCrawler
============
<h2>This project crawls reviews from imdb.com and save them into a
mysql database</h2>
At initial, 10 top movies and 10 bottom movies are given as seeds.
For each review it crawled, it will add the unseen user or movie to
the taskqueue.

Before running, you have to build the tables in mysql and change the
<b>host, passward</b> and <b>userID</b>  
(line <b>9</b> in mySQLWrapper.py and line <b>9</b> in mysql2file.py).
```python
conn=pymysql.connect(host="IP",user="MySQL user ID",passwd="password",db="imdb")
```

The main fuction files:
```python
crawler.py     -  crawl the reviews
mysql2file.py  -  output the reviews in mysql database to an xml
format file
str2index.py   -  given a xml format file of reviews, output the word
index file for each instance(review), user file recording the user and movie
file recording the movie 
```

The Mysql database contains four main tables, imdbReview, imdbUser,
imdbMovie, queueTask
The descs are:
<b>imdbReview</b>
```cmd
+---------+---------------+------+-----+---------+-------+
| Field   | Type          | Null | Key | Default | Extra |
+---------+---------------+------+-----+---------+-------+
| user    | varchar(20)   | YES  | MUL | NULL    |       |
| movie   | varchar(20)   | YES  | MUL | NULL    |       |
| rating  | int(1)        | YES  |     | NULL    |       |
| useful  | varchar(10)   | YES  |     | NULL    |       |
| time    | varchar(20)   | YES  |     | NULL    |       |
| title   | varchar(100)  | YES  |     |         |       |
| content | varchar(5000) | YES  |     |         |       |
+---------+---------------+------+-----+---------+-------+
```

<b>taskQueue</b>
```cmd
+--------+---------------------+------+-----+---------+----------------+
| Field  | Type                | Null | Key | Default | Extra         |
+--------+---------------------+------+-----+---------+----------------+
| id     | int(10) unsigned    | NO   | PRI | NULL    | auto_increment |
| task   | varchar(20)         | YES  |     | NULL    |		       |
| status | tinyint(3) unsigned | NO   |     | 0       |		       |
+--------+---------------------+------+-----+---------+----------------+
```

<b>imdbMovie</b>
```cmd
+-------+----------------+------+-----+---------+-------+
| Field | Type           | Null | Key | Default | Extra |
+-------+----------------+------+-----+---------+-------+
| id    | varchar(20)    | YES  | MUL | NULL    |       |
| title | varchar(100)   | YES  |     | NULL    |       |
| data  | varchar(55534) | YES  |     | NULL    |       |
+-------+----------------+------+-----+---------+-------+
```

<b>imdbUser</b>
```cmd
+----------+--------------+------+-----+---------+-------+
| Field    | Type         | Null | Key | Default | Extra |
+----------+--------------+------+-----+---------+-------+
| id       | varchar(20)  | YES  | MUL | NULL    |       |
| username | varchar(100) | YES  |     | NULL    |       |
+----------+--------------+------+-----+---------+-------+
```
