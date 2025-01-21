from fastapi import FastAPI, Request, Depends
from db.database import engine, SessionLocal
import models
from api import users, messages, channels
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
app.include_router(channels.router, prefix="/channels", tags=["channels"])

