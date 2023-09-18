from api import PetFriends
from settings import valid_email, valid_password
from settings import  unvalid_email, unvalid_pass
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Получить уникальный ключ по валидным данным пользователя """
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_unvalid_email(email=unvalid_email, password=valid_password):
    """Получить уникальный ключ c невалидной почтой. Ошибка 4хх"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_unvalid_pass(email=valid_email, password=unvalid_pass):
    """Получить уникальный ключ с невалидным паролем."""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Kika', animal_type='cat',
                                     age ='1', pet_photo='images/cat2.jpg'):
    """Добавление нового пета с фото"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_unvalid_name(name='Ki ?/{]ka', animal_type='cat',
                                     age ='1', pet_photo='images/cat2.jpg'):
    """Добавление нового пета с фото, в имени будут пробелы и лишние символы.Должна быть ошибка 4хх"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert result['name'] == name

def test_add_new_pet_with_unvalid_png(name='Kilka', animal_type='cat',
                                     age ='1', pet_photo='images/cat2.png'):
    """Добавление нового пета с фото некоректным форматом. Выдаст ошибку 4хх"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert result['name'] == name

def test_add_new_pet_with_unvalid_name(name='Kilka', animal_type='cat',
                                     age ='1', pet_photo='images/cat2.jpg'):
    """Добавление нового пета с цифровым значением в имени. Выдаст ошибку 4хх"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert result['name'] == name

def test_add_new_pet_with_unvalid_age(name='Kilka', animal_type='cat',
                                     age ='-1', pet_photo='images/cat2.jpg'):
    """Добавление нового пета с фото, имея отрицательный возраст. Запрос должен выдать ошибку 4хх"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Удалить питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Kilka", "cat", "1")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_update_self_pet_info_age_symvols(name='', animal_type='', age='cdsfку1'):
        """Поле "возраст" - ввести символы. Запрос должен выдать ошибку 4хх."""
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info_incorrect(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status == 400
        else:
            raise Exception("There is no my pets")

