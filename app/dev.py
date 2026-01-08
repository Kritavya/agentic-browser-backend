import uvicorn

def run():
    uvicorn.run(
        "app.main:app",
        reload=True
    )
