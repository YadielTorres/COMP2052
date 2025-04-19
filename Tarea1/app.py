from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta GET /info
@app.route('/info', methods=['GET'])
def get_info():
    """
    Endpoint para obtener información básica de la aplicación.
    """
    app_info = {
        "nombre_app": "Servidor de Actividad",
        "descripcion": "Servidor de Flask ."
    }
    return jsonify(app_info)

# Ruta POST /mensaje
@app.route('/mensaje', methods=['POST'])
def post_mensaje():
    
    #Endpoint para recibir un mensaje y devolver una respuesta personalizada.
    
    data = request.json

    if data and 'mensaje' in data:
        mensaje_recibido = data['mensaje']
        respuesta = {
            "respuesta": f"Mensaje recibido: '{mensaje_recibido}'",
            "status": "exitoso"
        }
        return jsonify(respuesta)
    else:
        # Si 'mensaje' no se encuentra o no hay datos JSON, devolver un error
        error_respuesta = {
            "error": "Formato de inválido o falta la clave 'mensaje'.",
        }
        # Devolver la respuesta de error y el código de estado 400 (Bad Request)
        return jsonify(error_respuesta)

if __name__ == '__main__':
    app.run(debug=True)