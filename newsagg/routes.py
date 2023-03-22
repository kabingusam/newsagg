import random
from newsagg import *
from flask import render_template, request, send_file
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from newsagg import app
from newsapi import NewsApiClient
from dotenv import load_dotenv
import pathlib
import requests
import os
from google.oauth2 import id_token
from .models import db, User
from flask import Blueprint

bp = Blueprint('routes', __name__)

load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv('NEWS_API_KEY')
google_key = os.getenv('GOOGLE_KEY')
secret_key = os.getenv('APP_KEY')

app = Flask(__name__, template_folder='templates')

app.secret_key = secret_key

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = google_key
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback" 
)

# a function to check if the user is authorized or not
def login_is_required(function):  
    def wrapper(*args, **kwargs):
        #authorization required
        if "google_id" not in session:  
            return abort(401)
        else:
            return function()
    return wrapper

#the page where the user can login
@app.route("/login")
def login():
    # asking the flow class for the authorization (login) url
    authorization_url, state = flow.authorization_url(prompt="consent")
    session["state"] = state
    return redirect(authorization_url)

# add user to database
def add_user_to_database(db, google_id, name):
    #check if the user exists
    user = User.query.filter_by(google_id=google_id).first()

    if not user:
        # If user doesnt exist , create a new user
        user = User(google_id=google_id, username=name)
        db.session.add(user)
        db.session.commit()


#this is the page that will handle the callback process meaning process after the authorization
@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        credentials.id_token,
        token_request,
        GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")

    # retrieve the google_id and name from the session
    google_id = session.get("google_id")
    name = session.get("name")
    print(google_id)
    print(name)

    # add user to database
    # add_user_to_database(db, google_id, name)

    return redirect("/news")

#the logout page and function
@app.route("/logout")  
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
def index():
    newsapi = NewsApiClient(api_key=api_key)

    # Get random articles for section 1
    top_headlines = newsapi.get_top_headlines()
    articles = []
    for article in top_headlines['articles']:
        articles.append({
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'image_url': article['urlToImage'],
            'date': article['publishedAt'],
            'channel': article['source']['name']
        })
    random_section1_articles = random.sample(articles, 9)

    # Get random articles for section 2 (health)
    health_articles = newsapi.get_everything(q="health")
    section2_articles = []
    for article in health_articles['articles']:
        section2_articles.append({
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'image_url': article['urlToImage'],
            'date': article['publishedAt'],
            'channel': article['source']['name']
        })
    random_section2_articles = random.sample(section2_articles, 3)

    # Get random tech news for section3 (tech)
    tech_articles =  newsapi.get_everything(q="technology")
    section3_articles = []
    for article in tech_articles['articles']:
        section3_articles.append({
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'image_url': article['urlToImage'],
            'date': article['publishedAt'],
            'channel': article['source']['name']
        })
    random_section3_articles = random.sample(section3_articles, 3)
    
    return render_template('index.html', 
                           section1_articles=random_section1_articles, 
                           section2_articles=random_section2_articles, 
                           section3_articles=random_section3_articles)
# Tech news
@app.route("/tech")
def tech():
    newsapi = NewsApiClient(api_key=api_key)

    tech_articles = newsapi.get_everything(q="technology")

    # get the current page
    page = request.args.get('page', default=1, type=int)
    # define number of articles per page
    per_page = 6

    # calculate the start and end indices for the current page
    start = (page - 1) * per_page
    end = start + per_page

    main_tech_articles = []
    for article in tech_articles['articles'][start:end]:
        main_tech_articles.append({
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'image_url': article['urlToImage'],
            'date': article['publishedAt'],
            'channel': article['source']['name']
        })

    # Get the total number of articles and pages
    total_articles = len(tech_articles['articles'])
    total_pages = (total_articles + per_page - 1) // per_page

    return render_template('tech.html', main_tech_articles=main_tech_articles, base_template="base.html", page=page, total_pages=total_pages)


# fashion news
@app.route("/fashion")
def fashion():
    newsapi = NewsApiClient(api_key=api_key)

    fashion_articles = newsapi.get_everything(q="fashion")

    # get the current page
    page = request.args.get('page', default=1, type=int)
    # define number of articles per page
    per_page = 6

    # calculate the start and end indices for the current page
    start = (page - 1) * per_page
    end =  start + per_page

    main_fashion_articles = []
    for article in fashion_articles['articles'][start:end]:
        main_fashion_articles.append({
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'image_url': article['urlToImage'],
            'date': article['publishedAt'],
            'channel': article['source']['name']
        })
    # random_main_fashion_articles = random.sample(main_fashion_articles, 9)

    # calculate the total number of pages
    total_articles = len(fashion_articles['articles'])
    total_pages = (total_articles + per_page - 1)

    return render_template('fashion.html', main_fashion_articles=main_fashion_articles, base_template="base.html", page=page, total_pages=total_pages, per_page=per_page)


@app.route("/politics")
def politics():
    newsapi = NewsApiClient(api_key=api_key)

    # get the current page
    page =  request.args.get('page', default=1, type=int)
    # define the number of articles
    per_page = 6

    # calculate the start and end indices of the current page
    start = (page - 1) * per_page
    end =  start + per_page

    politics_articles = newsapi.get_everything(q="politics")
    main_politics_articles = []
    for article in politics_articles['articles'][start:end]:
        main_politics_articles.append({
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'image_url': article['urlToImage'],
            'date': article['publishedAt'],
            'channel': article['source']['name']
        })
    
    #  calculate the total number of pages
    total_artcles = len(politics_articles['articles'])
    total_pages =  (total_artcles + per_page - 1)

    return render_template('politics.html', main_politics_articles=main_politics_articles, base_template="base.html", page=page, total_pages=total_pages, per_page=per_page)


@app.route('/news')
@login_is_required
def news():
    newsapi = NewsApiClient(api_key=api_key)
    country = request.args.get('country', default='us', type=str)
    category = request.args.get('category', default='all', type=str)
    
    if category == 'all':
        top_headlines = newsapi.get_top_headlines(country=country)
    else:
        top_headlines = newsapi.get_top_headlines(country=country, category=category)
    
    page = request.args.get('page', default=1, type=int)
    per_page = 4
    start = (page - 1) * per_page
    end = start + per_page
    articles = []
    for article in top_headlines['articles'][start:end]:
        articles.append({
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'image_url': article['urlToImage']
        })

    total_articles = len(top_headlines['articles'])
    total_pages = (total_articles + per_page - 1) // per_page

    return render_template('news.html', articles=articles, country=country, category=category, base_template="base.html", page=page, total_pages=total_pages)

# Function to download the article
# def download_article(url):
#     response = requests.get(url)
#     filename = os.path.basename(url)
#     folder_path = os.path.join(os.getcwd(), 'downloads')
#     os.makedirs(folder_path, exist_ok=True)
#     file_path = os.path.join(folder_path, filename)
#     with open(file_path, 'wb') as f:
#         f.write(response.content)
#     return file_path


# @app.route('/download')
# def download():
#     url = request.args.get('url')
#     file_path = download_article(url)
#     return send_file(file_path, as_attachment=True)


if __name__ == "__main__": 
    app.run(debug=True)