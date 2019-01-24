__author__ = 'alemaxona'


from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Configuration


app = Flask(__name__, template_folder='templates')
app.config.from_object(Configuration)
db = SQLAlchemy(app)


# !!!
from model import *  # Этот импорт должен быть минимум тут! Так как если импортировать раньше,
# то не успеет создаться объкт db, и соответственно классы из модуля- model!
# Также необходимо импотировать все (*). Так как выскакивает ошибка. Видимо, зацикливание...


@app.route('/', methods= ['GET', 'POST'])
def index():

    from form import ArticleForm, CommentForm
    from model import Article, Comment

    if request.method == 'POST':
        form = ArticleForm(request.form)
        if form.validate():
            user_post = Article(**form.data)
            db.session.add(user_post)
            db.session.commit()
            return 'Post created.'
        else:
            return 'Form not valid.'
    else:
        if Article.query.count() == 0:
            return 'Posts not found.'
        else:
            posts = Article.query.all()
            for column in posts:
                author = column.author
                title = column.title
                print(author, title)
            return render_template('Article.txt', posts=posts)


if __name__ == "__main__":
    db.create_all()
    app.run()
