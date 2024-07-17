from gevent.pywsgi import WSGIServer
from decouple import config

from .routes import app


ENVIRONMENT = config("ENVIRONMENT", "development")
PORT = config("PORT", 8080)
DEBUG = config("DEBUG", True)


if ENVIRONMENT == "production":
    http_server = WSGIServer((PORT, 8080), app)
    http_server.serve_forever()
else:
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
