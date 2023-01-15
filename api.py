import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """API библиотека сайта PetFriends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

# 1
    def get_api_key(self, email, password):
        """Этот метод позволяет получить ключ API, который следует использовать для других методов API"""
        headers = {
            "email": email,
            "password": password
        }
        res = requests.get(self.base_url+"api/key", headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

# 2
    def get_list_of_pets(self, auth_key, filter):
        """Этот метод позволяет получить список домашних животных. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""
        headers = {"auth_key": auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+"api/pets", headers=headers, params=filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

# 3
    def add_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        """Этот метод позволяет добавлять информацию о новом питомце с фотографией."""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status,result

# 4
    def delete_pet(self, auth_key, pet_id):
        """Этот метод позволяет удалить информацию о питомце из базы данных."""
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

# 5
    def update_pet_info(self, auth_key, pet_id, name, animal_type, age):
        """Этот метод позволяет обновлять информацию о домашнем животном."""
        headers = {'auth_key': auth_key['key']}
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age
            }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

# 6
    def add_new_pet_without_photo(self, auth_key, name, animal_type, age):
        """Этот метод позволяет добавлять информацию о новом питомце без фотографии.
        Результат в формате JSON"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

# 7
    def add_pet_photo(self, auth_key, pet_id, pet_photo):
        """Этот метод позволяет добавить фотографию домашнего животного.
        Результат в формате JSON с обновленными данными питомца."""
        data = MultipartEncoder(
            fields={
                    'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result