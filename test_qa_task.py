import unittest
import qa_task
import requests
import string
import random
import datetime

class Test_qa_task(unittest.TestCase):

    def setUp(self):
        self.data = {
            'title': 'fav_place',
            'lat': '55.028254',
            'lon': '82.918501' 
            }

    def tearDown(self):
        self.data = {
            'title': 'fav_place',
            'lat': '55.028254',
            'lon': '82.918501' 
            }
    
    # проверка на неправильный тип http запроса
    def test_wrong_http_request(self):
        response = requests.get('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertNotEqual(response.status_code, 200)
    
    # проверка на неправильный сессионный токен
    def test_wrong_session_token(self):
        response = requests.get('https://regions-test.2gis.com/v1/favorites', cookies={'token' : 'wrong_token'}, data=self.data)
        self.assertEqual(response.status_code, 405)

    # проверка широты
    def test_latitude(self):
        # проверка соответствия широты переданному (корректному) значению
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['lat'], 55.028254)
        # проверка на некорректное значение широты по нижней границе (меньше -90)
        self.data['lat'] = '-91'
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['error']['message'], "Параметр 'lat' должен быть не менее -90")
        # проверка на некорректное значение широты по верхней границе (больше 90)
        self.data['lat'] = '91'
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['error']['message'], "Параметр 'lat' должен быть не более 90")
        # проверка на некорректное значение широты по типу данных
        self.data['lat'] = "некорректное значение"
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['error']['message'], "Параметр 'lat' должен быть числом")
        
    # проверка долготы
    def test_longitude(self):
        # проверка соответствия долготы переданному (корректному) значению
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['lon'], 82.918501)
        # проверка на некорректное значение широты по нижней границе (меньше -180)
        self.data['lon'] = '-181'
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['error']['message'], "Параметр 'lon' должен быть не менее -180")
        # проверка на некорректное значение широты по верхней границе (больше 180)
        self.data['lon'] = '181'
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['error']['message'], "Параметр 'lon' должен быть не более 180")
        # проверка на некорректное значение широты по типу данных
        self.data['lon'] = "некорректное значение"
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['error']['message'], "Параметр 'lon' должен быть числом")

    # проверка названия
    def test_title(self):
        # проверка соответствия названия переданному (корректному) значению
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['title'], 'fav_place')
        # проверка на некорректное значение названия по нижней границе (меньше 1)
        self.data['title'] = ''
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['error']['message'], "Параметр 'title' не может быть пустым")
        # проверка на некорректное значение названия по верхней границе (больше 999)
        self.data['title'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=1000))
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['error']['message'], "Параметр 'title' должен содержать не более 999 символов")

    # проверка соответствия дополнительного параметра: цвет
    def test_color(self):
        # проверка для случая, когда цвет не передается
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertIsNone(response.json()['color'])
        # проверка соответствия названия цвета переданному (корректному) значению
        valid_colors = ['BLUE', 'green', 'Red', 'YeLLoW']
        for color in valid_colors:
            self.data['color'] = color
            response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
            self.assertEqual(response.json()['color'], color)
        # проверка на некорректное значение (цвет, невходящий в разрешенный диапазон)
        self.data['color'] = 'pink'
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['error']['message'], "Параметр 'color' может быть одним из следующих значений: BLUE, GREEN, RED, YELLOW")
        # проверка на некорректное значение (некорректный тип данных)
        self.data['color'] = 10
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['error']['message'], "Параметр 'color' может быть одним из следующих значений: BLUE, GREEN, RED, YELLOW")
    
    # проверка типов параметров ответа
    def test_response_parameters_type(self):
        self.data['color'] = 'green'
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertIsInstance(response.json()['id'], int)
        self.assertIsInstance(response.json()['title'], str)
        self.assertIsInstance(response.json()['lat'], float)
        self.assertIsInstance(response.json()['lon'], float)
        self.assertIsInstance(response.json()['color'], str)
        self.assertIsInstance(response.json()['created_at'], str)
    
    # проверка параметра created_at
    def test_created_ad_time(self):
        date_time_in_ISO8601_format = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).replace(microsecond=0).isoformat()
        response = requests.post('https://regions-test.2gis.com/v1/favorites', cookies=qa_task.cookies, data=self.data)
        self.assertEqual(response.json()['created_at'], date_time_in_ISO8601_format)

if __name__=="__main__":
    unittest.main()