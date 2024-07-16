from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from services.analytics_service import get_task_statistics
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route('/stats', methods=['GET'])
def stats():
    stats = get_task_statistics(db)
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
