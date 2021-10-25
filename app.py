from mimetypes import guess_type

from fastapi import FastAPI
from fastapi.responses import FileResponse, Response

app = FastAPI(
    # docs_url=None,
    # redoc_url=None,
)


@app.get('/')
async def index():
    return {"message": "Hello World"}


@app.get('/{image_name}')
async def image_via_file(image_name: str):
    return FileResponse(
        path=f'originals/{image_name}',
    )


@app.get('/{image_name}')
async def image_via_header(image_name: str):
    """
    Logic: https://github.com/vas3k/i.vas3k.ru/blob/7ff16e05806bbdb211ecdf6fee79eabb39a8b6dc/helpers.py#L70

    Nginx X-Accel Redirect magic.
    That headers will distribute statics files through nginx instead of python.
    Description: https://kovyrin.net/2006/11/01/nginx-x-accel-redirect-php-rails/
    """

    filepath = f'originals/{image_name}'
    return Response(
        media_type=guess_type(filepath)[0],
        headers={'X-Accel-Redirect': filepath},
    )
