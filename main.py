# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from myroutes.graph_ws import router, periodic_refresh_task
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: launch the Neo4j poller
    task = asyncio.create_task(periodic_refresh_task(interval_sec=10))
    print("🚀 Started periodic Neo4j refresh task.")
    yield
    # Shutdown: cancel the poller
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("🛑 Poller stopped gracefully.")

app = FastAPI(lifespan=lifespan)
app.include_router(router)

app = FastAPI(lifespan=lifespan)

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

# routes
# from myroutes import ent_data_websocket
# app.include_router(ent_data_websocket.router)

# routes
from myroutes import graph_ws
app.include_router(graph_ws.router)

