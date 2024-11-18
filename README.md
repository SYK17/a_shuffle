#  Shuffling Microservice
This microservice will shuffle a set number of items from 1 to n. It has various shuffling functions including basic, unique, and weighted. 

## Requirements
The next section will provide a detailed guide on how to install the following:
- Python3 (recommended to install with a package manager).
- Pip (should come with Python3 when its installed through a package manager).
- A copy of this microservice downloaded somewhere on your computer.
- The rest of the dependencies located in requirements.txt.
    - This will be installed automatically with `pip install -r requirements.txt` (Linux/macOS).
        - Using Pythons built in `venv` recommended before running this command (more details in the next section).


## Getting Started
Note: all instructions are for Linux/macOS

Once Python3 and Pip have been installed through your favorite package manager:
1. Navigate to folder location and `cd` into it.
2. Run `python -m venv venv`
    - This will use Python's builtin `venv` module to create a virtual environment.
    - This allows you to install dependencies in a virtual environment and not globally in your computer.
    - To remove, simply `rm -rf` the venv file.

3. Enter the newly created virtual environment with `source venv/bin/activate`
    - You should see `(venv)` on the far left side of your terminal line.
    - To exit the environment, enter `deactivate`

4. Run `pip install -r requirements.txt`
    - This tells pip to recursively install the rest of the requirements found in requirements.txt.

5. Run `python shuffle_service.py` to start the microservice.

6. Done! As long as the microservice is running, you can make calls to it.

7. End the microservice with `ctrl-c`


## Functionality

This microservice depends on a HTTP request by the main program via a JSON payload.
When running, it listens at `http://localhost:8000/shuffle` for a `POST` request.

### Basic Shuffle
The microservice expects the JSON body to have:
1. `"random_nums"` string as the key.
2. An integer which represents the number of items you are shuffling.

The microservice will then return:
1. `"shuffled_sequence"` string as the key
2. A list of shuffled numbers as the value

#### Example for Basic Shuffle
Main program sends:
```JSON
{
    "random_nums": 10
}
```
Microservice responds with:
```JSON
{
    "shuffled_sequence": [10, 2, 4, 7, 6, 9, 8, 5, 1, 3]
}
```

### Unique shuffle
Main program sends:
```JSON
{
    "unique_nums": 5
}
```
Microservice responds with:
```JSON
{
    "shuffled_sequence": [4, 1, 3, 2, 5]
}
```

### Weighted Shuffle
Main program sends:
```JSON
{
    "weighted_nums": 3,
    "weights": [5, 1, 1]
}
```
Microservice responds with:
```JSON
{
    "shuffled_sequence": [1, 1, 1] // Likley sequence since '1' is given a weight of '5' out of possible '7'
}
```

## How to Request and Receive
You can make requests to this microservice using any HTTP client library in your programming language of choice.

Pseudocode example:

```Pseudocode
FUNCTION get_shuffled_sequence(n):
    SET url = "http://localhost:8000/shuffle"
    SET requestBody = {"random_nums": n}

    SEND HTTP POST to url:
        headers: {"Content-Type": "application/json"}
        body: requestBody thats been converted to JSON string

    IF response 200 (OK) then
        SET responseData = parse JSON response
        RETURN responseData.shuffled_sequence
    ELSE
        Error handling
    END IF
END FUNCTION

// Example call

    SET shuffled_sequence = get_shuffled_sequence(10)

// Returns {"shuffled_sequence": [10, 2, 4, 7, 6, 9, 8, 5, 1, 3]}
```

## UML Sequence Design
![UML_sequence_diagram](https://github.com/user-attachments/assets/303996b0-3d0c-4724-9cde-239727150958)
