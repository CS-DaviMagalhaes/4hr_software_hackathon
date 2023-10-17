from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.mysql import MySQL
from flask_restful import Resource, Api

app = Flask(__name__)

CORS(app)

mysql = MySQL()

api = Api(app)

mysql.init_app(app)

class CommentList(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select * from comment""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


#API resource routes
#api.add_resource(CommentList, '/comments', endpoint='comments')
api.add_resource('pokeapi.co/api/v2/pokemon/ditto')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8003, debug=False)