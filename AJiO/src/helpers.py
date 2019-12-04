import urllib.request as urllib
import os
import shutil
import requests
import glob
from urllib.parse import urlparse


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


def get_file_name_for_image(path, content_type):
    url_file_name = os.path.basename(path)
    content_type = content_type.split('/')[1]
    if '?' in url_file_name:
        url_file_name = url_file_name.split('?')[0]

    if '.' not in url_file_name:
        url_file_name = url_file_name + '.' + content_type

    return get_new_image_file_name_if_already_exists(url_file_name)


def download_image(path):
    try:
        resource = urllib.urlopen(path)
        content_type = resource.headers.get('Content-Type')
        image_file_name = get_file_name_for_image(path, content_type)
    except Exception as e:
        print('Could not fetch file: ', path, ' ', str(e))
        return

    try:
        output = open(os.path.join(get_input_folder_path(), image_file_name), "wb")
        output.write(resource.read())
    finally:
        output.close()

    return


def ensure_folder_exists_and_is_empty(path):
    if os.path.exists(path) and os.path.isdir(path):
        try:
            shutil.rmtree(path, ignore_errors=True)
        except:
            print('Error while deleting directory')

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            print('Error while making directory')

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


def get_absolute_image_urls(image_urls, path):
    for i, url in enumerate(image_urls):
        if url.count('.') > 1:
            continue
        elif url.startswith('http'):
            continue
        elif url.startswith('/'):
            parsed_uri = urlparse(path)
            domain_url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
            image_urls[i] = domain_url + url
        else:
            image_urls[i] = path + url

    return image_urls


def get_image_urls_from_content(content, url):
    content = content.decode('utf-8')
    size = len(content)
    image_urls = []
    i = 0

    while i < size:
        if content[i] != '<':
            i = i + 1
            continue

        i = i + 1
        img_tag_name = content[i:i+3]
        if img_tag_name != 'img':
            continue

        while content[i:i+3] != 'src':
            i = i + 1

        quote_character = content[i+4]
        start = i + 5
        j = start
        while content[j] != quote_character:
            j = j + 1

        end = j
        image_urls.append(content[start:end])
        i = i + end - start

    return get_absolute_image_urls(image_urls, url)
