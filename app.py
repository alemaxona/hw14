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

            posts = db.session.query(Article).all()
            return render_template('Article.txt', posts=posts)
        else:
            return 'Form not valid.'
    else:
        if db.session.query(Article).count() == 0:
            return 'Posts not found.'
        else:
            posts = Article.query.all()
            # for column in posts:
            #     author = column.author
            #     title = column.title
            #     print(author, title)
            return render_template('Article.txt', posts=posts)


@app.route('/<post_id>', methods=['GET', 'POST'])
def comments(post_id):

    from form import ArticleForm, CommentForm
    from model import Article, Comment

    if request.method == 'GET':
        posts = db.session.query(Article).filter_by(id=post_id)
        if posts.count() == 0:
            return 'Post not found'
        else:
            # print('posts', posts)  # ? Может выводиться запрос SQL
            comments = db.session.query(Comment.text).join(Article).filter(Article.id == Comment.article_id, ).filter_by(id=post_id)
            # print('comments', comments)
            return render_template('user_post.txt', posts=posts, comments=comments)
    else:
        form = CommentForm(request.form)
        if form.validate():
            user_comment = Comment(**form.data)
            # print(request.form.get('article_id'))  # Получаем данные воода
            if request.form.get('article_id') == post_id:
                db.session.add(user_comment)
                db.session.commit() 
                posts = db.session.query(Article).filter_by(id=post_id)
                comments = db.session.query(Comment.text).join(Article).filter(Article.id == Comment.article_id).filter_by(id=post_id)
                return render_template('user_post.txt', posts=posts, comments=comments)
            else:
                return 'Post id failed.'
        else:
            return 'Form invalid.'


if __name__ == "__main__":
    db.create_all()
    app.run()
