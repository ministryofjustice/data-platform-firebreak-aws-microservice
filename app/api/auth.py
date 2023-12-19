from typing import Optional

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes
from pydantic import BaseModel

from app.api import exceptions
from app.core.config import get_settings

token_auth_scheme = HTTPBearer()

settings = get_settings()


class TokenData(BaseModel):
    scopes: str = ""


class VerifyToken:
    def __init__(self) -> None:
        self.jwks_url = f"https://{settings.oidc_domain}/.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(self.jwks_url)

    async def verify(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
    ):
        if token is None:
            raise exceptions.UnauthenticatedException

        # This gets the 'kid' from the passed token
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token.credentials).key
        except jwt.exceptions.PyJWKClientError as error:
            raise exceptions.UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            raise exceptions.UnauthorizedException(str(error))

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=settings.oidc_algorithms,
                audience=settings.oidc_api_audience,
                issuer=settings.oidc_issuer,
            )
        except Exception as error:
            raise exceptions.UnauthorizedException(str(error))

        token_data = TokenData(scopes=payload.get("scope"))
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise exceptions.UnauthorizedException(f"Missing required scope '{scope}'")

        return payload
