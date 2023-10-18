# Словарь с топиками и собираемыми из них параметрами
import asyncio
import threading
from datetime import datetime
import json
import xml.etree.ElementTree as ET

# Создаем корневой элемент
root = ET.Element('root')

SUB_TOPICS = {
    'motion': 'motion',
    'level': 'level',
    'illuminance': 'illuminance',
    'temperature': 'temperature'
}

JSON_LIST = []

# Создание словаря для хранения данных JSON
JSON_DICT = {}
for value in SUB_TOPICS.values():
    JSON_DICT[value] = 0

def on_message(topic, msg):
    """ Функция, вызываемая при получении сообщения от брокера по одному из отслеживаемых топиков

    Arguments:
    client - Экземпляр класса Client, управляющий подключением к брокеру
    userdata - Приватные данные пользователя, передаваемые при подключениии
    msg - Сообщение, приходящее от брокера, со всей информацией
    """

    param_name = SUB_TOPICS[topic]
    JSON_DICT[param_name] = msg
    time = str(datetime.now())
    JSON_DICT['time'] = str(datetime.now())
    JSON_DICT['ip'] = 17

    JSON_LIST.append(JSON_DICT.copy())

    data = ET.SubElement(root, 'data')
    # Пробегаемся по словарю и формируем XML
    for key in JSON_DICT:
        item = ET.SubElement(data, key)
        item.text = str(JSON_DICT[key])

async def saveToJsonAndXML():
    thread = threading.Timer
    # Запись данных в файл
    with open('data.json', 'w') as file:
        json_string = json.dumps(JSON_LIST)  # Формирование строки JSON из словаря
        file.write(json_string)

    # Запись в XML
    mydata = ET.tostring(root).decode()
    with open("data.xml", "w") as file:
        file.write(str(mydata))

    await asyncio.sleep(5)  # Ожидание 5 секунд

async def main():
    # Запускаем цикл асинхронных задач
    asyncio.create_task(saveToJsonAndXML())
    while True:
        topic, msg = str(input()).split(' ')
        if topic == 'q':
            return
        on_message(topic, msg)
        await saveToJsonAndXML()


if __name__ == "__main__":
    asyncio.run(main())
