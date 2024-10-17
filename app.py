# Import necessary modules from Flask
from flask import Flask, jsonify, request, abort

# Initialize the Flask app
app = Flask(__name__)

# In-memory "database" of messages
messages = [
    {"id": 1, "user": "Alice", "content": "Hello, how are you?"},
    {"id": 2, "user": "Bob", "content": "I'm good, thanks! And you?"},
    {"id": 3, "user": "Alice", "content": "Doing well, just working on a project."}
]

# Define route to handle requests to the root URL ('/')
@app.route('/')
def index():
    return "Welcome to the Chat Application API! Try accessing /messages to see all messages."

# Health check route (GET)
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200  # Return HTTP status 200 OK

# Route to retrieve all messages (GET request)
@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages), 200  # Return the list of messages with a 200 status code

# Route to retrieve a single message by its ID (GET request)
@app.route('/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = next((msg for msg in messages if msg['id'] == message_id), None)
    if message is None:
        abort(404)  # If the message is not found, return a 404 error
    return jsonify(message), 200  # Return the message with a 200 status code

# Route to create a new message (POST request)
@app.route('/messages', methods=['POST'])
def create_message():
    if not request.json or not 'user' in request.json or not 'content' in request.json:
        abort(400)  # Return a 400 error if the request body is invalid
    
    new_message = {
        'id': messages[-1]['id'] + 1 if messages else 1,  # Assign a new ID
        'user': request.json['user'],  # The user is provided in the request body
        'content': request.json['content']  # The content is provided in the request body
    }
    messages.append(new_message)  # Add the new message to the list
    return jsonify(new_message), 201  # Return the new message with a 201 status code

# Route to update an existing message (PUT request)
@app.route('/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    message = next((msg for msg in messages if msg['id'] == message_id), None)
    if message is None:
        abort(404)  # If the message is not found, return a 404 error
    
    if not request.json:
        abort(400)  # Return a 400 error if the request body is invalid
    
    # Update the message's content based on the request body
    message['user'] = request.json.get('user', message['user'])  # User can be updated
    message['content'] = request.json.get('content', message['content'])  # Content is updated
    return jsonify(message), 200  # Return the updated message with a 200 status code

# Route to delete a message (DELETE request)
@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    global messages
    messages = [msg for msg in messages if msg['id'] != message_id]  # Rebuild the messages list
    return '', 204  # Return a 204 status code indicating successful deletion

# Entry point for running the Flask app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
