from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(".env"))

print("DEBUG DATABASE_URL =", os.getenv("DATABASE_URL"))

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/tasks", methods=["GET"])
def get_tasks():

    tasks = Task.query.all()

    result = []

    for task in tasks:
        result.append({
            "id": task.id,
            "title": task.title,
            "done": task.done
        })

    return jsonify(result)


@app.route("/tasks", methods=["POST"])
def add_task():

    data = request.json

    task = Task(
        title=data["title"],
        done=False
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "done": task.done
    }), 201


@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):

    task = Task.query.get(id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.done = not task.done

    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "done": task.done
    })


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    task = Task.query.get(id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)