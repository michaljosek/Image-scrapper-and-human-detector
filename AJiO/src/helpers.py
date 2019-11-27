import urllib.request as urllib
import os
import shutil
import requests
import glob


def get_folder_path():
    return os.path.dirname(os.path.abspath(__file__))


def get_input_folder_path():
    return os.path.join(get_folder_path(), 'input')


def get_output_folder_path():
    return os.path.join(get_folder_path(), 'output')


def get_website_content(url):
    try:
        req = requests.get(url)
    except:
        return False, ''

    if req.status_code != 200:
        return False, ''

    return True, req.content


def get_new_image_file_name_if_already_exists(file_name):
    name, extension = os.path.splitext(file_name)
    i = 0
    while os.path.exists(os.path.join(get_input_folder_path(), f"{name}{i}{extension}")):
        i += 1

    return f"{name}{i}{extension}"


def download_images(image_urls):
    for image_url in image_urls:
        download_image(image_url)


def download_image(path):
    resource = urllib.urlopen(path)
    url_file_name = os.path.basename(path)
    image_file_name = get_new_image_file_name_if_already_exists(url_file_name)

    output = open(os.path.join(get_input_folder_path(), image_file_name), "wb")
    output.write(resource.read())
    output.close()

    return


def ensure_folder_exists_and_is_empty(path):
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)

    if not os.path.exists(path):
        os.makedirs(path)
    return


def ensure_input_folder_exists_and_is_empty():
    return ensure_folder_exists_and_is_empty(get_input_folder_path())


def ensure_output_folder_exists_and_is_empty():
    return ensure_folder_exists_and_is_empty(get_output_folder_path())


def get_files_from_folder(path):
    os.chdir(path)
    array = []
    for x in glob.glob("*"):
        array.append(x)
    return array


def get_input_files():
    return get_files_from_folder(get_input_folder_path())


def get_output_files():
    return get_files_from_folder(get_output_folder_path())


def get_image_urls_from_content(content):

    return []
