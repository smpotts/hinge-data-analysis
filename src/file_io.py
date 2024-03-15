import os
import base64

# define the directory where uploaded files will be stored
UPLOAD_DIRECTORY = "../data/app_uploaded_files"


def save_file(content, name):
    """
    Decode and store a file uploaded with Plotly Dash.
    """
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

