#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()  
    return jsonify([bakery.to_dict() for bakery in all_bakeries])  


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)  
    return jsonify(bakery.to_dict())  


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    goods_list = [good.to_dict() for good in goods]

    return jsonify(goods_list)  


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Query the database for the most expensive baked good
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    # Check if a baked good was found
    if most_expensive_good:
        return jsonify(most_expensive_good.to_dict())
    else:
        return jsonify({"message": "No baked goods found"}), 404


if __name__ == '__main__':
    app.run(port=5555, debug=True)
