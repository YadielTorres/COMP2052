from flask import Flask, request, jsonify
import datetime # Para añadir una fecha de registro

app = Flask(__name__)


usuarios_db = []
next_user_id = 1 # Para asignar IDs simples a los usuarios

# Ruta GET /info
@app.route('/info', methods=['GET'])
def get_info():

    system_info = {
        "system_name": "API de Usuario",

    }
    return jsonify(system_info)

# Ruta POST /crear_usuario
# Recibe nombre y correo, valida y almacena el usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():

    #Espera un JSON con 'nombre' y 'correo'.
    global next_user_id 
    
    data = request.json

    # Validar que los datos necesarios esten presente
    if not data or 'nombre' not in data or 'correo' not in data:
        return jsonify({
            "error": "Datos incompletos."
            })

    nombre = data.get('nombre')
    correo = data.get('correo')

    # Validación simple adicional (que no esten vacios)
    if not nombre or not isinstance(nombre, str) or len(nombre.strip()) == 0:
         return jsonify({"error": "Nombre' no puede estar vacio."})
     
    if not correo or not isinstance(correo, str) or len(correo.strip()) == 0:
         return jsonify({"error": "Correo no puede estar vacio."})

    # Crear el nuevo usuario
    nuevo_usuario = {
        "id": next_user_id,
        "nombre": nombre.strip(),
        "correo": correo.strip(),
    }
    
    usuarios_db.append(nuevo_usuario)
    next_user_id += 1 # Incrementar el ID para el próximo usuario

    # Devolver una respuesta de exito
    return jsonify({
        "message": "Usuario creado.",
        "usuario": nuevo_usuario # Devolvemos el usuario creado
        })

# Ruta GET /usuarios
# Devuelve la lista de todos los usuarios almacenados
@app.route('/usuarios', methods=['GET'])
def get_usuarios():

    return jsonify({
        "usuarios": usuarios_db,
        "total_usuarios": len(usuarios_db)
        })

if __name__ == '__main__':
    app.run(debug=True)