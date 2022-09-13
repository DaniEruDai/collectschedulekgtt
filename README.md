# ***Получение расписания с Google Таблицы КГТТ***
____
### Установка
```
pip install collectschedulekgtt
```
### Импорт и инициализация
```python
from collectschedulekgtt import Collector

collector = Collector("Название группы")
```
### Пример

```python
collector = Collector("1ИСИП-21-9")
collector.get_image()  # Вернет расписание для группы 1ИСИП-21-9
```
## Примечание
>Важно чтобы таблица была открытой для общего доступа!
## Полезные ссылки
>[Страница на GitHub](https://github.com/DaniEruDai/collectschedulekgtt)
> | [Страница на PyPi](https://pypi.org/project/collectschedulekgtt)


