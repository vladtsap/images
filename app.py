from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from admin import router as admin_router

app = FastAPI(
    docs_url=None,
    redoc_url=None,
)

app.include_router(admin_router)


@app.get('/{image_name}')
async def get_image(image_name: str):
    filepath = f'originals/{image_name}'

    if not Path(filepath).is_file():
        raise HTTPException(status_code=404, detail='image not found')

    return FileResponse(
        path=filepath,
    )
