from flask import Flask, jsonify, request #importing the Flask class
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from db_connector import db_connection, Error

app = Flask(__name__)
ma = Marshmallow(app)

class BookSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    title = fields.String(required=True)
    isbn = fields.String(required=True)
    publication_date = fields.String(required=True)
    availability = fields.Boolean()

    class Meta:
        fields = ("title", "isbn", "publication_date","availability")

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/')
def home():
    return "Welcome to the Library System"

@app.route('/books', methods=['POST'])
def add_book():
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    conn = db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            new_book = (book_data['title'], book_data['isbn'], book_data['publication_date'],book_data['availability'])

            query = "INSERT INTO books (title, isbn, publication_date, availability) VALUES (%s, %s, %s, %s)"

            cursor.execute(query, new_book)
            conn.commit()

            return jsonify({'Message': "New Book Added Successfully! Let's get it."}), 201
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"Error": "Database Connection failed"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)

#--- SAMPLE ENTRY FOR POSTMAN
# {
#     "title": "CODING 101",
#     "isbn": "987654321",
#     "publication_date": "2024-02-02",
#     "availability": true
# }