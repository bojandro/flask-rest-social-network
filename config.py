# Configuration file

SECRET_KEY = 'e8=$#io8@o5cuo=$d7q4=n!viw8b!sj3g=ljo08s0_7ytn073l' # Secret key
TOKEN_EXPIRATION_TIME = 20 # Time after which token will expire

POSTGRES_USER = 'admin'
POSTGRES_PASSWORD = '1111'
POSTGRES_HOST = 'postgres'
POSTGRES_DB = 'flask_sn_db'
POSTGRES_PORT = '5432'

DATABASE_CONNECTION_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
