import requests

# URL.
url = "http://localhost:8000/shuffle"

# Test data to send.
data = {
        "unique_nums": 5,
}

# Send POST request to the microservice.
try:
        # "json=" is the data to send (requests converts the Python dict to JSON).
        response = requests.post(url, json=data)

        # Check if request was successful (status code 200).
        if response.status_code == 200:
                result = response.json()  # .json() converts the JSON response back to a Python dictionary
                print("Success! Response:", result)
        else:
                print(f"Error: Received status code {response.status_code}")
                print("Error message:", response.json())

except requests.exceptions.ConnectionError:
        print("Error: Server connection failed.")
        print("Is your microservice is running?")
