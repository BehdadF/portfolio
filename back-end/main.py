from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Cheatsheet API"}

@app.get("/cheatsheet/{name}")
def get_cheatsheet(name: str):
    data = {
        "vim": {"title": "Vim Cheatsheet", "content": ["Command 1", "Command 2"]},
        "shell": {"title": "Shell Cheatsheet", "content": ["Command A", "Command B"]},
    }
    return data.get(name, {"error": "Cheatsheet not found"})
