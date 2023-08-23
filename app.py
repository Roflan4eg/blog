from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


# _________________________________ POST DATA _________________________________
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

# _________________________________ home page _________________________________

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

# _________________________________ about page _________________________________

@app.route('/about')
def about():
    return render_template("about.html")


# _________________________________ posts page _________________________________
@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


# _________________________________ post detail _________________________________
@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get_or_404(id)
    return render_template("post-detail.html", article=article)


# _________________________________ delete post _________________________________
@app.route('/posts/<int:id>/del')
def delete_post(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


# _________________________________ update post _________________________________
@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def update_post(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect(f'/posts/{article.id}')

        except:
            return "При обновлении статьи произошла ошибка"

    return render_template("update.html", article=article)


# _________________________________ create post _________________________________
@app.route('/create-article', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title,
                          intro=intro,
                          text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')

        except:
            return "При добавлении статьи произошла ошибка"

    return render_template("create-article.html")


if __name__ == "__main__":
    app.run(debug=True)
