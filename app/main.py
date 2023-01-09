from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


try:
    from app.routers import auth, favicon, quote, user
except ImportError:
    from routers import auth, favicon, quote, user

app = FastAPI(
    title="Sunny Info Api",
    description="API for all things 'It's Always Sunny in Philadephia",
    version="0.0.1",
    terms_of_service="",
    contact={
        "name": "Andreas Calleja",
        "email": "andreascalleja@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)
app.include_router(favicon.router)
app.include_router(quote.router)
app.include_router(user.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home_dir():
    return {"home": "success"}
