# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# home
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
templates = Jinja2Templates(directory='templates')
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    # myEntityRelationship
    return templates.TemplateResponse(name="index.html", context={'request':request})

# templates
@app.get("/myitems/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(name="item.html", context={'request':request, 'id': id})

# public/static
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

# routes
from myroutes import mytest
app.include_router(mytest.router)

# routes
from myroutes import gojs_service
app.include_router(gojs_service.router)

