from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.router import router  # Import the router module correctly

app = FastAPI()

# Serve static files (e.g., the index.html for the UI)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Root endpoint to serve the HTML file
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("app/static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Including the query and upload router
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
