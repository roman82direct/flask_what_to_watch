from flask import jsonify, request

from . import app, db
from .models import Opinion
from .views import random_opinion


@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    # Получить объект по id или выбросить ошибку 404.
    opinion = Opinion.query.get_or_404(id)
    print(opinion.title)
    # Конвертировать данные в JSON и вернуть JSON-объект и HTTP-код ответа.
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    data = request.get_json()
    opinion = Opinion.query.get_or_404(id)
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    db.session.delete(Opinion.query.get_or_404(id))
    db.session.commit()
    # При удалении принято возвращать только код ответа 204.
    return '', 204


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    return jsonify(
        {'opinions': [opinion.to_dict() for opinion in Opinion.query.all()]}
    ), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    # Получить данные из запроса в виде словаря.
    data = request.get_json()
    # Создать новый пустой экземпляр модели.
    opinion = Opinion()
    # Наполнить экземпляр данными из запроса.
    opinion.from_dict(data)
    # Добавить новую запись в сессию.
    db.session.add(opinion)
    # Сохранить изменения.
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/get-random-opinion/', methods=['GET'])
def get_random_opinion():
    return jsonify({'opinion': random_opinion().to_dict()}), 200
