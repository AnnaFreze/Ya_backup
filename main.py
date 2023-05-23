import requests
import os
import json

class VK:

    def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

    def get_photo(self):
        URL = 'https://api.vk.com/method/photos.get'
        params = {
        'owner_id': self.id,
        'access_token': self.token,
        'album_id': 'profile',
        'extended': 1,
        'v': '5.131'
        }
        res = requests.get(URL, params=params)
        return res.json()

    def photo_download(self):
        data = vk.get_photo()
        photos = []
        files_dict = {}
        likes = []
        dates = []
        file_names = []
        file_sizes = []
        json_list = []
        count = 0
        i = 0
        for photo in data['response']['items']:
            photo_url = photo['sizes'][-1]['url']
            photos.append(photo_url)
            like = photo['likes']['count']
            likes.append(like)
            date = photo['date']
            dates.append(date)
            photo_size = photo['sizes'][-1]['type']
            file_sizes.append(photo_size)
        for item in likes:
            if likes.count(item) >= 2:
                file_name = '_'.join([str(item), str(dates[count])])
                file_names.append(file_name)
                count +=1
            else:
                file_name = item
                file_names.append(file_name)
                count +=1
        for file in file_names:
            files_dict[file] = photos[i]
            i += 1
            api = requests.get(files_dict[file])
            with open(os.path.join('images',f'{file}.jpg'), 'wb') as file:
                file.write(api.content)
        for el, size in zip(file_names, file_sizes):
            file_d = {}
            file_d["file_name"] = str(el)
            file_d["size"] = size
            json_list.append(file_d)
        with open("info.json", "w") as f:
            json.dump(json_list, f, ensure_ascii=False, indent=2)
        return file_names

class YaUploader:
    def __init__(self, token: str):
        self.token = ya_token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
    def create_folder(self, path='images_folder'):
        self.path = path
        create_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {"path": path, "overwrite": "true"}
        response = requests.put(create_url, headers=headers, params=params)
        return response.json()

    def get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self. get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_all(self):
        names = vk.photo_download()
        for name in names:
            href = self.get_upload_link(disk_file_path=f'images_folder/{name}.jpg').get('href', '')
            response = requests.put(href, data=open(os.path.join('images', f'{name}.jpg'), 'rb'))
            response.raise_for_status()
            if response.status_code == 201:
                print("Success")

access_token = ''
user_id = ''
vk = VK(access_token, user_id)

if __name__ == '__main__':
    ya_token = ""
    uploader = YaUploader(ya_token)
    uploader.upload_all()
