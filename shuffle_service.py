# Flask is the main framework for creating web services.
# Request helps us read what the user sends as a request to this microservice.
# jsonify helps us package response in JSON format.

from flask import Flask, request, jsonify
import os
import json
import random

# Initialize new web service.
app = Flask(__name__)

##################
# Helper Functions
##################

def basic_shuffle(playlist_size):
        """
        Generates a randomly shuffled sequence of numbers from 1 to playlist_size.
        """
        ordered_sequence = list(range(1, playlist_size + 1))
        random.shuffle(ordered_sequence)
        return ordered_sequence

def create_log():
        """
        Creates log.json in same directory as shuffle_service.py to hold previous shuffled arrays.
        """
        service_directory = os.path.dirname(os.path.abspath(__file__))
        log_file_path = os.path.join(service_directory, 'log.json')

        if os.path.exists(log_file_path) is False:
                with open(log_file_path, 'w') as log_file:
                    json.dump({"shuffle_history": []}, log_file)

        return log_file_path

def save_sequence_to_log(shuffled_sequence):
        """
        Saves a shuffled sequence to the log file with timestamp.
        """
        log_file_path = create_log()

        with open(log_file_path, 'r') as log_file:
                log_data = json.load(log_file)

        sequence_entry = {
                "shuffled_sequence": shuffled_sequence
        }
        log_data["shuffle_history"].append(sequence_entry)

        with open(log_file_path, 'w') as log_file:
                json.dump(log_data, log_file)

def validate_request_data(request_data):
        """
        Validates the request data for proper format and constraints.

        Arguments:  request_data (dict): The JSON request data
        Returns:    (boolean, error_message, error_code)
        """
        if not request_data or "random_nums" not in request_data:
                return False, {'error': 'Please provide random_nums in the request body'}, 400

        playlist_size = request_data["random_nums"]
        if not isinstance(playlist_size, int) or playlist_size <= 0:
                return False, {'error': 'random_nums must be a positive integer'}, 400

        return True, None, None

##################
# Service Handlers
##################

def basic_shuffle_handler(playlist_size):
        """
        Handles basic shuffle requests: generates and logs a shuffled sequence.
        """
        shuffled_sequence = basic_shuffle(playlist_size)
        save_sequence_to_log(shuffled_sequence)
        return {"shuffled_sequence": shuffled_sequence}

def unique_shuffle_handler():
        """
        TODO: Will handle unique shuffle requests.
        """
        pass

def weighted_shuffle_handler():
        """
        TODO: Will handle weighted shuffle requests.
        """
        pass

####################
# Main Route Handler
####################

@app.route("/shuffle", methods=["POST"])
def handle_shuffle_request():
        """
        Main endpoint for handling shuffle requests.
        """
        # Parse JSON request
        request_data = request.get_json()

        # Validate request data
        is_valid, error_message, error_code = validate_request_data(request_data)
        if not is_valid:
                return jsonify(error_message), error_code

        # Get shuffle type from request
        shuffle_type = request_data.get("service_type", "basic")

        # Route to appropriate handler
        if shuffle_type == "basic":
                response = basic_shuffle_handler(request_data["random_nums"])

        # TODO: implement unique and weighted shuffle handlers
        # elif shuffle_type == "unique":
        #         response = unique_shuffle_handler(request_data["random_nums"])
        # elif shuffle_type == "weighted":
        #         response = weighted_shuffle_handler(request_data["random_nums"], request_data.get("weights", []))
        else:
                return jsonify({"error": "Invalid shuffle type"}), 400

        return jsonify(response)

if __name__ == "__main__":
        app.run(debug=True, port=8000)
