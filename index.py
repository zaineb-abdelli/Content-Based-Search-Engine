from flask import Flask, request, render_template
import numpy as np
import pandas as np
from elasticsearch import Elasticsearch

es = Elasticsearch()
print("Connection established with elasticsearch")

def description_search(query,image):
    global es
    es.indices.refresh(index= 'data')
    results = es.search(
            index='data',
            body={
                    "size": 100,
                    "query": {
                            "match": {"Pic_cluster": query}
                            }
                    })
    print(len(results))
    if len(results) > 0:
        answers =[]
        answers = predict_img(image)
    else:
        answers = []
    return answers

import pandas as pd
import re

def ehddist(ehd1,ehd2):
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for i in range(80):
      sum1 += abs(float(ehd1[i])-float(ehd2[i]))
    for i in range(79,85):
      sum2 += abs(float(ehd1[i])-float(ehd2[i]))
    for i in range(84,150):
      sum3 += abs(float(ehd1[i])-float(ehd2[i]))
    distance = sum1 +5* sum2 + sum3
    return(distance)
def cleaning_Image(data):
    List=[]
    j=0
    c=[]
    for i in data.split(' '):
        j=j+1
        c.append(i)
    L=[]
    for e in c:
        if e=='':
            continue
        else:
            L.append(e)
    a=[]
    for el in L: 
        m=re.sub("[^0-9.]",'',el)
        if m!='':
            a.append(float(m))
    List.append(a)
    return(List[0])
#input colonne
def cleaning_data(data):   
	List=[]
	for dat in data:
		j=0
		c=[]
		for i in dat.split(' '):
			j=j+1
			c.append(i)
		L=[]
		for e in c:
			if e=='':
				continue
			else:
				L.append(e)
		a=[]
		for el in L: 
			m=re.sub("[^0-9.]",'',el)
			if m!='':
				a.append(float(m))
		List.append(a)
	return(List)

DataProject2=pd.read_csv("DataProjet2.csv")

centr=pd.read_csv("centroids.xls")
centroids=cleaning_data(centr["centroid"])

def give_class(image):
    
		distances = [ehddist(image , centroid) for centroid in centroids]
		classification=distances.index(min(distances))
		return classification

def predict_img(img):
	classe=give_class(img)
	print(classe)
	intra_distance=[]
	List_index=[el for el in DataProject2[DataProject2['Pic_cluster']== 23]['Unnamed: 0']]
	Pic_semblable=DataProject2[DataProject2['Pic_cluster']== classe]['Pic_Bins']
	Pic_semblable=cleaning_data(Pic_semblable)
	intra_distances=[ehddist(img ,pic) for pic in Pic_semblable]
	ln = len(List_index)
	i=0
	answerss=[]
	while (ln > 0) and (i<9):
		cc = List_index[intra_distances.index(min(intra_distances))] #id de l'image thrumble
		answerss.append("static/"+str(int(cc))+".jpg")
		intra_distances[intra_distances.index(min(intra_distances))] = 1000000000000000000
		i = i+1
		ln = ln-1
	return answerss

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']
        uploaded_img_path = "static/" + file.filename
        jj = int(file.filename.split('.')[0])
        #nekhou les bins mte3 l'image en se basant 3al identifiant mte7a
        p = pd.read_csv('imagesWithclusters.csv')
        # X = bins de img
        X = p.image[jj]
        X=cleaning_Image(X)
        print(len(X))
        #pred= class de img
        pred=give_class(X)
        print(pred)
        answers = description_search(str(int(pred)), X)
        return render_template('index.html',query_path=uploaded_img_path,answers=answers)
    else:
        return render_template('index.html')

if __name__=="__main__":
     app.run(debug=True)
      