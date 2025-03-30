from fastapi import FastAPI
from .routes import data_processing  # Import route from routes folder

app = FastAPI()

# Include the data processing route
app.include_router(data_processing.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to !"}
