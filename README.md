# Flask-rest-social-network

## Intro

Simple Flask REST API that provides following features:
- user sign up
- user login
- post creation
- post like
- post unlike
- analytics about how many likes was made. API returns analytics aggregated by day.
- last login time and when user made a last request to the service.

Database used in this project is ```Postgres```.

<br>

## Project structure

```
.
├── app.py
├── config.py
├── models
│   └── models.py
├── requirements.txt
├── service
│   └── db.py
├── docker-compose.yml
├── Dockerfile
└── views.py
```

<br>

## Running application

Application is dockerized, so to run just type:
```shell
docker-compose up --build
```

<br>

To change configuration variables, edit ```config.py``` file in root:
```python
SECRET_KEY = 'e8=$#io8@o5cuo=$d7q4=n!viw8b!sj3g=ljo08s0_7ytn073l' # Secret key
TOKEN_EXPIRATION_TIME = 20 # Time after which token will expire

POSTGRES_USER = 'admin'
POSTGRES_PASSWORD = '1111'
POSTGRES_HOST = 'postgres'
POSTGRES_DB = 'flask_sn_db'
POSTGRES_PORT = '5432'

DATABASE_CONNECTION_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
```
<br>

## Sending requests

### Actual features

To sign up (create new user), send ```POST``` request with the following ```json``` data to ```/signup```:
```json
{
    "username": "Dan",
    "password": "mypass123"
}
```

<br>

Response should be like this:
```json
{
    "username": "Dan"
}
```

<br>

After successfully logging in, token should be present in a response:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.yJpZCI6ImZmY2FkZDdlLTkwMDctNGE5MC1iMjc5LTY4MDk0MGZlNzVhNSIsImV4cCI6MTYyNTg1MzQyMX0.XWZBFNPVsfALz0JGg22keNJAWwABMJBjRFkeiaciw7s"
}
```

<br>

Token should be passed with request in Headers with ```x-access-token``` key.
Token will work for 20 minutes by default (can be changed in ```config.py```).
With this token, you can perform actions, such as:

- creating new posts
- liking/unliking posts
- getting list of your own posts

<br>

To create new post, send ```POST``` request with the following data in ```json``` format to ```/post```:
```json
{
    "text": "Bananas are cool!"
}
```

<br>

> Note: responses are not listed here, they are pretty self-explanatory.

<br>

To like a post, send ```POST``` request to ```/<post_id>/like```, where ```<post_id>``` is the id of a post.
Sending this request to the post user already liked by this user will unlike it.

<br>

To get a list of user's posts, send ```GET``` request to ```/post```.

<br>

To get analytics on how many likes were made aggregated by day, send ```GET``` request to ```/analytics?date_from=2021-07-10&date_to=2021-07-11```, where ```date_from``` and ```date_to``` mean period, for which analytics should be made.

Response should be like this:
```json
{
    "analytics": [
        {
            "date": "Thu, 21 Oct 2021 00:00:00 GMT",
            "like_count": 1
        }
    ]
}
```

<br>

### Features for the testing purposes

To perform actions listed here, no token is required. They are just for the testing purposes.

<br>

To get list of all users, send ```GET``` request to ```/users```.

<br>

To get list of all posts, send ```GET``` request to ```/posts```.

<br>
<br>
