import uuid
import os

# handle the path for uploading pictures
def upload_path_handler(instance, filename):
    filename = os.path.splitext(filename)
    file_name = filename[0] + '_' + str(uuid.uuid4()) + filename[1]
    return "pics_uploaded/{id}/{file}".format(id=instance.author.username, file=file_name)
