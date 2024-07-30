import os
import time

from flask import Flask, render_template, request
from flask_mail import Mail
from dotenv import load_dotenv
from my_modules import send_email, calculate_age


load_dotenv()

CURRENT_DIR = os.getcwd()
BLOG_DIR = CURRENT_DIR+"/templates/blog"
LIST_OF_ARTICLES_HTML = os.listdir(BLOG_DIR)
LIST_OF_ROUTES = ["/" + file_name[:-5] for file_name in LIST_OF_ARTICLES_HTML]

app = Flask(__name__)

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

mail = Mail(app)



@app.route("/")
def home():    
    age = calculate_age()
    return render_template('index.html', my_age=age)

@app.route("/blog")
def get_blog():
    return render_template("blog.html", list_of_articles = LIST_OF_ROUTES)


@app.route("/projects")
def get_projects():
    return render_template("projects.html")


@app.route("/publications")
def get_publications():
    return render_template("publications.html")


@app.route('/about/my_resume')
def get_resume():
    return render_template('my_resume.html')

@app.route('/about/mon_cv')
def get_cv():
    return render_template('mon_cv.html')

@app.route("/contact", methods=["GET", "POST"])
def get_in_touch():

    if request.method == 'POST':
        name = request.form['name'];
        email = request.form['email']
        title = request.form['subject']
        message_text = request.form["message"]

        send_email(name, email, title, message_text, mail)

        return render_template('message_sent.html', success_message=True)
        
    return render_template("contact.html")

def make_blog_article(route, article_html):
    def blog_article():
        file_path = os.path.join(BLOG_DIR, article_html)
        creation_date = os.path.getctime(file_path)
        creation_date = time.strftime('%B %Y', time.localtime(creation_date))
        return render_template("blog/" + article_html, 
                               article_title=article_html[:-5].replace("_", " ").title(), 
                               pub_date=creation_date)
    blog_article.__name__ = f"blog_article_{route.strip('/')}"  # unique function name
    return blog_article

for route, article_html in zip(LIST_OF_ROUTES, LIST_OF_ARTICLES_HTML):
    app.route("/blog" + route)(make_blog_article(route, article_html))
if __name__=="__main__":
    app.run(debug=True)