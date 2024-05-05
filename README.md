# Chores App

The Chores App is a web application built with FastAPI and MySQL that helps manage and track chores and rewards for kids.

## Features

- Create and manage kid profiles
- Assign chores to kids and track their completion
- Define rewards that kids can earn by completing chores
- API endpoints for creating, reading, updating, and deleting chores and rewards
- Integration with MySQL database for persistent storage

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Docker

## Getting Started

### Prerequisites

- Python 3.9+
- Docker
- MySQL database

### Installation

1. Clone the repository:
git clone https://github.com/your-username/chores-app.git

2. Navigate to the project directory:
cd chores-app

3. Create a `.env` file in the project root and provide the necessary environment variables:
DB_HOST=your_db_host
DB_PORT=your_db_port
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name

4. Build the Docker image:
docker build -t chores-app .

5. Run the Docker container:
docker run -p 8000:8000 chores-app

6. Access the application at `http://localhost:8000`.

### API Endpoints

- `POST /kids`: Create a new kid profile
- `GET /kids`: Retrieve a list of all kids
- `GET /kids/{kid_id}`: Retrieve a specific kid by ID
- `PUT /kids/{kid_id}`: Update a kid's profile
- `DELETE /kids/{kid_id}`: Delete a kid's profile
- `POST /chores`: Create a new chore
- `GET /chores`: Retrieve a list of all chores
- `GET /chores/{chore_id}`: Retrieve a specific chore by ID
- `PUT /chores/{chore_id}`: Update a chore
- `DELETE /chores/{chore_id}`: Delete a chore
- `POST /rewards`: Create a new reward
- `GET /rewards`: Retrieve a list of all rewards
- `GET /rewards/{reward_id}`: Retrieve a specific reward by ID
- `PUT /rewards/{reward_id}`: Update a reward
- `DELETE /rewards/{reward_id}`: Delete a reward

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, please contact [arigsela@gmail.com](mailto:arigsela@gmail.com).