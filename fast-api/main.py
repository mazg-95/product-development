from typing import Optional
from fastapi import FastAPI, Response
from enum import Enum
from pydantic import BaseModel
from random import randint
from fastapi.responses import ORJSONResponse, UJSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse, StreamingResponse, FileResponse
import pandas as pd
import io


fake_items_db = [{"item_name": "uno"}, {"item_name": "dos"}, {"item_name": "tres"}]

class Rolename(str, Enum):
    writer = "Writer"
    admin = "Admin"
    reader = "Reader"

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World, From Galileo Master!"}


@app.get("/items/all", response_class = ORJSONResponse)
def read_all_items():
    return [{"item_id": "uno"}] * 100

@app.get("/items/all/alternative", response_class = UJSONResponse)
def read_all_items_alternative():
    return [{"item_id": "uno"}] * 100

@app.get("/items/{item_id}")
def read_items(item_id: int, query: Optional[str] = None):
    if query:
        return {"item_id": item_id, "query": query}
    return {"item_id": item_id}

@app.get("/users/current")
def read_current_user():
    return {"user_id": "current"}

@app.get("/users/{user_id}")
def current_user(user_id: int):
    return {"user_id": user_id}

@app.get('/roles/{rolename}')
def get_role_permissions(rolename: Rolename):
    if rolename == Rolename.reader:
        return {"role": rolename, "permissions": "You are allowed only to read."}
    if rolename == "writer":
        return {"role": rolename, "permissions": "You are allowed to write and read."}
    return {"role": rolename, "permissions": "You have all access"}

@app.get('/items')
def read_all_items(skip:int = 0, limit:int = 10):
    return fake_items_db[skip: skip + limit]

@app.get("/users/{user_id}/items/{item_id}")
def read_user_items(user_id: int, item_id: int, query: Optional[str] = None, short:bool = False):
    item = {"item_id": item_id, "owner": user_id}
    if query:
        item.update({"query": query})

    if not short:
        item.update({"description": "This is a long description for the item selected."})

    return item

@app.post("/items")
def create_item(item:Item):
    if not item.tax:
        item.tax = item.price * 0.12

    return { "item_id": randint(1, 100), **item.dict()}

@app.put("/items/{item_id}")
def update_item(item_id:int, item:Item):
    return {
        "msg": f"El item {item_id} fue actualizado",
        "item": item
    }

@app.get("/html",  response_class=HTMLResponse)
def get_html():
    return """
    <html>
        <head>
            This is HTML from Python
        </head>
        <body>
            Hello World!
        </body>
    </html>
    """


@app.get("/legacy")
def get_legacy_reponse():
    data = """<?xml version="1.0"?> 
    <shampoo>
    <Header>
        Apply Shampoo Here.
    </Header>   
    <Body>
        You ll have to use soap here
    </Body>
    </shampoo>
    """

    return Response(content=data, media_type="application/xml")


@app.get("/plain", response_class=PlainTextResponse)
def get_plain_text():
    return "Hello World"

@app.get("/redirect")
def redirect():
    return RedirectResponse("https://google.com")

@app.get("/video")
def show_video():
    video_file = open("ejemplo.mp4", mode='rb')
    return StreamingResponse(video_file, media_type='video/mp4')


@app.get("/video/donwload")
def show_video():
    return FileResponse("ejemplo.mp4")

@app.get('/csv')
def download_csv():
    df = pd.DataFrame({'col1': [1,2], 'col2': [3,4]})

    stream = io.StringIO()

    df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]), media_type='text/csv')
    response.headers['Content-Disposition'] = "attachment; filename=export.csv"
    return response

