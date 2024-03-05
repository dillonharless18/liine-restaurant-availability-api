# Liine API Service

## Project Description
The Liine API Service is a Python-based project designed to provide information about restaurant availability. Given a datetime string as input, the API endpoint returns a list of restaurants open at the specified date and time. The system is built with a focus on correctness, with optimization being a secondary goal.

## Setup and Installation

To set up and run the Liine API Service, follow these steps:

1. **Clone the Repository**
    ```
    git clone https://github.com/your-repository/liine-api-service.git
    cd liine-api-service
    ```

2. **Create and Activate Virtual Environment** (optional but recommended)
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**
    Create a `.env` file in the project root directory and add any necessary environment variables.

5. **Run the Application**
    ```
    python app.py
    ```

## Usage Examples

To use the API, send a GET request to the endpoint with the datetime parameter:

    ```
    GET /restaurants?datetime=2023-03-15T18:00:00
    ```


This will return a JSON response with a list of open restaurants at the given datetime.

## How to Run Tests

To run the test suite, execute the following command:

python -m unittest discover -s tests


This will discover and run all tests in the `tests` directory. 

## Docker Support

To run the Liine API Service in a Docker container, use the included `Dockerfile`:

1. **Build the Docker Image**
    ```
    docker build -t liine-restaurant-availability-api-dillon-harless .
    ```

2. **Run the Container**
    ```
    docker run -p 5000:5000 liine-restaurant-availability-api-dillon-harless
    ```

This will start the API service inside a Docker container, accessible on port 5000.
