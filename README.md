# micros

Welcome to my message broker microservices which enables communication between different components of the app.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Running the APPs](#running-the-apps)
- [Contributing](#contributing)
- [License](#license)

## Features
- A fully functioning message queueing app.
- Lightweight and efficient powered by Django and FastAPI.
- Easy deployment using Docker.

## Tech Stack
- **Programming Language**: Python
- **Framework**: Django Rest Framework and FastAPI
- **Containerization**: Docker

## Quick Start

Follow these steps to get started:

### 1. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/Gideon-Nobbs7/micros.git
```

### 2. Set Up a Virtual Environment
Navigate to the admin directory and fastpi directory which contains the Django(message producer) and FastAPI(message consumer) create a virtual environment respectively:
#### Admin
```bash
cd admin
python -m venv [environment_name]
```
Activate the virtual environment:
- On Windows:
  ```bash
  [environment_name]\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source [environment_name]/bin/activate
  ```
Install the required Python packages:
```bash
pip install -r requirements.txt
```

#### Fastpi
```bash
cd fastpi
python -m venv [environment_name]
```
Activate the virtual environment:
- On Windows:
  ```bash
  [environment_name]\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source [environment_name]/bin/activate
  ```
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Create .env file
Go to your root directory and create a .env file

### 4. Set Up Your RabbitMQ
Head over to CloudAMQP for your AMQP_URL and create an environmental variable for your AMQP_URL
```bash
https://www.cloudamqp.com/
```

## Running the APPs
Build and run the Docker images to start the application:
#### Admin
In your admin directory:
```bash
docker-compose up --build
```

#### Fastpi
In your fastpi directory:
```bash
docker-compose up --build
```

### Run the APP Locally
If Docker is not an option, navigate to the admin and fastpi directory respectively and run each of them manually:
#### Admin
```bash
python manage.py runserver
```
#### Fastpi
```bash
python main.py
```

### Accessing the Apps
To access both apps/services:
1. Open your terminal to both the admin and fastpi apps and make sure both apps are running.
2. Open Postman and make a POST request to the admin app

#### API Schema
Below is the schema for the API endpoints, detailing the parameters and their expected data.

#### Endpoint: `api/fares`
**Method:** POST  
**Description:** Create a new fare.

**Request Body** (JSON):
```json
{
  "location": "string",
  "price": "integer",
  "difficulty": "string"
}
```

Check your terminal opened for fastpi to see the message being consumed from the broker and added to its database.

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Open a pull request with a detailed description of your changes.

---

Feel free to reach out if you have any questions or need further assistance!