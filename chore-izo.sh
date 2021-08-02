cd "$(dirname "$0")"
export FLASK_APP=choreizo.py
flask run --host=0.0.0.0 &
