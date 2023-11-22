import logging.config

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import auth, registration, roles, sessions, user, users
from core.logging import LOGGING
from core.settings import settings
from db import redis

logging.config.dictConfig(LOGGING)

app = FastAPI(
    title='auth',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = Redis.from_url(settings.redis_dsn)


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()


app.include_router(registration.router, prefix='/api/v1', tags=['Регистрация'])
app.include_router(auth.router, prefix='/api/v1', tags=['Авторизация'])
app.include_router(user.router, prefix='/api/v1/user',
                   tags=['Профиль пользователя'])
app.include_router(sessions.router, prefix='/api/v1/user/sessions',
                   tags=['История входов в аккаунт'])
app.include_router(roles.router, prefix='/api/v1/roles',
                   tags=['Управление ролями'])
app.include_router(users.router, prefix='/api/v1/users',
                   tags=['Управление доступами'])


@AuthJWT.load_config
def get_config():
    return settings


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return ORJSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.message}
    )


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(decrypted_token):
    return await redis.redis.get(decrypted_token['jti'])
