
#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
NooLite PR1132 command line interface
"""

import os
import json
import logging
import argparse

import yaml

from noolite_api import NooLiteApi
import paho.mqtt.client as mqtt


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


# Logging config
logger = logging.getLogger()
formatter = logging.Formatter(
    '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def get_args():
    """Получение аргументов запуска

    :return:  словарь вида {название: значение} для переданных аргументов.
    :rtype: dict
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-sns', type=int, help='Получить данные с указанного датчика')
    parser.add_argument('-hsns', type=int, help='Получить данные с указанного датчика в текстовом формате')
    parser.add_argument('-ch',  type=int, help='Адрес канала')
    parser.add_argument('-cmd', type=int, help='Команда')
    parser.add_argument('-br',  type=int, help='Абсолютная яркость')
    parser.add_argument('-fmt', type=int, help='Формат')
    parser.add_argument('-d0',  type=int, help='Байт данных 0')
    parser.add_argument('-d1',  type=int, help='Байт данных 1')
    parser.add_argument('-d2',  type=int, help='Байт данных 2')
    parser.add_argument('-d3',  type=int, help='Байт данных 3')
    return {key: value for key, value in vars(parser.parse_args()).items()
            if value is not None}

if __name__ == '__main__':
    # Получаем конфиг из файла
    config = yaml.full_load(open(os.path.join(SCRIPT_PATH, 'conf_cli.yaml')))

    # Создаем объект для работы с NooLite
    noolite_api = NooLiteApi(
        config['noolite']['login'],
        config['noolite']['password'],
        config['noolite']['api_url']
    )

    # Получаем аргументы запуска
    args = get_args()
    logger.debug('Args: {}'.format(args))

    # Если есть аргумент sns, то возвращаем информацию с датчиков
if 'sns' in args:
           sens_list = noolite_api.get_sens_data()
           send_data = sens_list[args['sns']]
           print(json.dumps({
            'temperature': send_data.temperature,
            'humidity': send_data.humidity,
            'state': send_data.state,
        }))
#else:
 #       logger.info('Send command to noolite: {}'.format(args))
  #      print(noolite_api.send_command_to_channel(args))

if 'hsns' in args:
        sens_list = noolite_api.get_sens_data()
        send_data = sens_list[args['hsns']]
        jsonStr = json.dumps({
            'temperature': send_data.temperature,
            'humidity': send_data.humidity,
                        'state': send_data.state,
        })
        to_python = json.loads(jsonStr)
        string = str(to_python['temperature'])
        msg1 = "mqtt/noolite/sens"
        msg2 = str(args['hsns'])
#       client = mqtt.Client("Server")
#       client.connect("192.168.1.200", 1883, 60)
#       client.publish(msg1+msg2, send_data.temperature)
        print(send_data.temperature)
