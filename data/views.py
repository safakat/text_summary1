from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import urllib.request
import nltk
import re
import sqlite3
import json
# Create your views here.

def text0(request):
    if "GET" == request.method:
        return render(request,"data/take_text.html")
    elif request.POST:
        url0 = request.POST['url0']
        scraped_data = urllib.request.urlopen(url0)
        article = scraped_data.read()
        
        parsed_article = BeautifulSoup(article,'lxml')
        paragraphs = parsed_article.find_all('p')
        
        article_text = ""
        
        for p in paragraphs:
            article_text += p.text
            article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
            article_text = re.sub(r'\s+', ' ', article_text)
            
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        sentence_list = nltk.sent_tokenize(article_text)
        stopwords = nltk.corpus.stopwords.words('english')
        
        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
             if word not in stopwords:
                  if word not in word_frequencies.keys():
                       word_frequencies[word] = 1
                  else:
                       word_frequencies[word] += 1
        maximum_frequncy = max(word_frequencies.values())
        for word in word_frequencies.keys():
             word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
             sentence_scores = {}
        
        for sent in sentence_list:
             for word in nltk.word_tokenize(sent.lower()):
                  if word in word_frequencies.keys():
                       if len(sent.split(' ')) < 30:
                            if sent not in sentence_scores.keys():
                                 sentence_scores[sent] = word_frequencies[word]
                            else:
                                 sentence_scores[sent] += word_frequencies[word]
        import heapq
        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)
        list0 = []
        list0.append((url0,summary))
        summary1 = repr(summary)
        args = {'summary':summary}
        my_db = sqlite3.connect('summary3.sqlite3')
        cur_db=my_db.cursor()
        cur_db.execute("CREATE TABLE IF NOT EXISTS data1(id INTEGER PRIMARY KEY AUTOINCREMENT,url TEXT(500),sum0 TEXT(5000));")
        sql0 = "INSERT INTO data1(url,sum0) VALUES(?,?);"
        cur_db.executemany(sql0,list0)
        my_db.commit()
        return render(request,'data/summary.html',args)

def admin0(request):
	if "GET" == request.method:
		return render(request,"data/login.html")
	elif request.POST:
		user_id = str(request.POST['user_id'])
		passwd = str(request.POST['passwd'])
		admin_db = sqlite3.connect('admin_details.sqlite3')
		admin_curs = admin_db.cursor()
		admin_curs.execute('''SELECT userid FROM details;''')
		record0 = admin_curs.fetchall()
		user_id0 = str(record0[0][0])
		admin_curs.execute('''SELECT password FROM details;''')
		record1=admin_curs.fetchall()
		passwd0 = str(record1[0][0])

		if user_id == user_id0:
			if passwd == passwd0:
				db0 = sqlite3.connect('summary3.sqlite3')
				cur_db0 = db0.cursor()
				cur_db0.execute('''SELECT id FROM data1''')
				id9 = cur_db0.fetchall()
				cur_db0.execute('''SELECT url FROM data1''')
				url9 = cur_db0.fetchall()
				cur_db0.execute('''SELECT sum0 FROM data1''')
				sum9 = cur_db0.fetchall()
				data9 = {'id':id9,'url':url9,'sum':sum9}
				args = {'data9':data9}
				return render(request,"data/template.html",args)
			return render(request,"data/login.html")
		else:
			return render(request,"data/login.html")




def temp0(request):
	db0 = sqlite3.connect('summary3.sqlite3')
	cur_db0 = db0.cursor()
	cur_db0.execute('''SELECT id FROM data1''')
	id9 = cur_db0.fetchall()
	cur_db0.execute('''SELECT url FROM data1''')
	url9 = cur_db0.fetchall()
	cur_db0.execute('''SELECT sum0 FROM data1''')
	sum9 = cur_db0.fetchall()
	data9 = {'id':id9,'url':url9,'sum':sum9}
	return HttpResponse(json.dumps(data9),content_type='application/json')
	#return render(request,"data/template.html")