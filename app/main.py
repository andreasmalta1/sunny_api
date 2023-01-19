from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


try:
    from app.routers import auth, favicon, quote, user
except ImportError:
    from routers import auth, favicon, quote, user


tags_metadata = [
    {
        "name": "Quptes",
        "description": "You can get quotes from the show with information including season, episode and character that said the actual quote",
    }
]


description = """  :sunny:
The ItsSunnyAPI :sunny: provides data regarding the popular American sitcom 'It's Always Sunny in Philadephia' created by Rob McElhenney. The date provided by this api included quotes from all seasons and episodes of the show, data about each season and episode as well as data about the main characters of the show. The API is constantly updated with new data. If any data is missing or incorrect, contact me on andreascalleja@gmail.com have it fixed. 💻
<br></br>
Please see each get request for more information including query parameters.
"""

app = FastAPI(
    title="Sunny Info Api",
    description=description,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    version="1.0.0",
    contact={
        "name": "Andreas Calleja",
        "email": "andreascalleja@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
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
