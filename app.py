from mimetypes import guess_type

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pathlib import Path

from admin import router as admin_router

app = FastAPI(
    docs_url=None,
    redoc_url=None,
)

app.include_router(admin_router)


@app.get('/{image_name}')
async def get_image(image_name: str):
    """
    Logic: https://github.com/vas3k/i.vas3k.ru/blob/7ff16e05806bbdb211ecdf6fee79eabb39a8b6dc/helpers.py#L70

    Nginx X-Accel Redirect magic.
    That headers will distribute statics files through nginx instead of python.
    Description: https://kovyrin.net/2006/11/01/nginx-x-accel-redirect-php-rails/
    """

    filepath = f'originals/{image_name}'

    if not Path(filepath).is_file():
        raise HTTPException(status_code=404, detail='image not found')

    return Response(
        media_type=guess_type(filepath)[0],
        headers={'X-Accel-Redirect': filepath},
    )
