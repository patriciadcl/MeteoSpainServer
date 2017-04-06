import bottle
from bottle import run
import predicciones

if __name__ == '__main__':
    run(host='localhost', port=8080)

app = application = bottle.default_app()
