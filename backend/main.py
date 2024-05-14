from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.users import users_router
from backend.routers.chats import chats_router
from backend.auth import auth_router


from backend.auth import UserExisted
from backend.database import create_db_and_tables, EntityNotFoundException

from mangum import Mangum


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Pony Express",
    description="API for managing fosters and adoptions.",
    version="0.1.0",
    lifespan=lifespan,

)

app.include_router(users_router)
app.include_router(chats_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://main.d3eififu6izf2.amplifyapp.com"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# decorator version
@app.exception_handler(UserExisted)
def handle_entity_existed(
    _request: Request,
    exception: UserExisted,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "type": "duplicate_value",
                "entity_name": "User",
                "entity_field":  exception.entity_field,
                "entity_value": exception.entity_value,
            },
        },
    )
    
@app.exception_handler(EntityNotFoundException)
def handle_entity_not_found(
    _request: Request,
    exception: EntityNotFoundException,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": {
                "type": "entity_not_found",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )
    
# @app.exception_handler(PermissionNotAllowed)
# def handle_entity_not_found(
#     _request: Request,
#     exception: PermissionNotAllowed,
# ) -> JSONResponse:
#     return JSONResponse(
#         status_code=404,
#         content={
#             "detail": {
#                 "type": "entity_not_found",
#                 "entity_name": exception.entity_name,
#                 "entity_id": exception.entity_id,
#             },
#         },
#     )

    
@app.get("/", include_in_schema=False)
def default() -> str:
    return HTMLResponse(
        content=f"""
        <html>
            <body>
                <h1>{app.title}</h1>
                <p>{app.description}</p>
                <h2>API docs</h2>
                <ul>
                    <li><a href="/docs">Swagger</a></li>
                    <li><a href="/redoc">ReDoc</a></li>
                </ul>
            </body>
        </html>
        """,
    )

lambda_handler = Mangum(app)

# app.add_exception_handler(IDAlreadyExisted, handle_entity_not_found)