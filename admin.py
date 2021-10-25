from typing import List

import aiofiles
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
from pathlib import Path

from config import IMAGE_EXTENSIONS, WEBSITE_PATH

router = APIRouter(
    prefix='/admin',
)


@router.get('/upload')
async def page_for_uploading():
    content = """
    <body>
        <form action="/admin/upload-files" enctype="multipart/form-data" method="post">
            <input name="in_files" type="file" multiple>
            <input type="submit">
        </form>
    </body>
    """
    return HTMLResponse(content=content)


@router.post('/upload-files')
async def upload_files(in_files: List[UploadFile] = File(...)):
    page = "<body>"

    for in_file in in_files:
        filename = in_file.filename.lower()
        async with aiofiles.open(f'originals/{filename}', 'wb') as out_file:
            content = await in_file.read()
            await out_file.write(content)

        link_to_file = f'{WEBSITE_PATH}/{filename}'
        page += f"""<a href="{link_to_file}" target="_blank">{link_to_file}</a><br>"""

    page += "</body>"
    return HTMLResponse(content=page)


@router.get('/images')
async def images_list():
    images = []
    directory = Path('originals')

    for extension in IMAGE_EXTENSIONS:
        for image_path in directory.glob(f'*.{extension}'):
            images.append(image_path.name)

    page = "<body><h3>Images:</h3><ul>"
    for image in images:
        page += f"""<li><a href="{WEBSITE_PATH}/{image}" target="_blank">{image}</a></li>"""
    page += "</ul></body>"

    return HTMLResponse(content=page)
