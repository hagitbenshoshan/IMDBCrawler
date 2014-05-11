__author__ = 'melo'
from BeautifulSoup import BeautifulSoup as BS
import BeautifulSoup
from IMDBTypes import IMDBReview
import HTMLParser
import urllib2
from mySQLWrapper import Database
import json
import re
import time
from socket import error as SocketError

htmlParser=HTMLParser.HTMLParser()
usefulPattern=re.compile("\d* out of \d* people found the following review useful:",re.IGNORECASE)
MONTH={"January","February","March","April","May","June","July","August","September","October","November","December"}
def extractHead(tag):
    useful=(0,0)
    time=""
    title=""
    rating=None
    userID=None
    movieID=None
    generator=tag.childGenerator()
    while True:
        try:
            child=generator.next()
        except Exception,e:
            break
        if isinstance(child,BeautifulSoup.Tag) and child.name=="small" and usefulPattern.match(child.string)!=None:
            splits=child.string.split(" ")
            useful=(int(splits[0]),int(splits[3]))
        elif isinstance(child,BeautifulSoup.Tag) and child.name=="h2":
            if child.string!=None:
                title=child.string.replace('"',"''")
        elif isinstance(child,BeautifulSoup.Tag) and child.name=="img":
            attrs=child.attrs
            for attr in attrs:
                if attr[0]=="alt":
                    rating=int(attr[1].split("/")[0])
        elif isinstance(child,BeautifulSoup.Tag) and child.findChild()!=None and child.findChild().name=="a":
            attrs=child.findChild().attrs
            for attr in attrs:
                if attr[0]=="href" and attr[1].startswith("/user/ur"):
                    userID=attr[1].split("/")[-2]
                elif attr[0]=="href" and attr[1].startswith("/title/tt"):
                    movieID=attr[1].split("/")[-2]
        elif isinstance(child,BeautifulSoup.Tag) and child.name=="a":
            attrs=child.attrs
            for attr in attrs:
                if attr[0]=="href" and attr[1].startswith("/user/ur"):
                    userID=attr[1].split("/")[-2]
                elif attr[0]=="href" and attr[1].startswith("/title/tt"):
                    movieID=attr[1].split("/")[-2]
        elif isinstance(child,BeautifulSoup.Tag) and child.string!=None and len(child.string.split(" "))>2 and child.string.strip().split(" ")[1] in MONTH:
            time=child.string
    return (userID, movieID, title, rating, time, useful)


def findReviews_fromMovie(soup,movieID):
    """
    return the reviews movieIDs and userIDs
    """
    reviews=[]
    hr_tags=soup.findAll("hr")
    i=0
    while i<(len(hr_tags)-6):
        i+=1
        head=hr_tags[i].findNextSibling()
        body=head.findNextSibling()
        userID,tmp,title,rating,time,useful=extractHead(head)
        if userID==None or rating==None:
            print "throw one review!",head
            reviews.append(None)
            continue
        content=""
        body_gen=body.childGenerator()
        while True:
            try:
                tag=body_gen.next()
            except StopIteration,e:
                break
            if tag==None:
                break
            if isinstance(tag,BeautifulSoup.Tag) and tag.name=="br":
                content+="\n"
            elif isinstance(tag,BeautifulSoup.NavigableString):
                try:
                    tag_str=htmlParser.unescape(tag.string).replace("\n"," ")
                    content+=tag_str
                except UnicodeEncodeError,e:
                    print e
            else:
                raise Exception("not recognizable tag",+tag.prettify())
        content=content.replace('"',"''")
        review=IMDBReview(json.dumps(content),title,userID,movieID,rating,time,useful)
        reviews.append(review)
    return reviews
def findReviews_fromUser(soup,userID):
    reviews=[]
    hr_tags=soup.findAll("hr")
    if len(hr_tags)<4:
        return reviews
    body=hr_tags[0]
    while True:
        head=body.findNextSibling()
        if head!=None and head.name=="hr":
            break
        body=head.findNextSibling()
        while True:
            if body.name=="p" and (body.findChild()==None or body.findChild().name=="br"):
                break
            body=body.findNextSibling()
        tmp,movieID,title,rating,time,useful=extractHead(head)
        if movieID==None or rating==None:
            print "throw one review!",head
            reviews.append(None)
            continue
        bgen=body.childGenerator()
        content=""
        while True:
            try:
                tag=bgen.next()
            except StopIteration,e:
                break
            if tag==None:
                break
            if isinstance(tag,BeautifulSoup.Tag) and tag.name=="br":
                content+="\n"
            elif isinstance(tag,BeautifulSoup.NavigableString):
                try:
                    tag_str=htmlParser.unescape(tag.string).replace("\n"," ")
                    content+=tag_str
                except UnicodeEncodeError,e:
                    print e,tag.string
            else:
                print "not recognizable tag"+tag.prettify()
                continue
        content=content.replace('"',"''")
        review=IMDBReview(json.dumps(content),title,userID,movieID,rating,time,useful)
        reviews.append(review)
    return reviews
def crawlMovie(movieID):
    print " crawling movie",movieID,"...",
    reviewList=[]
    start=0
    while True:
        html=None
        num_sleep=0
        while html==None:
            if num_sleep>3:
                return reviewList
            time.sleep(2)
            try:
                response=urllib2.urlopen("http://www.imdb.com/title/"+movieID+"/reviews?order=date&start="+str(start))
            except urllib2.HTTPError,e:
                print e,"Sleep 30 secs."
                time.sleep(30)
                num_sleep+=2
                continue
            except SocketError,e:
                print e,"speep 1 min"
                time.sleep(60)
                num_sleep+=3
                continue
            html=response.read()
        soup=BS(html,convertEntities=BS.HTML_ENTITIES)
        revs=findReviews_fromMovie(soup,movieID)
        for review in revs:
            if review!=None:
                reviewList.append(review)
        if len(revs)==10:
            start+=10
            continue
        else:
            break
    print "collected",len(reviewList),"reviews"
    return reviewList
def crawlUser(userID):
    print " crawling user",userID,"...",
    reviewList=[]
    start=0
    while True:
        html=None
        num_sleep=0
        while html==None:
            if num_sleep>3:
                return reviewList
            time.sleep(2)
            try:
                response=urllib2.urlopen("http://www.imdb.com/user/"+userID+"/comments?order=date&start="+str(start))
            except urllib2.HTTPError,e:
                print e,"Sleep 30 secs."
                time.sleep(30)
                num_sleep+=2
                continue
            except SocketError,e:
                print e,"speep 1 min"
                time.sleep(60)
                num_sleep+=3
                continue
            html=response.read()
        soup=BS(html,convertEntities=BS.HTML_ENTITIES)
        revs=findReviews_fromUser(soup,userID)
        for review in revs:
            if review!=None:
                reviewList.append(review)
        if len(revs)==10:
            start+=10
            continue
        else:
            break
    print "collected",len(reviewList),"reviews"
    return reviewList

db=Database()
task=db.popTask()
while task!=None:
    if task.startswith("ur"):
        review_list=crawlUser(task)
    elif task.startswith("tt"):
        review_list=crawlMovie(task)
    new_tasks=set()
    for review in review_list:
        new_tasks.add(review._user)
        new_tasks.add(review._movie)
        db.insertReview(review._user,review._movie,review._doc,review._title,review._rating,review._useful,review._time)
    for new_task in new_tasks:
        db.addTask(new_task)
        if new_task.startswith("ur"):
            db.insertUser(new_task,"")
        elif new_task.startswith("tt"):
            db.insertMovie(new_task,"","")
    task=db.popTask()
