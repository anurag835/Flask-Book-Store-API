from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id":1, "title":"Book 1", "author":"Author 1"},
    {"id":2, "title":"Book 2", "author":"Author 2"},
    {"id":3, "title":"Book 3", "author":"Author 3"},
    {"id":4, "title":"Book 4", "author":"Author 4"},
    {"id":5, "title":"Book 5", "author":"Author 5"},
]

@app.route('/', methods=['GET'])
def home_page():
    return 'Home Page'

# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# Route to get a specific book by id
@app.route('/books/<int:book_id>/', methods=['GET'])
def get_book(book_id):
    try:
        for book in books:
            if book['id'] == book_id:
                return jsonify(book)
        return jsonify({'error':'Book not found for this ID'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for add new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    if "id" in data and "title" in data and "author" in data and isinstance(data["id"], int):
        if any(b['id'] == data['id'] for b in books):
            return jsonify({'error':'Book with the same ID already exists'}), 400
        new_book = {
            "id": data['id'],
            "title": data['title'],
            "author": data['author'],
        }
        books.append(new_book)
        return jsonify({'message':'Book added successfully'}), 201 # HTTP 201 Created
    else:
        return jsonify({'error':'Invalid or Missing data in the request'}), 400 # HTTP 400 Bad request
    
# Route to update an existing book
@app.route('/books/<int:book_id>/', methods=['PUT'])
def update_books(book_id):
    try:
        data = request.json
        for book in books:
            if book['id'] == book_id:
                book['title'] = data['title']
                book['author'] = data['author']
                return jsonify({'message':'Book updated successfully'}), 200 # HTTP 200 OK
        return jsonify({'error':'Book not found for this ID'}), 404 # HTTP 404 Not Found
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Route to update an existing book
@app.route('/books/<int:book_id>/', methods=['DELETE'])
def delete_books(book_id):
    try:
        for book in books:
            if book['id'] == book_id:
                books.remove(book)
                return jsonify({'message':'Book deleted successfully'}), 204 # HTTP 204 No Content
        return jsonify({'error':'Book not found for this ID'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)