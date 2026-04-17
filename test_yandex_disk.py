import pytest
import requests

from config import API_BASE, RESOURCES_PATH, UPLOAD_PATH


TEST_DIR_PATH = "/test_yandex_disk_api_tests"
TEST_FILE_PATH = f"{TEST_DIR_PATH}/test_file.txt"
RENAMED_FILE_PATH = f"{TEST_DIR_PATH}/renamed_test_file.txt"


def test_get_disk_info(auth_headers):
    """GET /v1/disk – базовая проверка информации о диске."""
    url = f"{API_BASE}"
    response = requests.get(url, headers=auth_headers)
    assert response.status_code == 200
    j = response.json()
    assert "used_space" in j
    assert "total_space" in j


def test_put_create_folder(auth_headers):
    """PUT /v1/disk/resources – создание тестовой папки."""
    url = f"{API_BASE}{RESOURCES_PATH}"
    params = {"path": TEST_DIR_PATH}
    response = requests.put(url, headers=auth_headers, params=params)
    # 201 – создано, 202 – асинхронно, 409 – уже существует
    assert response.status_code in [201, 202, 409]


def test_get_upload_link(auth_headers):
    """GET /v1/disk/resources/upload – получение ссылки для загрузки файла."""
    url = f"{API_BASE}{UPLOAD_PATH}"
    params = {"path": TEST_FILE_PATH, "overwrite": "true"}
    response = requests.get(url, headers=auth_headers, params=params)
    assert response.status_code == 200
    j = response.json()
    assert "href" in j


def test_get_resource_info(auth_headers):
    """GET /v1/disk/resources – информация о файле."""
    url = f"{API_BASE}{RESOURCES_PATH}"
    params = {"path": TEST_FILE_PATH}
    response = requests.get(url, headers=auth_headers, params=params)
    if response.status_code == 404:
        pytest.skip("Файл ещё не загружен или не успел появиться в индексе.")
    assert response.status_code == 200
    j = response.json()
    assert j.get("type") == "file"
    assert j.get("name") == "test_file.txt"


def test_get_resources_list(auth_headers):
    """GET /v1/disk/resources – список содержимого папки."""
    url = f"{API_BASE}{RESOURCES_PATH}"
    params = {"path": TEST_DIR_PATH}
    response = requests.get(url, headers=auth_headers, params=params)
    assert response.status_code == 200
    j = response.json()
    # Яндекс возвращает в _embedded.items
    assert "_embedded" in j
    embedded = j["_embedded"]
    assert "items" in embedded
    items = embedded["items"]
    # Может быть пустой список, если папка пуста
    assert isinstance(items, list)


# def test_post_move_resource(auth_headers):
#     """POST /v1/disk/resources/move – перемещение/переименование файла."""
#     url = f"{API_BASE}{RESOURCES_PATH}/move"
#     params = {
#         "from": TEST_FILE_PATH,
#         "path": RENAMED_FILE_PATH,
#         "overwrite": "true",
#     }
#     response = requests.post(url, headers=auth_headers, params=params)
#     # 201 – успешно перемещено, 202 – асинхронно
#     assert response.status_code in [201, 202]


def test_delete_resource(auth_headers):
    """DELETE /v1/disk/resources – удаление файла."""
    url = f"{API_BASE}{RESOURCES_PATH}"
    params = {"path": RENAMED_FILE_PATH, "permanently": "true"}
    response = requests.delete(url, headers=auth_headers, params=params)
    # 204 – удалено, 202 – асинхронно, 404 – не найдено (не ошибка)
    assert response.status_code in [202, 204, 404]


def test_delete_folder(auth_headers):
    """DELETE /v1/disk/resources – удаление тестовой папки."""
    url = f"{API_BASE}{RESOURCES_PATH}"
    params = {"path": TEST_DIR_PATH, "permanently": "true"}
    response = requests.delete(url, headers=auth_headers, params=params)
    assert response.status_code in [202, 204, 404]