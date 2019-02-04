# -*- coding: utf-8 -*-

from datetime import date
from app import db


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    date_create = db.Column(db.Date, default=date.today)
    author = db.Column(db.String(20), nullable=True)
    title = db.Column(db.String(20), nullable=False)
    post = db.Column(db.String(500), nullable=False)

    def __str__(self):
        return 'Table article>'


class Comment(db.Model):
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False, index=True)
    date_create = db.Column(db.Date, default=date.today)
    text = db.Column(db.String(100), nullable=False)

    article = db.relationship(Article, foreign_keys=[article_id])

    def __str__(self):
        return '<Table comment>'
