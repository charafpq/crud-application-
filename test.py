from flask import Flask ,render_template ,request,redirect,url_for
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

print("Hello World")


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/flask'

db = SQLAlchemy(app)
# initialize the database
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.Text, nullable=True)

#route for the home page 
@app.route('/')
def hello_start():
    tasks = Task.query.all()

    return render_template('index.html',tasks=tasks)

#route for adding a new task
@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task_name = request.form["taskName"]
        task_desc = request.form["taskDesc"]
        new_task = Task(name=task_name, desc=task_desc)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('hello_start'))
    return render_template("add.html")

#route for editing a task
@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit_task(id):
    task = db.get_or_404(Task, id)
    if request.method == "POST":
        task.name = request.form["taskName"]
        task.desc = request.form["taskDesc"]
        db.session.commit()
        return redirect(url_for('hello_start'))
    return render_template("edit.html", task=task)

#route for deleting a task
@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete_task(id):
    task = db.get_or_404(Task, id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('hello_start'))

if __name__ == "__main__":
    app.run(debug=True)