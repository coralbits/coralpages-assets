import fastapi
from fastapi.templating import Jinja2Templates
import pathlib

from am.storage.factory import get_storage

templates = Jinja2Templates(directory=pathlib.Path(__file__).parent / "templates")


routes = fastapi.APIRouter()


@routes.get("/favicon.ico")
async def favicon():
    return fastapi.responses.PlainTextResponse(
        "Not found", media_type="text/plain", status_code=404
    )


@routes.get("/style.css")
async def style():
    with open(
        pathlib.Path(__file__).parent / "templates" / "style.css", "r", encoding="utf-8"
    ) as f:
        return fastapi.responses.PlainTextResponse(f.read(), media_type="text/css")


@routes.get("/")
async def root(request: fastapi.Request):
    storage = get_storage("default")
    buckets = storage.list_buckets()

    return templates.TemplateResponse(
        "buckets.html", {"request": request, "buckets": buckets}
    )


@routes.get("/{bucket}")
async def files(request: fastapi.Request, bucket: str):
    storage = get_storage(bucket)
    files = storage.list_files(bucket)
    print(files)
    return templates.TemplateResponse(
        "files.html", {"request": request, "files": files, "bucket": bucket}
    )
