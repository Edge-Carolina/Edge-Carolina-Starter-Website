"""Entrypoint of backend API exposing the FastAPI `app` to be served by an application server such as uvicorn."""

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware



from .api import (
    join,
    static_files,
)

from .services.exceptions import (
    UserRegistrationException,
    UserPermissionException,
    ResourceNotFoundException,
)

__authors__ = ["Weston Voglesonger"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

description = """
Welcome to the Edge Carolina RESTful Application Programming Interface.
"""

# Metadata to improve the usefulness of OpenAPI Docs /docs API Explorer
app = FastAPI(
    title="Edge Carolina API",
    version="0.0.1",
    description=description,
    openapi_tags=[
        join.openapi_tags,
    ],
)

# Use GZip middleware for compressing HTML responses over the network
app.add_middleware(GZipMiddleware)

# Plugging in each of the router APIs
feature_apis = [
    join,
]

for feature_api in feature_apis:
    app.include_router(feature_api.api)

# Static file mount used for serving Angular front-end in production, as well as static assets
app.mount("/", static_files.StaticFileMiddleware(directory=Path("./static")))


# Add application-wide exception handling middleware for commonly encountered API Exceptions
@app.exception_handler(UserPermissionException)
def permission_exception_handler(request: Request, e: UserPermissionException):
    return JSONResponse(status_code=403, content={"message": str(e)})


@app.exception_handler(ResourceNotFoundException)
def resource_not_found_exception_handler(
    request: Request, e: ResourceNotFoundException
):
    return JSONResponse(status_code=404, content={"message": str(e)})

@app.exception_handler(UserRegistrationException)
def user_registration_exception_handler(request: Request, e: UserPermissionException):
    return JSONResponse(status_code=405, content={"message": str(e)})
