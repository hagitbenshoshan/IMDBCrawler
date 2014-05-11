__author__ = 'melo'
import json

"""
    This file describe the basic objects:
    Review
    Movie
    User
"""

class IMDBReview:
    def __init__(self,doc,title,user,movie,rating,time,useful):
        self._id=movie+"&"+user
        self._doc=doc
        self._title=title
        self._user=user
        self._movie=movie
        self._time=time
        self._rating=rating
        self._useful=useful
    def json_dump(self):
        return json.dump([self._id,self._doc,self._title,self._rating,self._user,self._movie,self._time,self._useful])
        pass
    def json_load(self,str):
        data=json.loads(str)
        self._doc=data[0]
        self._title=data[1]
        self._rating=data[2]
        self._user=data[3]
        self._movie=data[4]
        self._time=data[5]
        self._useful=data[6]
        self._id=self._movie+"&"+self._user
    def __str__(self):
        return "Review id:"+self._id+"\n"+\
                "rating:"+str(self._rating)+\
                "content:"+self._doc+"\n"
    def __repr__(self):
        return self.__str__()
class IMDBMovie:
    def __init__(self,id,title,data):
        self._id=id
        self._title=title
        self._data=data
    def json_dump(self):
        return json.dump([self._id,self._title,self._data])
        pass
    def json_load(self,str):
        data=json.loads(str)
        self._id=data[0]
        self._title=data[1]
        self._data=data[2]
class IMDBUser:
    def __init__(self,id,username):
        self._id=id
        self._username=username
    def json_dump(self):
        return json.dump([self._id,self._username])
        pass
    def json_load(self,str):
        data=json.loads()
        self._id=data[0]
        self._username=data[1]
class ReviewReader:
    def __init__(self,file_str):
        self.infile=open(file_str)
        self.remain=self.infile.readline()
        ind=self.remain.index("<root>")
        self.remain=self.remain[ind+len("<root>"):]
    def readReview(self):
        line=self.remain
        while line.find("</review")==-1:
            tline=self.infile.readline()
            if tline=="":
                return None
            line+=tline
        ind_start=line.index("<review>")+len("<review>")
        ind_end=line.index("</review>")
        review_str=line[ind_start:ind_end]
        self.remain=line[ind_end+len("</review>"):]
        user=review_str[(review_str.index("<user>")+6):review_str.index("</user>")]
        rating=int(review_str[(review_str.index("<rating>")+8):review_str.index("</rating>")])
        title=review_str[(review_str.index("<title>")+7):review_str.index("</title>")]
        content=review_str[(review_str.index("<content>")+9):review_str.index("</content>")]
        movie=review_str[(review_str.index("<movie>")+7):review_str.index("</movie>")]
        time=review_str[(review_str.index("<time>")+6):review_str.index("</time>")]
        useful=review_str[(review_str.index("<useful>")+8):review_str.index("</useful>")]
        return IMDBReview(content,title,user,movie,rating,time,useful)
    def close(self):
        self.infile.close()
        self.remain=None