from datetime import datetime
from operator import add
from turtle import title
from flask import Flask , render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100) , nullable = False)
    desc = db.Column(db.String(100) , nullable = False)
    date = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} - {self.desc}"

@app.route("/" , methods = ['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title , desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)



@app.route("/about")
def about():
    return  render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)