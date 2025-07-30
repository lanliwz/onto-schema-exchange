## Dependencies


## Install FastAPI
```
pip install "fastapi[all]"
pip install "uvicorn[standard]"
```
### Run it
```uvicorn main:app --reload```

### Home setting
in main.py
```commandline
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse(name="myEntityRelationship.html", context={'request':request})
```
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse(name="myEntityRelationship.html", context={'request':request})

### Used by Pydantic:

* email_validator - for email validation.
* pydantic-settings - for settings management.
* pydantic-extra-types - for extra types to be used with Pydantic.

### Used by Starlette:

* httpx - Required if you want to use the TestClient.
* jinja2 - Required if you want to use the default template configuration.
* python-multipart - Required if you want to support form "parsing", with request.form().
* itsdangerous - Required for SessionMiddleware support.
* pyyaml - Required for Starlette's SchemaGenerator support (you probably don't need it with FastAPI).
* ujson - Required if you want to use UJSONResponse.

### Used by FastAPI / Starlette:

* uvicorn - for the server that loads and serves your application.
* orjson - Required if you want to use ORJSONResponse.

### Reference:
FastAPI Tutorial - User Guide (https://fastapi.tiangolo.com/tutorial/)

### Test FastAPI

```
http://127.0.0.1:8000/docs
```

## Install Tailwindcss
```
npm install -D tailwindcss
npx tailwindcss init
```
### run it
```npx tailwindcss -i tailwind.main.css -o ./static/css/tailwind.local.css```

## GoGS
### install GoJS, Install GoJS using npm install gojs and npm create gojs-kit@latest (to folder static/js)
```
npm install gojs
npm create gojs-kit@latest
```

## This project provides interactive diagrams for better visualization.
- [Entity-Relationship Diagram](http://127.0.0.1:8000/static/my-er-diagram.html)
- [Family Tree Diagram](http://127.0.0.1:8000/static/my-family-tree.html)
- [Workflow Diagram](http://127.0.0.1:8000/static/my-fsm-designer.html)

Make sure your server is running locally at `http://127.0.0.1:8000` to view them.

### run sample
```
https://gojs.net/latest/intro/
http://127.0.0.1:8000/static/js/gojs-kit/samples/absolute.html
http://127.0.0.1:8000/static/js/gojs-kit/samples/addRemoveColumns.html
http://127.0.0.1:8000/static/js/gojs-kit/samples/dataFlow.html
http://127.0.0.1:8000/static/js/gojs-kit/samples/processFlow.html
http://127.0.0.1:8000/static/js/gojs-kit/samples/dataVisualization.html
http://127.0.0.1:8000/static/js/gojs-kit/samples/Dimensioning.html
http://127.0.0.1:8000/static/js/gojs-kit/samples/umlClass.html
http://127.0.0.1:8000/static/js/gojs-kit/samples/stateChart.html

```