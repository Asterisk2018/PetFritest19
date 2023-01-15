from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password,valid_email_2,valid_password_2
import os

pf = PetFriends()

#1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что с использованием валидных email и пароля получаем ключ API. Код ответа 200"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

#2
def test_get_all_pets_with_valid_key(filter='my_pets'):
    """ Проверяем, что запрос всех питомцев пользователя возвращает не пустой список.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

#3
def test_add_new_pet_with_valid_data(name='тобик', animal_type='собака',
                                     age='2', pet_photo='images/2.jpeg'):
    """Проверяем, что можно добавить питомца с корректными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#4
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Мосик", "пингвин", '2', 'images/1.jpeg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

#5
def test_successful_update_self_pet_info(name='Боба', animal_type='Медведь', age='8'):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Негативные тесты
#1
def test_get_api_key_for_valid_user_and_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем, что запрос api ключа пользователя с вводом не верного пароля возвращает статус 403."""
    status, result = pf.get_api_key(email, password)
    assert status == 403

#2
def test_get_api_key_for_invalid_user(email=valid_email_2, password=valid_password_2):
    """ Проверяем, что запрос api ключа пользователя возвращает статус 403 при попытке авторизироватся
    незарегистрированому пользователю."""
    status, result = pf.get_api_key(email, password)
    assert status == 403

#3
def test_get_api_key_for_valid_user_and_invalid_mail(email=invalid_email, password=valid_password):
    """ Проверяем, что запрос api ключа пользователя с вводом не верного адреса email возвращает статус 403."""
    status, result = pf.get_api_key(email, password)
    assert status == 403

#4
def test_add_new_pet_without_photo_with_invalid_name(name='1245', animal_type='слон', age='5'):
    """Проверяем, что поле ввода имени питомца принимает цифры."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200

#5
def test_add_new_pet_without_photo_with_negative_age(name='Тоня', animal_type='мартышка', age='-100'):
    """Проверяем, что можно добавить питомца с отрицательным значением возраста."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200

#6
def test_add_new_pet_without_photo_with_invalid_age(name='Кеша', animal_type='сом', age='тысячапятьсот'):
    """Проверяем, что можно добавить питомца с тектовым значением возраста."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200

#7
def test_add_new_pet_without_photo_with_invalid_animal_type(name='Шустрик', animal_type='125478', age='2'):
    """Проверяем, что поле ввода породы питомца может принимать цифры."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200

#8
def test_add_new_pet_without_photo_with_invalid_parameters(name='"№;%:?*?*"', animal_type='(*?:%;№)', age='"%:*)*:%"'):
    """Проверяем, что поля для ввода параметров питомца принимают символы."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200

#9
def test_add_new_pet_with_invalid_photo(name='Тобик', animal_type='собака', age='1', pet_photo='images/8.jpeg'):
        """Проверяем, что нельзя добавить фото, которого нет в папке images."""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        try:
            status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        except FileNotFoundError:
            print("Такого файла не существует")

#10
def test_add_new_pet_with_invalid_photo_format(name='Тузик', animal_type='пёс', age='1', pet_photo='images/1.txt'):
        """Проверяем, что нельзя добавить текстовый файл."""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        try:
            status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        except FileNotFoundError:
            print("Не верный формат файла")

