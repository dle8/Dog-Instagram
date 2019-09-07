import datetime
import jwt

from main.config import config


def encode(account):
    iat = datetime.datetime.utcnow()
    return jwt.encode({
        'sub': account.email,
        'iat': iat,
        'exp': iat + datetime.timedelta(days=365),
    }, config.JWT_SECRET)


def decode(access_token, audience):
    try:
        payload = jwt.decode(access_token, config.JWT_SECRET)
    except jwt.InvalidTokenError:
        return None
    return payload
