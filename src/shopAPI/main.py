import uvicorn
from api.server import app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
