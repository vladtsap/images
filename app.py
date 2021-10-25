from mimetypes import guess_type

import aiofiles
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import Response, FileResponse, HTMLResponse
from pathlib import Path

app = FastAPI(
    # docs_url=None,
    # redoc_url=None,
)


@app.post("/upload-file/")
async def upload_file(in_file: UploadFile = File(...)):
    async with aiofiles.open(f'originals/{in_file.filename}', 'wb') as out_file:
        content = await in_file.read()
        await out_file.write(content)

    link_to_file = f'http://localhost:8000/{in_file.filename}'
    return HTMLResponse(content=f"""
    <body>
        <a href="{link_to_file}" target="_blank">{link_to_file}</a>
    </body>
    """)


@app.get("/")
async def main():
    content = """
    <body>
        <form action="/upload-file/" enctype="multipart/form-data" method="post">
            <input name="in_file" type="file">
            <input type="submit">
        </form>
    </body>
    """
    return HTMLResponse(content=content)


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

    return FileResponse(
        path=f'originals/{image_name}',
    )

    # return Response(
    #     media_type=guess_type(filepath)[0],
    #     headers={'X-Accel-Redirect': filepath},
    # )
