from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True, cascade="all, delete-orphan")

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    new_author = Author(name=data['name'])
    db.session.add(new_author)
    db.session.commit()
    return jsonify({"message": "Author created", "author": {"id": new_author.id, "name": new_author.name}}), 201

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author_id=data['author_id'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book created", "book": {"id": new_book.id, "title": new_book.title, "author_id": new_book.author_id}}), 201

@app.route('/authors/<int:id>', methods=['GET'])
def get_author(id):
    author = Author.query.get_or_404(id)
    return jsonify({"id": author.id, "name": author.name, "books": [{"id": book.id, "title": book.title} for book in author.books]})

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({"id": book.id, "title": book.title, "author_id": book.author_id})

@app.route('/authors/<int:id>', methods=['PUT'])
def update_author(id):
    data = request.get_json()
    author = Author.query.get_or_404(id)
    author.name = data['name']
    db.session.commit()
    return jsonify({"message": "Author updated", "author": {"id": author.id, "name": author.name}})

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = Book.query.get_or_404(id)
    book.title = data['title']
    db.session.commit()
    return jsonify({"message": "Book updated", "book": {"id": book.id, "title": book.title, "author_id": book.author_id}})

@app.route('/authors/<int:id>', methods=['DELETE'])
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return jsonify({"message": "Author deleted"})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})

@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return jsonify([{"id": author.id, "name": author.name, "books": [{"id": book.id, "title": book.title} for book in author.books]} for author in authors])

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": book.id, "title": book.title, "author_id": book.author_id} for book in books])

if __name__ == '__main__':
    app.run(debug=True)