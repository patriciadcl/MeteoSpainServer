import bottle
app = application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(server='gunicorn', host='127.0.0.1', port=8000)
