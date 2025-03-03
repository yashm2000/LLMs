from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from api_handler import get_all_model_responses
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def generate_responses(user_input):
    """
    Generator function that yields responses as they arrive.
    """
    response_generators = get_all_model_responses(user_input)  # ✅ Call function properly

    while response_generators:
        for model in list(response_generators.keys()):
            try:
                chunk = next(response_generators[model])  # ✅ Get next chunk
                yield f'data: {json.dumps({"model": model, "response": chunk})}\n\n'
            except StopIteration:
                del response_generators[model]  # ✅ Remove completed generators

@app.route('/send_message', methods=['POST'])
def send_message():
    """
    Handles user input and starts streaming responses.
    """
    data = request.json
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Missing input"}), 400

    return Response(stream_with_context(generate_responses(user_input)), content_type="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
