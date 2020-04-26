import os
from googleapiclient.discovery import build
import requests


def dir_creation_task(query):
    query_dir = os.path.join(IMAGES_DIR, query)

    if not os.path.exists(query_dir):
        os.makedirs(query_dir)


def make_query():
    while True:
        try:
            query_input = str(input('Image Search >>> '))
            break
        except Exception:
            print('\nAn Error have occoured, try again!\n')

    return query_input.lower()


def search(query):
    GOOGLE_API_KEY = '{YOUR API KEY HERE}'
    SEARCH_ENGINE_ID = '{YOUR SEARCH ENGINE ID HERE}'

    service = build('customsearch', 'v1', developerKey=GOOGLE_API_KEY)
    response = service.cse().list(
        q=query,
        cx=SEARCH_ENGINE_ID,
        searchType='image',
        num=10,
    ).execute()
    return response


def download_images(response, query):
    char_dir = IMAGES_DIR + '/' + query
    images_link = list()
    for image in response['items']:
        images_link.append(image['link'])

    for i, link in enumerate(images_link):
        try:
            print(f'Downloading image {i + 1}/{len(images_link)}')
            img = requests.get(link)
            extension = img.headers['content-type'].split('/')[-1]
            if img.text.startswith('<head>'):
                raise Exception('NOT AVAIBLE ERROR')
        except Exception as err:
            print(f'Can\'t download image {i + 1} by the error {err}')
            continue

        file_name = '/image' + f' {i + 1}' + '.' + extension
        with open(char_dir + file_name, 'wb') as new_img:
            new_img.write(img.content)


def get_images():
    query = make_query()
    response = search(query)
    if not response:
        print('Some error have occoured. Closing the program!')
        quit()
    dir_creation_task(query)
    download_images(response, query)


if __name__ == '__main__':
    CUR_DIR = os.getcwd()
    IMAGES_DIR = os.path.join(CUR_DIR, 'downloads').replace('\\', '/')
    get_images()
