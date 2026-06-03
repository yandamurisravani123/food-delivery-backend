import os


async def save_file(file):

    upload_dir = "uploads"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    file_path = f"{upload_dir}/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(
            await file.read()
        )

    return file_path