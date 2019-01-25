from wtforms_alchemy import ModelForm
from model import Article, Comment


class ArticleForm(ModelForm):
    class Meta:
        model = Article

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        include = ['article_id']

