# Rest Module Server
Простой RESTapi сервер для ваших программ. Сервер при запуске смотрит папки в каталоге modules, и если он подходит, подключает его.

#### Настройка
Ваш модуль должен содержать файл main.py с методом setup_routes(flask_app), который устанавливает пути для рест-сервиса для вашего приложения. Пример main.py:
```python
from flask import request
from flask.views import MethodView

class UserAPI(MethodView):
	def get(self, id=None):
		return "Success GET"
	def post(self):
		data = request.data # POST data here
        return "Success POST with data"

def setup_routes(flask_app):
	user_view = UserAPI.as_view("app_name")
	flask_app.add_url_rule("/app_route" % settings.MODULE_ROUTE, view_func=user_view)
```

### Запуск
Для запуска запустите файл RestModules.py:
```bash
python3 RestModules.py
```

### Инструменты
- python3
- flask

### Version
0.1

### License
GNU GPLv2
