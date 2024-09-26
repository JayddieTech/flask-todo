from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///app.db"

db=SQLAlchemy(app)

class Todo(db.Model):
    Id=db.Column(db.Integer,primary_key=True)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    content=db.Column(db.String,nullable=False)
    completed=db.Column(db.Integer,default=0)

    def  __repr__(self) -> str:
        return f'Task {self.Id}'

@app.route('/',methods=["POST","GET"])
def index():
    if request.method=="POST":
       task_content=request.form['content']
       todo=Todo(content=task_content)

       db.session.add(todo)
       db.session.commit()

       return redirect("/")
    else:
        todos=Todo.query.order_by("created_at").all()
        return render_template("index.html",todos=todos)
    
@app.route('/delete/<Id>')
def delete(Id):
    todo=Todo.query.get_or_404(Id)
    
    try:
        db.session.delete(todo)
        db.session.commit()

        return redirect('/')  
    except:
        return "Thre was an error deleting the item"  

@app.route('/update/<Id>',methods=["GET","POST"])
def update(Id):
    todo=Todo.query.get_or_404(Id)
    if request.method=="POST":
        new_todo_content=request.form['content']
        todo.content=new_todo_content

        db.session.commit()

        return redirect("/")
    else:
        return render_template("update.html",todo=todo)




 #Function to initialize the database if it doesn't exist
def initialize_database():
    # Check if the database file exists
    if not os.path.exists('app.db'):
        # If it doesn't, create the database tables
        with app.app_context():
            db.create_all()
            print("Database initialized")

# Main entry point
if __name__ == "__main__":
    # initialize_database()  # Initialize the database if not present
    app.run(debug=True)