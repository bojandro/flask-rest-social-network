# Flask-rest-social-network

<br>

## Intro

Simple Flask REST API that provides following features:
- user sign up
- user login
- post creation
- post like
- post unlike
- analytics about how many likes was made. API returns analytics aggregated by day.
- last login time and when he made a last request to the service.

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
└── views.py
```

<br>

## Installation

Create virtual environment (Ubuntu):
```shell
$ python3 -m venv env
```
<br>

Start using virtual environment:

```shell
$ source env/bin/activate
```
<br>

Install required packages:

```shell
(env) $ pip install -r requirements.txt
```
<br>

## Running application

To run application (Ubuntu):
```shell
(env) $ python3 app.py
```
<br>

To change configuration variables, edit ```config.py``` file in root:
```python
db_username = 'name' # Database username
db_password = 'pass' # Database passsword
CONNECTOR = 'mysql+pymysql' # Connector to reach database
SECRET_KEY = 'e8=$#io8@o5cuo=$d7q4=n!viw8b!sj3g=ljo08s0_7ytn073l' # Secret key
DATABASE = 'flask_sn_app_db' # Database name
LINK = 'localhost' # Link
TOKEN_EXPIRATION_TIME = 20 # Time after which token will expire
```
<br>

## Sending requests

<br>

### Actual features

To sign up (create new user), send data in ```json``` format to ```/signup``` with ```POST``` request:
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
    "message": "New user created!"
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

Token should be passed with request in ```Headers``` with ```x-access-token``` key.
Token will work for 20 minutes by default (can be changed in ```config.py```).
With this token, you can perform actions, such as:

- creating new posts
- liking/unliking posts
- getting list of your own posts

<br>

To create new post, send ```POST``` request with data in ```json``` format to ```/post```:
```json
{
    "text": "Bananas are cool!"
}
```

<br>

Note: responses are not listed here, they are pretty self-explanatory.

<br>

To like a post, send ```POST``` request to ```/<post_id>/like```, where ```<post_id>``` is the id of a post.
Sending this request to the post user already liked by this user will unlike it.

<br>

To get a list of user's posts, send ```GET``` request to ```/post```.

<br>

To get analytics on how many likes were made aggregated by day, send ```GET``` request to ```/analytics?date_from=2021-07-10&date_to=2021-07-11```, where ```date_from``` and ```date_to``` mean period, for which analytics should be made.

<br>
<br>

### Features for the testing purposes

To perform actions listed here, no token is required. They are just for the testing purposes.

<br>

To get list of all users, send ```GET``` request to ```/users```.

<br>

To get list of all posts, send ```GET``` request to ```/posts```.

<br>
<br>

## Reference

Official website
- [Flask](https://flask.palletsprojects.com)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com)
- [MySQL](https://www.mysql.com/)
