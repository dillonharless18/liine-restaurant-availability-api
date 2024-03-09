# Liine Restaurant API Service

## Project Description
The Liine Restaurant API Service is a Python-based project designed to provide information about restaurant availability. It uses only the Python standard library and has no external dependencies. Given a datetime string as input, the API endpoint returns a list of restaurants open at the specified date and time. The system is built with a focus on correctness, with optimization being a secondary goal. 

The data exists in the repository under `data/` folder in the given `csv` format. The project parses the human-readable data and stores it in 1 of 2 ways, depending on which server you choose to run. There are two server options.

`server.py` uses an in-memory data structure to store the parsed data. 

`server_with_db.py` stores the data in a SQLite database.

The two servers use somewhat different logic to parse the data. `server.py` explores parsing the data in a more direct logic-driven manner based on the patterns I recognized in the data, while `server_with_db.py` leverages regular expressions to extract the data based on the patterns. The code in `server.py` is admittedly more complex, therefore I paid extra attention to docstrings, tests, and modularity in there. In the interest of time, once I got `server_with_db.py` working I didn't focus as much on modularity in that one.

## Setup and Installation

To set up and run the Liine API Service, follow these steps:

1. **Clone the Repository**
    ```
    git clone https://github.com/dillonharless18/liine-restaurant-availability-api.git
    cd liine-restaurant-availability-api
    ```

2. **Create and Activate Virtual Environment** (optional but recommended)
    ```
    python -m venv venv # I usually make these in my home directory under a folder called `.venvs`
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. **Run the Application**
    ```
    python src/server.py
    ```

    or

    ```
    python src/server_with_db.py
    ```

## Usage Examples

To use the API, send a GET request to the endpoint with the datetime parameter:

    ```
    GET http://127.0.0.1:3000/restaurants?datetime=2024-03-09T14:00:00
    ```


This will return a JSON response with a list of open restaurants at the given datetime or it will return an appropriate error.

## How to Run Tests

To run the test suite, execute the following command:

python -m unittest


## Docker Support

To run the Liine API Service in a Docker container, use the included `Dockerfile`:

1. **Build the Docker Image**
    ```
    docker build -t liine-restaurants .
    ```

2. **Run the Container**
    ```
    docker run -p 3000:3000 liine-restaurants
    ```

    Or if you would like to use the database version instead of the in-memory datastore run the following command:

    ```
    docker run -p 3000:3000 -e USE_DB=1 liine-restaurants
    ```

This will start the API service inside a Docker container, accessible on port 3000.