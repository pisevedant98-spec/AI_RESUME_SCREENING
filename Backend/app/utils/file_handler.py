import os

UPLOAD_FOLDER = "uploads"

def save_file(file, filename):
    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path