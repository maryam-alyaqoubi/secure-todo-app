#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app
export DATABASE_URL=${DATABASE_URL:-"mysql+pymysql://todo_user:todo_pass@127.0.0.1:3306/secure_todo_db"}
flask run --host=0.0.0.0 --port=5000
