# FastAPI Template with Google OAuth 2.0 Authentication
This project is a FastAPI template with Google OAuth 2.0 integration for user authentication. It uses PostgreSQL as the database and runs using Uvicorn.

## Requirements
- Python 3.13
- PostgreSQL
- Uvicorn
- FastAPI
- SQLAlchemy

## Installation
1. Clone the repository:
```bash
git https://github.com/jamshid6573/FastApi-Template.git
cd FastApi-Template
```

## Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
venv\Scripts\activate  
```

## Set up the database connection in the .env file:
``` bash
user=your_database_user
password=your_database_password
host=database_host
port=database_port
database=database_name
SECRET_KEY=your_secret_key

```

## Install the dependencies:
``` bash
pip install -r requirements.txt
```

## Create the PostgreSQL database, if not created already, and set it up:
``` bash
CREATE DATABASE your_db_name;
```

## Run database migrations:
``` bash
alembic upgrade head
```

## Start the server using Uvicorn:
``` bash
uvicorn main:app --reload
```


- Get the Client ID and Client Secret and add them to the .env file.

## License
- This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

