#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>', methods = ['GET', 'PATCH'])
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()

    # bakery_serialized = bakery.to_dict()
    # return make_response ( bakery_serialized, 200  )
    if bakery == None:
        response_body ={
            "message" : "This Bakery doesnt exitst. Please try again"
        }
        response = make_response(response_body, 404)

        return response
    else:
        if request.method == "GET":
            bakeries_dict = bakery.to_dict()
        
            response = make_response(
            bakeries_dict,
            200
            )
            return response
    
        elif request.method == "PATCH":
            for attr in request.form:
                setattr(bakery, attr, request.form.get(attr))
                
            db.session.add(bakery)
            db.session.commit()

            bakery_dict = bakery.to_dict()
            response = make_response(
                bakery_dict,
                200
            )
            return response
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

@app.route('/baked_goods', methods =['GET', "POST", 'DELETE'])
def baked_goods():
    if request.method == "GET":
        baked_goods=[]
        for bg in BakedGood.query.all():
            bg_dict= bg.to_dict()
            baked_goods.append(bg_dict)
        response = make_response(
            baked_goods, 
            200
        )
        return response
    elif  request.method == "POST":
        
        new_baked= BakedGood(
            name = request.form.get('name'),
            price = request.form.get('price'),
            created_at = request.form.get('created_at'),
            updated_at = request.form.get('updated_at'),)
    
        db.session.add(new_baked)
        db.session.commit()
        
        baked_goods_dict = new_baked.to_dict()

        response = make_response(
            baked_goods_dict, 
            201
        )
        return response
    
@app.route( '/baked_goods/<int:id>', methods = ["GET", "PATCH", "DELETE"])
def baked_goods_by_id(id):
    bg_by_id= BakedGood.query.filter(BakedGood.id == id).first()

    if bg_by_id == None:
        response_body ={
            "message" : "This baked good doesnt exist"

        }
        response = make_response(response_body, 404)
        return response
    else:
        if request.method == 'GET':
            bg_dict = bg_by_id.to_dict()
            response = make_response(
                bg_dict,
                200
            )
            return response
        
        elif request.method == "DELETE":
            db.session.delete(bg_by_id)
            db.session.commit()

            response_body ={
                "delete_successful": True,
                "message": "Baked good deleted"
            }
            response = make_response(
                response_body,
                200
                 )
            return response
if __name__ == '__main__':
    app.run(port=5555, debug=True)