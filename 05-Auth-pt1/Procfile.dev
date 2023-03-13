web: PORT=4000 npm start --prefix client
api: gunicorn -b 127.0.0.1:5000 --chdir ./server app:app