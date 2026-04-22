from datetime import datetime, UTC
from random import randrange

from flask import Flask, jsonify, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'opinions_secret_key'
app.json.ensure_ascii = False

db = SQLAlchemy(app)


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(UTC)
    )


class OpinionForm(FlaskForm):
    title = StringField(
        'Введите название фильма',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    text = TextAreaField(
        'Напишите мнение',
        validators=(DataRequired(message='Обязательное поле'),)
    )
    source = URLField(
        'Добавьте ссылку на подробный обзор фильма',
        validators=[Length(1, 256), Optional()]
    )
    submit = SubmitField('Добавить')


@app.route('/')
def index_view():
    count = Opinion.query.count()
    if not Opinion.query.count():
        return 'В базе данных мнений о фильмах нет.'
    return render_template(
        'opinion.html',
        opinion=Opinion.query.offset(randrange(count)).first()
    )
    # return Opinion.query.offset(randrange(count)).first().text
    # return jsonify(
    #     [{opinion.id: opinion.text} for opinion in Opinion.query.all()]
    # )


@app.route('/opinions/<int:id>')
def opinion_view(id):
    return render_template(
        'opinion.html', opinion=Opinion.query.get_or_404(id)
    )


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    form = OpinionForm()
    if form.validate_on_submit():
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)


if __name__ == '__main__':
    app.run()
