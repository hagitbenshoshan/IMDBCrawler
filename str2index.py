__author__ = 'melo'
"""
input a xml file of review
output
  1. the word index
  2. the file formated as word index of features id pos/neg f1:1 f2:1 ...
  3. user list user[TAB]reviewID
  4. prod list movie[TAB]reviewID
"""
from nltk.tokenize import TreebankWordTokenizer
from IMDBTypes import *
out_dir="/home/melo/work/collectiveSA_java/data/imdb_gao"
wordInd_file=out_dir+"/word.index"
feat_file=out_dir+"/feat.txt"
user_file=out_dir+"/user"
prod_file=out_dir+"/prod"

xml_file="review.xml"
wordDict=dict()
tokenizer=TreebankWordTokenizer()
reviewReader=ReviewReader(xml_file)
review=reviewReader.readReview()
while review!=None:
    content=review._doc
    tokens=tokenizer.tokenize(content)
    for token in tokens:
        if not wordDict.has_key(token):
            wordDict[token]=len(wordDict)
    review=reviewReader.readReview()
reverseInd=dict()
for word in wordDict.keys():
    reverseInd[wordDict[word]]=word
wordInd_out=open(wordInd_file,"w")
for i in range(len(reverseInd)):
    wordInd_out.write(reverseInd[i]+"\n")
wordInd_out.close()

feat_out=open(feat_file,"w")
user_out=open(user_file,"w")
prod_out=open(prod_file,"w")
reviewReader=ReviewReader(xml_file)
review=reviewReader.readReview()
while review!=None:
    content=review._doc
    user=review._user
    movie=review._movie
    if review._rating>5:
        polarity="1"
    else:
        polarity="-1"
    tokens=tokenizer.tokenize(content)
    feat_out.write(user+"@"+movie+" "+polarity)
    feats=set()
    for token in tokens:
        feats.add(wordDict[token])
    feats_list=sorted(list(feats))
    for feat in feats_list:
        feat_out.write(" "+str(feat)+":1")
    feat_out.write("\n")
    user_out.write(user+"\t"+user+"@"+movie+"\n")
    prod_out.write(movie+"\t"+user+"@"+movie+"\n")
    review=reviewReader.readReview()
feat_out.close()
user_out.close()
prod_out.close()
