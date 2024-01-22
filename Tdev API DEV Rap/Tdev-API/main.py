from fastapi import APIRouter, FastAPI, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from JwtAuthentication import has_access
from api.api_v2.api import api_router
from config import settings

# Set up main router, initialize FastAPI app
root_router = APIRouter()

if settings.env == "dev":
    app = FastAPI(title="TADA API", version="2.0")
else:
    app = FastAPI(title="TADA API", version="2.0",
                  docs_url=None, redoc_url=None)


# Add cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

RouteAutheticationGuard = [Depends(has_access)]
# Comment out line 20, and use like 21 when testing API updates
app.include_router(api_router, prefix=settings.API_V2_STR,
                   dependencies=RouteAutheticationGuard)
# app.include_router(api_router, prefix=settings.API_V2_STR)
app.include_router(root_router)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = Response()
    try:
        response = await call_next(request)
    except Exception as e:
        if response.status_code == 200:
            response.status_code = 500
    finally:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Cache-control"] = "no-store, no-cache, max-age=0"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Security-Policy"] = "img-src 'self' https://fastapi.tiangolo.com/img/favicon.png style-src 'self' https://cdn.jsdelivr.net  connect-src 'self'  script-src 'self' https://cdn.jsdelivr.net"
        return response
