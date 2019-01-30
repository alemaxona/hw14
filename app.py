from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Configuration


app = Flask(__name__, template_folder='templates')
app.config.from_object(Configuration)
db = SQLAlchemy(app)
# print(dir(db))


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
            db.session.close()
            return render_template('Article.html', posts=posts)
        else:
            return 'Form not valid.'
    else:
        if db.session.query(Article).count() == 0:
            db.session.close()
            return 'Posts not found.'
        else:
            posts = db.session.query(Article).all()  # OR: posts = Article.query.all()
            # print('???', posts)
            # ??? [<Article 2>, <Article 3>, <Article 4>, <Article 5>, <Article 6>, <Article 7>, <Article 8>, <Article 9>, <Article 10>]
            
            # posts = db.session.execute("SELECT * FROM article")
            # print('???', posts)
            # ??? <sqlalchemy.engine.result.ResultProxy object at 0x047CB470>
            db.session.close() 
            return render_template('Article.html', posts=posts)


@app.route('/<int:post_id>', methods=['GET', 'POST'])
def comments(post_id):

    from form import ArticleForm, CommentForm
    from model import Article, Comment

    if request.method == 'GET':
        posts = db.session.query(Article).filter_by(id=post_id)
        # print('???', posts)
        # ??? SELECT article.id AS article_id, article.date_create AS article_date_create, article.author AS article_author, article.title AS article_title, article.post AS article_post
        # FROM article WHERE article.id = %(id_1)s

        # posts = db.session.execute("Select * from article where id = :post_id")
        if posts.count() == 0:
            db.session.close()  # Работает 
            # db.session.remove()  # Тут это работает! O_o Все это блять страннно! Помогите мне, тупому.
            return 'Post not found'
        else:
            comments = db.session.query(Comment).join(Article).filter(Article.id == Comment.article_id).filter_by(id=post_id)
            # print('???', comments)
            # SELECT comment.id AS comment_id, comment.article_id AS comment_article_id, comment.date_create AS comment_date_create, comment.text AS comment_text
            # FROM comment JOIN article ON article.id = comment.article_id
            # WHERE article.id = comment.article_id AND article.id = %(id_1)s
            db.session.close()  # Не работает
            return render_template('user_post.html', posts=posts, comments=comments)
    else:
        form = CommentForm(request.form)
        if form.validate():
            user_comment = Comment(**form.data)
            # print(request.form.get('article_id'))  # Получаем данные воода
            if request.form.get('article_id') == post_id:
                db.session.add(user_comment) 
                posts = db.session.query(Article).filter_by(id=post_id)
                comments = db.session.query(Comment.text).join(Article).filter(Article.id == Comment.article_id).filter_by(id=post_id)
                return render_template('user_post.html', posts=posts, comments=comments)
            else:
                return 'Post id failed.'
        else:
            return 'Form invalid.'


if __name__ == "__main__":
    db.create_all()
    app.run()
