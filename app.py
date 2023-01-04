from flask_cors import CORS
from flask import Flask, jsonify, request
from ClsAlgoritmo import ClsAlgoritmo
import jwt
from dotenv import dotenv_values

ClsAlgoritmo = ClsAlgoritmo()
app = Flask(__name__)
CORS(app)
config = dict(dotenv_values(".env"))
dataset= ""
ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/v1/archivo', methods=["POST"])
def algoritmo():
    if(request.headers.get("Authorization")==None):
        return jsonify({"error":"JWT missing"})
    token = request.headers.get("Authorization").replace("Bearer ","")
    secret = config.get("JWT_SECRET")
    print(secret)
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    user_id = payload.get("id")
    dfs = ClsAlgoritmo.getDatos(user_id)
    ClsAlgoritmo.df_datos = []
    print("Respondiendo...")
    return jsonify({"success":"Procesado correctamente","datos": dfs})


if __name__ == '__main__':
    app.run(port = 4004, debug = True)