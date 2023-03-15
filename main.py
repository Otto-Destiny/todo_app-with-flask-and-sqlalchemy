from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1937@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)
    
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(), nullable=False) 
    todos = db.relationship('Todo', backref='list', lazy=True)

with app.app_context():
    db.create_all()
    
@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    with app.app_context():
        try:
            Todo.query.filter_by(id=todo_id).delete()
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify({ 'success': True })

@app.route('/todos/create', methods=['POST'])
def create_todo():
    with app.app_context():
        error = False
        body = {}
        try:
            description = request.get_json()['description']
            todo = Todo(description=description)
            db.session.add(todo)
            db.session.commit()
            todo_data = {
                'id': todo.id,
                'description': todo.description
            }
        except:
            error == True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        if error:
            abort(400)
        else:
            return jsonify(todo_data)
    
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    with app.app_context():
        try:
            completed = request.get_json()['completed']
            todo = Todo(todo_id)
            todo.completed = completed
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return redirect(url_for('index'))

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    with app.app_context():
        todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()
        lists = TodoList.query.all()
        active_list = TodoList.query.get(list_id)
        return render_template('index.html', 
                               lists=lists,
                               todos=todos)
    
    
@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))   
    
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)