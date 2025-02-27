# EventAPI

Authentication used JWT (JSON Web Token).

EventAPI is a RESTful API for managing events. Users can create events, join them, and leave them.

## Running Locally

### Requirements:

- Python 3.8+
- Django
- Django REST Framework
- Docker (if running in a container)

### Setting up the local environment:

1. Clone the repository:
   ```sh
   git clone https://github.com/Sparix/TestTask_Join.to.IT.git
   cd TaskEventAPI
   ```
2. Create a virtual environment and install dependencies:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```sh
   python manage.py migrate
   ```
4. Start the server:
   ```sh
   python manage.py runserver
   ```

## Running with Docker

1. Build the container:
   ```sh
   docker build -t eventapi .
   ```
2. Run the container:
   ```sh
   docker run -p 8000:8000 eventapi
   ```

## Authentication

1. Register a user:
   ```sh
   POST /api/users/
   ```
2. Obtain an authorization token (if using JWT):
   ```sh
   POST /api/token/
   ```

### Pre-existing Users

The system includes preloaded users with matching usernames and passwords:

- **admin** / **admin**
- **user1** / **user1**
- **user2** / **user2**
- **user3** / **user3**

## Using the API

### Get a list of events

```sh
GET /api/events/
```

Optional parameters:

- `search` - search by title or description
- `location` - filter by location
- `date` - filter by date

### Create an event (authenticated users only)

```sh
POST /api/event/event/
```

### Join an event

```sh
GET /api/event/event/{id}/event_join/
```

### Leave an event

```sh
GET /api/event/event/{id}/event_leave/
```

### Update or delete an event (organizers only)

```sh
PUT /api/event/event/{id}/  # Update
DELETE /api/event/event/{id}/  # Delete
```

