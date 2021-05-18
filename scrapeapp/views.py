from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


# Create your views here.
def homepage(request):
    url="https://www.flipkart.com/search?q=mobiles"
    resp=requests.get(url).content
    soup=BeautifulSoup(resp,'html.parser')
    titles=soup.find_all('div',class_='_4rR01T')
    ratings=soup.find_all('div',class_='_3LWZlK')
    reviews=soup.find_all('span',class_='_2_R_DZ')
    prices=soup.find_all('div',class_='_30jeq3 _1_WHN1')
    m_titles=[]
    m_ratings=[]
    m_reviews=[]
    m_prices=[]
    for title,rating,review,price in zip(titles,ratings,reviews,prices):
        m_titles.append(title.text)
        m_ratings.append(rating.text)
        m_reviews.append(review.text)
        m_prices.append(price.text)

    data={'mobiles':m_titles,'ratings':m_ratings,'reviews':m_reviews,'prices':m_prices}
    df=pd.DataFrame(data=data)
    df.to_csv('mobile_data.csv',index=False)
    d=json.dumps(data)
    l=json.loads(d)
    with open('mobile_data.json','w')as f:
        f.write(d)
        f.close()
def get_columns(request):
    df=pd.read_csv('mobile_data.csv')
    return render(request,'get_columns.html',{'columns':df.columns,'rows':df.to_dict('records')})
