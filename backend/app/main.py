from fastapi import FastAPI

app = FastAPI(title="CMS Catalog API")

@app.get("/health")
def health():
    return {"status": "ok"}
