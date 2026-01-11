from fastapi import FastAPI
from app.routers import auth, programs, terms, lessons, users, catalog


app = FastAPI(title="CMS Catalog API")

@app.get("/health")
def health():
    return {"status": "ok"}
app.include_router(auth.router)

app.include_router(auth.router)
app.include_router(programs.router)
app.include_router(terms.router)
app.include_router(lessons.router)
app.include_router(users.router)
app.include_router(catalog.router)
