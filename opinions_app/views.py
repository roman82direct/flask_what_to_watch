from random import randrange

from flask import abort, flash, jsonify, redirect, render_template, url_for


from . import app, db
from .forms import OpinionForm
from .models import Opinion

@app.route('/')
def index_view():
    count = Opinion.query.count()
    if not count:
        abort(500)
    return render_template(
        'opinion.html', opinion=Opinion.query.offset(randrange(count)).first()
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
        text = form.text.data
        if Opinion.query.filter_by(text=text).first() is not None:
            flash('Такое мнение уже было оставлено ранее!', 'message')
            return render_template('add_opinion.html', form=form)
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)
