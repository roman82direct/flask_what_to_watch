from random import randrange

from flask import abort, flash, redirect, render_template, url_for


from . import app, db
from .dropbox import async_upload_files_to_dropbox
from .forms import OpinionForm
from .models import Opinion


def random_opinion():
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)
        opinion = Opinion.query.offset(offset_value).first()
        return opinion


@app.route('/')
def index_view():
    opinion = random_opinion()
    if opinion is None:
        abort(500)
    return render_template('opinion.html', opinion=opinion)
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
async def add_opinion_view():
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first() is not None:
            flash('Такое мнение уже было оставлено ранее!', 'message')
            return render_template('add_opinion.html', form=form)
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data,
            # images=upload_files_to_dropbox(form.images.data)
            images=await async_upload_files_to_dropbox(form.images.data)
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)
