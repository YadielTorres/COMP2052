# app.py
from flask import Flask, render_template, abort

app = Flask(__name__)

# Lista de diccionarios, cada uno representando una pelicula
peliculas_favoritas = [
    {
        'id': 1,
        'titulo': 'Moonfall',
        'director': 'Roland Emmerich',
        'year': 2022,
        'genero': 'Sci-Fi, Disaster',
        'sinopsis': 'A mysterious force knocks the moon from its orbit and sends it hurtling on a collision course toward earth.'
    },
    {
        'id': 2,
        'titulo': 'Geostorm',
        'director': 'Dean Devlin',
        'year': 2017,
        'genero': 'Ciencia Ficción, Acción, Thriller, Disaster',
        'sinopsis': "When the network of satellites designed to control the global climate starts to attack Earth, it's a race against the clock for its creator to uncover the real threat before a worldwide Geostorm wipes out everything and everyone."
    },
    {
        'id': 3,
        'titulo': 'Interstellar',
        'director': 'Christopher Nolan',
        'year': 2014,
        'genero': 'Sci-Fi, Time Travel, Adventure',
        'sinopsis': 'When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.'
    },
    {
        'id': 4,
        'titulo': 'Joker',
        'director': 'Todd Phillips',
        'year': 2019,
        'genero': 'Psychological Drama, Psychological Thriller, Crime, Tragedy',
        'sinopsis': 'Arthur Fleck, a party clown and a failed stand-up comedian, leads an impoverished life with his ailing mother. However, when society shuns him and brands him as a freak, he decides to embrace the life of chaos in Gotham City.'
     }
]

# Ruta principal: Muestra la lista de todas las peliculas
@app.route('/')
def index():
    return render_template('index.html', peliculas=peliculas_favoritas)

# Ruta para detalles: Muestra los detalles de una pelicula especifica por su ID
@app.route('/pelicula/<int:pelicula_id>')
def detalle_pelicula(pelicula_id):
    pelicula_encontrada = None
    for pelicula in peliculas_favoritas:
        if pelicula['id'] == pelicula_id:
            pelicula_encontrada = pelicula
            break

    if pelicula_encontrada is None:
        abort(404, description=f"Película con ID {pelicula_id} no encontrada") # Abortar con error 404

    # Si se encuentra, pasamos el diccionario de esa pelicula a la plantilla
    return render_template('movie_detail.html', pelicula=pelicula_encontrada)

if __name__ == '__main__':
    app.run()