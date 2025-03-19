# First REST API with Flask

This project demonstrates the creation of a basic REST API using Flask, a lightweight web framework for Python. The API provides endpoints to perform CRUD (Create, Read, Update, Delete) operations.

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.x
- Flask (`pip install flask`)

## Project Structure

```
/First-restAPI
├── app.py          # Main application file
├── requirements.txt # Dependencies for the project
└── Readme.md       # Documentation for the project
```

## How to Run

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
4. Run the application:
  ```bash
  python app.py
  ```
5. Access the API at `http://127.0.0.1:5000`.

## API Endpoints

### 1. GET `/items`
- **Description**: Retrieve a list of all items.
- **Response**:
  ```json
  [
   {
    "id": 1,
    "name": "Item 1",
    "price": 10.99
   },
   {
    "id": 2,
    "name": "Item 2",
    "price": 15.49
   }
  ]
  ```

### 2. GET `/items/<id>`
- **Description**: Retrieve a specific item by its ID.
- **Response**:
  ```json
  {
   "id": 1,
   "name": "Item 1",
   "price": 10.99
  }
  ```

### 3. POST `/items`
- **Description**: Add a new item.
- **Request Body**:
  ```json
  {
   "name": "New Item",
   "price": 20.00
  }
  ```
- **Response**:
  ```json
  {
   "id": 3,
   "name": "New Item",
   "price": 20.00
  }
  ```

### 4. PUT `/items/<id>`
- **Description**: Update an existing item by its ID.
- **Request Body**:
  ```json
  {
   "name": "Updated Item",
   "price": 25.00
  }
  ```
- **Response**:
  ```json
  {
   "id": 1,
   "name": "Updated Item",
   "price": 25.00
  }
  ```

### 5. DELETE `/items/<id>`
- **Description**: Delete an item by its ID.
- **Response**:
  ```json
  {
   "message": "Item deleted successfully."
  }
  ```

## Notes

- Ensure the Flask server is running before making API requests.
- Use tools like Postman or cURL to test the endpoints.
