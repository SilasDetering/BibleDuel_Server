import os

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
PEPPER = os.environ.get('PEPPER', 'B289EB7F2065F1DA7E849552DD0D7A652FD7F194AF63D711C9D0E7CE41126EC2')
HASHROUNDS = int(os.environ.get('HASHROUNDS', 100000))
JWT_SECRET = os.environ.get('JWT_SECRET', 'secret')
