import sys
import requests

# Данные авторизации в API Trello
auth_params = {
    'key': "180fdf04b2f5e869bbd4d3d390ccf4ec",
    'token': "dbea7275df02ff833c2a1ec294c5c6a5f214f43b3a971f65f2bb1588fc1c889b", }

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.
base_url = "https://api.trello.com/1/{}"

board_id = "yQ4gJ7L4"

def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print("{} ({})".format(column['name'], len(task_data)))
        # Получим данные всех задач в колонке и перечислим все названия

        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])

def create(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break

def create_column(column_name):

    response = requests.post(
        base_url.format('boards') + '/' + board_id + '/lists',
        data = {
            'name': column_name,
            **auth_params
        }
    )

    print(response.text)

def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = find_all_tasks(name)

    # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу

    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            break
    read()

def find_all_tasks(name):
    class TaskObj:
        def __init__(self, id, task_id, task_name, column_id, column_name):
            self.id = id
            self.task_id = task_id
            self.task_name = task_name
            self.column_id = column_id
            self.column_name = column_name

    tasks = []
    task_id = None

    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    id = 0
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                id +=1
                tasks.append(TaskObj(id, task['id'], task['name'], column['id'], column['name']))
    if id>0:
        print("Задача содержится в следующих карточках:")
        for item in tasks:
            print("{}.'{}' в карточке '{}'".format(item.id, item.task_name, item.column_name))
        tasks_id = int(input("Выберите номер нужной задачи: "))
        task_id, column_id = [[item.task_id, item.column_id] for item in tasks if item.id == tasks_id][0]

    return task_id



if __name__ == "__main__":
    if len(sys.argv) <= 1:
        read()
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])