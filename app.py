from flask import Flask,render_template
from flask import request
import requests
from bs4 import BeautifulSoup 
from google import search


app = Flask(__name__)
@app.route("/")
def main():
    return render_template("home.html")


def behindwoods():
    movie_name = str(request.form.get("movie_name")).lower().replace(" " , "-")
    base_url = "http://www.behindwoods.com/tamil-movies/"
    page_url = base_url + movie_name + "/" + movie_name + "-review.html"
    review_page = requests.get(page_url)

    soup = BeautifulSoup(review_page.content)

    try:
        review = soup.find("div",{"class":"top_margin_15 lightblackfont_15"}).text
        rating = soup.find("span",{"itemprop":"ratingValue"}).text
        
    except(AttributeError):
        review = soup.find_all("div",{"class":"col_418_box float top_margin_15"})
        rating = soup.find("strong",{"class":"font_25 redfont"}).text.split("/")[0].replace("(","")
        review = review[1].text
    return  review,rating


def get_main_url(movie_name):
    search_term = movie_name + "movie times of india review"
    for url in search(search_term,stop=5):
        if "http://timesofindia.indiatimes.com/entertainment/tamil" in url:
            review_url = url
            break
    return review_url
    
    

def toi():
    movie_name = str(request.form.get("movie_name"))
    review_url = get_main_url(movie_name)
    review_page = requests.get(review_url)

    soup = BeautifulSoup(review_page.content)
    
    review = soup.find("div",{"class" : "Normal"}).text.split("Review")[0]
    rating = soup.find("span",{"class" : "ratingMovie"}).text.split("/")[0]
    return review,rating

@app.route("/review",methods=['GET','POST'])
def pnr():
    
    b_review,b_rating = behindwoods()
    i_review,i_rating = toi()
        
    return render_template("review_page.html",b_review = b_review,b_rating = b_rating,i_review = i_review,i_rating = i_rating)
if __name__ == "__main__":
   
    app.run()
