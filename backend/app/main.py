from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.routers import auth, programs, terms, lessons, users, catalog
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="CMS Catalog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


security = HTTPBearer()
@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(programs.router)
app.include_router(terms.router)
app.include_router(lessons.router)
app.include_router(users.router)
app.include_router(catalog.router)
