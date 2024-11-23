# Flask imports and setup...
from flask import Flask, request, jsonify
import os
import json
import random

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

        with open(log_file_path, 'w') as log_file:
                json.dump({"last_sequence": []}, log_file)

        return log_file_path

def save_sequence_to_log(shuffled_sequence):
        """
        Overwrites log file with recent sequence.
        """
        log_file_path = create_log()

        with open(log_file_path, 'w') as log_file:
                json.dump({"last_sequence": shuffled_sequence}, log_file)

def validate_request_data(request_data):
        """
        Validates that exactly one valid shuffle type key is present with a positive integer.
        """
        valid_keys = ["random_nums", "unique_nums", "weighted_nums"]
        
        # Check if request is empty
        if not request_data:
                return False, {'error': 'Request body is empty'}, 400
        
        # Check if exactly one valid key is present
        present_keys = [key for key in valid_keys if key in request_data]
        if len(present_keys) == 0:
                return False, {'error': 'Please provide one of: random_nums, weighted_nums, or unique_nums'}, 400
        if len(present_keys) > 1:
                return False, {'error': 'Please provide only one of: random_nums, weighted_nums, or unique_nums'}, 400
        
        # Get the value for the present key
        key = present_keys[0]
        value = request_data[key]
        
        # Validate the value
        if not isinstance(value, int) or value <= 0:
                return False, {'error': f'{key} must be a positive integer'}, 400

        # Special validation for weighted shuffle
        if key == "weighted_nums" and "weights" not in request_data:
                return False, {'error': 'weights array must be provided with weighted_nums'}, 400

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

def read_log():
        """
        Returns the logged sequence. Helper function for Service Handlers
        """
        log_file = create_log()
        with open(log_file, 'r') as log_file:
                log_data = json.load(log_file)
                return log_data.get("last_sequence", [])

def unique_shuffle_handler(playlist_size):
        """
        Handles unique shuffle requests: Ensures the new sequence is different from the previous sequence generated.
        """
        # Get last sequence
        last_sequence = read_log()

        # if missing or size is different, do basic shuffle
        if not last_sequence or len(last_sequence) != playlist_size:
                return basic_shuffle_handler(playlist_size)
        
        # Otherwise, check for difference
        while True:
                new_shuffled_sequence = basic_shuffle_handler(playlist_size)
                if new_shuffled_sequence["shuffled_sequence"] != last_sequence:
                        return new_shuffled_sequence

def weighted_shuffle_handler(playlist_size, weights):
        """
        Handles weighted shuffle requests:
        Calculations done by random.choices from Python's random library.
        probability of a number is the weight assigned to that index / sum of all possible weights.
        Ex.
        {
            "weighted_nums": 3
            "weights: [5, 1, 1]"
        }
        number 1 has 5/7 or 71% chance to occur again.
        number 2 has 1/7 or 14% chance to occur again.
        number 3 has 1/7 or 14% chance to occur again.
        """
        if len(weights) != playlist_size:
                return jsonify({"error": "weights array length must match playlist size"}), 400

        # Generate sequence 1 to playlist_size
        sequence = list(range(1, playlist_size + 1))

        # Use random.choices: probability = weight / sum(all_weights)
        shuffled_sequence = random.choices(sequence, weights=weights, k=playlist_size)

        save_sequence_to_log(shuffled_sequence)
        return {"shuffled_sequence": shuffled_sequence}


####################
# Main Route Handler
####################

@app.route("/shuffle", methods=["POST"])
def handle_shuffle_request():
        """
        Main endpoint for handling shuffle requests.
        Routes based on which key is used in the request.
        """
        # Parse JSON request
        request_data = request.get_json()

        # Validate request data
        is_valid, error_message, error_code = validate_request_data(request_data)
        if not is_valid:
                return jsonify(error_message), error_code

        # Route based on which key is present
        if "random_nums" in request_data:
                response = basic_shuffle_handler(request_data["random_nums"])
        elif "unique_nums" in request_data:
                response = unique_shuffle_handler(request_data["unique_nums"])
        elif "weighted_nums" in request_data:
                response = weighted_shuffle_handler(
                    request_data["weighted_nums"],
                    request_data.get("weights", [])
                )
        return jsonify(response)

if __name__ == "__main__":
        app.run(debug=True, port=8000)
