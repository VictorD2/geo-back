from flask_cors import CORS
from flask import Flask, jsonify, send_file, request
from ClsAlgoritmo import ClsAlgoritmo

ClsAlgoritmo = ClsAlgoritmo()
app = Flask(__name__)
CORS(app)

dataset= ""
ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/v1/archivo', methods=["POST"])
def algoritmo():
    print(request.files)
    if 'file' not in request.files:
        return jsonify({"error":"No está el campo File"})
    archivos = request.files.getlist("file") 
    for file in archivos:
        if allowed_file(file.filename):
            dfs = ClsAlgoritmo.getDatos(file)
            ClsAlgoritmo.df_datos = []
            print("Respondiendo...")
            return jsonify({"success":"Procesado correctamente","datos": dfs})
        else:
            return jsonify({"error": "Formato no aceptado"})


if __name__ == '__main__':
    app.run(port = 4004, debug = True)