from jose import jwt
from jose.exceptions import JOSEError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config import settings
from jwtUtils import rsa_pem_from_jwk
import requests

security = HTTPBearer()

async def has_access(credentials: HTTPAuthorizationCredentials= Depends(security)):
    """
        Function that is used to validate the token in the case that it requires it
    """
    token = credentials.credentials
    header_data=jwt.get_unverified_header(token)
    public_key = get_public_key(token)

    try:
        payload = jwt.decode(token, public_key,algorithms=[header_data['alg']], audience=settings.aud, issuer=settings.iss, \
                             options={"verify_signature": True,
                                      "verify_aud": True,
                                      "verify_iss": True
                                    })
        return payload["unique_name"]
    
    except JOSEError as e:  # catches any exception
        raise HTTPException(
            status_code=401,
            detail=str(e))
    

def get_kid(token):
    headers = jwt.get_unverified_header(token)
    if not headers:
        raise InvalidAuthorizationToken('missing headers')
    try:
        return headers['kid']
    except KeyError:
        raise InvalidAuthorizationToken('missing kid')


def get_jwk(kid):
    jwks_uri = settings.jwks_uri
    jwkeys = requests.get(jwks_uri).json()['keys']
    for jwk in jwkeys:
        if jwk.get('kid') == kid:
            return jwk
    raise InvalidAuthorizationToken('kid not recognized')


def get_public_key(token):
    return rsa_pem_from_jwk(get_jwk(get_kid(token)))

  

class InvalidAuthorizationToken(Exception):
    def __init__(self, details):
        super().__init__('Invalid authorization token: ' + details)    