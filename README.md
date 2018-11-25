# students_rating
# init
```
pip3 install -r requirements.txt
mkdir instance
FLASK_APP=flask_app FLASK_ENV=development FLASK_DEBUG=1 python3 -m flask init-db
```

# run
```
FLASK_APP=flask_app FLASK_ENV=development FLASK_DEBUG=1 python3 -m flask run --host=0.0.0.0 --port=8080
```
