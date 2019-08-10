#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Запуск по умолчанию: ./start.py --protocol https --host 192.168.1.1 --port 8443 --login admin --passwd radmin

import requests
import json
import re
import sys
import progressbar
from datetime import datetime
from terminaltables import AsciiTable

# Библиотека запросов
import librequests
# Библиотека парсеров
import parser_route_config
import parser_netstatus_routes

print('\x1b[1;32;40m' + datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") + ' скрипт запущен: ' + '\x1b[0m')

# Читаем переменные переданные в скрипт
arg_all_ = ''
for arg_ in sys.argv:
    arg_all_ += str(arg_) + ' '
print (arg_all_)

# С помощью регулярных вырожений назначаем значение параметров
try:
    protocol_ = str(re.findall(r'--protocol.(\w+)', arg_all_, re.MULTILINE | re.DOTALL)[0])
    host_ = str(re.findall(r'--host.(\d+.\d+.\d+.\d+)', arg_all_, re.MULTILINE | re.DOTALL)[0])
    port_ = str(re.findall(r'--port.(\d+)', arg_all_, re.MULTILINE | re.DOTALL)[0])
    login_ = str(re.findall(r'--login.(\w+)', arg_all_, re.MULTILINE | re.DOTALL)[0])
    password_ = str(re.findall(r'--passwd.(\w+)', arg_all_, re.MULTILINE | re.DOTALL)[0])
except:
    print('Ошибка, заданы не все параметры: ' + arg_all_)
    print('Формат: ./start.py --protocol https --host 192.168.1.1 --port 8443 --login admin --passwd radmin')
    exit()

print('----------------------------------------------------------')
print('IP-address = ' + protocol_ + '://' + host_ + ':' + port_)
print('login = ' + login_)
print('password = ' + password_)

# Чтение параметров из файла
print('----------------------------------------------------------')
print('\x1b[1;32;40m' + ' Шаг-1: Загрузка параметров ' + '\x1b[0m')

parameters_file_ = 'parameters.json'
try:
    with open(parameters_file_, 'r', encoding='utf-8') as read_file_:
        parameters_ = json.load(read_file_)
    print(parameters_['name'])
    print('Описание: ' + parameters_['description'])
    timeout_ = parameters_['timeout']
    timeout_start_ = parameters_['timeout_start']
    print('Время ожидания ответа от Рубикон: ' + str(timeout_) + ' сек')
    print('Время ожидания загрузки Рубикон: ' + str(timeout_start_) + ' сек')
# print (parameters)
except:
    print('Ошибка чтения файла конфигурации: ' + parameters_file_)
    exit()

# Чтение словаря из файла
print('----------------------------------------------------------')
print('\x1b[1;32;40m' + ' Шаг-2: Загрузка словаря ' + '\x1b[0m')

dictionary_file_ = 'dictionary.json'
try:
    with open(dictionary_file_, 'r', encoding='utf-8') as read_file_:
        dictionary_ = json.load(read_file_)
    # print (dictionary)
    print('Количество проверок в словаре: ' + str(len(dictionary_)))
except:
    print('Ошибка чтения словаря: ' + dictionary_file_)
    exit()

# Тест-кейс проверки
# проверяем post-запросы
print('----------------------------------------------------------')
print('\x1b[1;32;40m' + ' Шаг-3: Проверка post-запросов с параметрами по умолчанию: ' + '\x1b[0m')

description_ = str(parameters_['post']['route_add']['description'])
urn_ = str(parameters_['post']['route_add']['urn'])
data_ = parameters_['post']['route_add']['data'].copy()

print('Описание: ' + description_)
print('URL: ' + protocol_ + '://' + host_ + ':' + port_ + urn_)
print('Параметры: ' + str(data_))

req_ = librequests.post(protocol_, host_, port_, urn_, login_, password_, timeout_, data_)
print('Код ответа сервера: ' + str(req_))

print('----------------------------------------------------------')
print('\x1b[1;32;40m' + ' Шаг-4: Проверка get-запросов и парсеров с параметрами по умолчанию: ' + '\x1b[0m')

# Парсер для route_config
description_ = str(parameters_['get']['route_config']['description'])
urn_ = str(parameters_['get']['route_config']['urn'])
print('Описание: ' + description_)

req_ = librequests.get(protocol_, host_, port_, urn_, login_, password_, timeout_)

if type(req_) == requests.models.Response:
    print('Код ответа сервера: ' + str(req_.status_code))
    route_, isInserted = parser_route_config.parsing(req_.text)
else:
    route_, isInserted = 'error', False

print('Результат парсинга страницы ' + protocol_ + '://' + host_ + ':' + port_ + urn_ + ' :')
table_data_ = [['Имя', 'Сеть', 'Маска сети', 'Промежуточный адрес', 'Устройство', 'Метка']]
for i_ in route_:
    table_data_.append([i_['name'], i_['net'], i_['mask'], i_['via'], i_['dev'], i_['fwmark']])
print(AsciiTable(table_data_).table)
print('')

# Парсер для netstatus
description_ = str(parameters_['get']['netstatus']['description'])
urn_ = str(parameters_['get']['netstatus']['urn'])
print('Описание: ' + description_)
req_ = librequests.get(protocol_, host_, port_, urn_, login_, password_, timeout_)

if type(req_) == requests.models.Response:
    print('Код ответа сервера: ' + str(req_.status_code))
    route_, isInserted = parser_netstatus_routes.parsing(req_.text)
else:
    route_, isInserted = 'error', False

print('Результат парсинга страницы ' + protocol_ + '://' + host_ + ':' + port_ + urn_ + ' :\n')
table_data_ = [['Сеть/Маска', 'Промежуточный адрес', 'Устройство', 'Метка']]
for i_ in route_:
    table_data_.append([i_['net_mask'], i_['via'], i_['dev'], i_['fwmark']])
print(AsciiTable(table_data_).table)
print('')

#удаление тестового маршрута
print('----------------------------------------------------------')
print('\x1b[1;32;40m' + ' Шаг-5: Подготовка к тестированию: ' + '\x1b[0m')

description_ = str(parameters_['post']['route_delete']['description'])
urn_ = str(parameters_['post']['route_delete']['urn'])
data_ = parameters_['post']['route_delete']['data'].copy()
req_ = librequests.post(protocol_, host_, port_, urn_, login_, password_, timeout_, data_)

print('Описание: ' + description_)
print('URL: ' + protocol_ + '://' + host_ + ':' + port_ + urn_)
print('Параметры: ' + str(data_))

req_ = librequests.post(protocol_, host_, port_, urn_, login_, password_, timeout_, data_)
print('Код ответа сервера: ' + str(req_))

print('----------------------------------------------------------')
print('\x1b[1;32;40m' + ' Шаг-6: Проверка по словарю: ' + '\x1b[0m')

bar_ = progressbar.ProgressBar(maxval=(len(dictionary_) + 1),
                               widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar_.start()
number_ = 0

table_data_ = [['Имя', 'Описание', 'Тип', 'Имя маршрута', 'Сеть', 'Маска', 'Промежуточный адрес', 'Устройство', 'Метка', 'Код post', 'Фактическое имя маршрута (route_config)', 'Фактическая сеть (route_config)', 'Фактическая маска (route_config)', 'Фактический промежуточный адрес (route_config)', 'Фактическое устройство (route_config)', 'Фактическая метка (route_config)', 'Фактическая сеть/маска (netstatus)', 'Фактический промежуточный адрес (netstatus)', 'Фактическое устройство (netstatus)', 'Фактическая метка (netstatus)', 'result']]

for i_ in dictionary_:
    urn_ = str(parameters_['post']['route_add']['urn'])
    data_ = parameters_['post']['route_add']['data'].copy()

    # Назначение переменных из словаря
    data_['NAME'] = i_['NAME']
    data_['NET'] = i_['NET']
    data_['MASK'] = i_['MASK']
    data_['VIA'] = i_['VIA']
    data_['DEV'] = i_['DEV']
    data_['FWMARK'] = i_['FWMARK']
    code_post_ = librequests.post(protocol_, host_, port_, urn_, login_, password_, timeout_, data_)

    #парсеры
    urn_ = str(parameters_['get']['netstatus']['urn'])
    req_ = librequests.get(protocol_, host_, port_, urn_, login_, password_, timeout_)

    if type(req_) == requests.models.Response:
        route_netstatus_, isInserted = parser_netstatus_routes.parsing(req_.text)
    else:
        route_netstatus_, isInserted = 'error', False

    urn_ = str(parameters_['get']['route_config']['urn'])
    req_ = librequests.get(protocol_, host_, port_, urn_, login_, password_, timeout_)

    if type(req_) == requests.models.Response:
        route_route_config_, isInserted = parser_route_config.parsing(req_.text)
    else:
        route_route_config_, isInserted = 'error', False

    # Сравнение результатов:
    if route_route_config_[0]['name'] == i_['resultNAME'] and route_route_config_[0]['net'] == i_['resultNET'] and route_route_config_[0]['mask'] == i_['resultMASK'] and route_route_config_[0]['via'] == i_['resultVIA'] and route_route_config_[0]['dev'] == i_['resultDEV'] and route_route_config_[0]['fwmark'] == i_['resultFWMARK'] and code_post_ != 200:
        diff_status_ = '\x1b[1;32;40m' + ' ok ' + '\x1b[0m'
    else:
        diff_status_ = '\x1b[1;31;40m' + ' error ' + '\x1b[0m'

    table_data_.append([i_['name'], i_['description'], i_['type'], i_['NAME'], i_['NET'], i_['MASK'], i_['VIA'], i_['DEV'], i_['FWMARK'], code_post_, route_route_config_[0]['name'], route_route_config_[0]['net'], route_route_config_[0]['mask'], route_route_config_[0]['via'], route_route_config_[0]['dev'], route_route_config_[0]['fwmark'], route_netstatus_[0]['net_mask'], route_netstatus_[0]['via'],route_netstatus_[0]['dev'], route_netstatus_[0]['fwmark'], diff_status_])

    #удаление маршрута, если он сохранился
    if isInserted == True:
        urn_ = str(parameters_['post']['route_delete']['urn'])
        data_ = parameters_['post']['route_delete']['data'].copy()
        data_['ROUTE_NAME'] = i_['NAME']
        req_ = librequests.post(protocol_, host_, port_, urn_, login_, password_, timeout_, data_)

    # Прогресс бар
    bar_.update(number_ + 1)
    number_ += 1
bar_.finish()

print('----------------------------------------------------------')
print('\x1b[1;32;40m' + ' Шаг-7: Вывод результата: ' + '\x1b[0m')
print(AsciiTable(table_data_).table)

outputfile = "output.log"
with open(outputfile, "w") as file:
    file.write(AsciiTable(table_data_).table)

print('Файл ' + outputfile + ' записан')
print('\x1b[1;32;40m' + datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") + ' скрипт завершен' + '\x1b[0m')