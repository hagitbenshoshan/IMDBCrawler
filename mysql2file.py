__author__ = 'melo'
"""
Save the reviews from mysql into a file
"""
import pymysql
from lxml import etree
txt_file="review.xml"
if __name__=="__main__":
    conn=pymysql.connect(host="IP",user="MySQL user ID",passwd="password",db="imdb")
    cur=conn.cursor()
    cur.execute("select id from imdbUser;")
    users=cur.fetchall()
    print len(users)
    ost_r=open(txt_file,"w")
    ost_r.write("<root>\n")
    for user in users:
        cur.execute("select movie,rating,content,time,title,useful from imdbReview where user=\""+user[0]+"\";")
        rs=cur.fetchall()
        print "get",len(rs),"reviews for user",user[0]
        for r in rs:
            r_xml=etree.Element("review")
            try:
                rating_xml=etree.Element("rating")
                rating_xml.text=str(r[1])
                r_xml.append(rating_xml)
                title_xml=etree.Element("title")
                title_xml.text=r[4]
                r_xml.append(title_xml)
                content_xml=etree.Element("content")
                content_xml.text=r[2]
                r_xml.append(content_xml)
                movie_xml=etree.Element("movie")
                movie_xml.text=r[0]
                r_xml.append(movie_xml)
                user_xml=etree.Element("user")
                user_xml.text=user[0]
                r_xml.append(user_xml)
                time_xml=etree.Element("time")
                time_xml.text=r[3]
                r_xml.append(time_xml)
                useful_xml=etree.Element("useful")
                useful_xml.text=r[5]
                r_xml.append(useful_xml)
                ost_r.write(etree.tostring(r_xml,pretty_print=True)+"\n")
            except ValueError,e:
                pass
    ost_r.write("</root>")
