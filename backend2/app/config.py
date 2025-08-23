from urllib.parse import quote_plus

password = quote_plus('Mydeen0302@')

class Config:
    # SQLALCHEMY_DATABASE_URI = f'postgresql://mydeen:{password}@postgres:5432/mydb'
    SQLALCHEMY_DATABASE_URI = f'postgresql://mydeen:{password}@host.docker.internal:5432/mydb'
    JWT_SECRET_KEY = 'alpha@zone'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    