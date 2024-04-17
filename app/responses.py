from flask import jsonify

def bad_request_response(message):
    """
    Returns a standard 400 Bad Request response with a custom message.

    Args:
    message (str): The custom message to include in the response.

    Returns:
    tuple: A tuple containing a Flask response and the status code 400.
    """
    return jsonify({'error': message}), 400

def bad_request_ticker_response():
    """
    Returns a standard 400 Bad Request response with a ticker is required message.

    Returns:
    tuple: A tuple containing a Flask response and the status code 400.
    """
    return jsonify({'error': "'ticker' is required."}), 400