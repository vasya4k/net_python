#!/usr/bin/python3
import logging
import sys
import xmltodict
import json

from ncclient import manager

class router(object):
    pass

def connect(host, port, user, key):
    conn = manager.connect(host=host,
                           port=port,
                           username=user,                           
                           key_filename=key,
                           timeout=60,
                           device_params={'name': 'junos'},
                           hostkey_verify=False)


    # logging.info('show system users')
    # logging.info('*' * 30)
    # result = conn.command(command='show system users', format='text')
    # logging.info(result)

    # logging.info('show version')
    # logging.info('*' * 30)
    # result = conn.command('show version', format='text')
    # logging.info(result.xpath('output')[0].text)

    # logging.info('bgp summary')
    # logging.info('*' * 30)
    result = conn.command('show bgp summary')
    # print('AAAAAAAAA')
    # logging.info(result)
    # print(result.__dir__())
    xml_dict = xmltodict.parse(result.data_xml)
    
    # print(json.dumps(xml_dict, indent=4, sort_keys=True))
    try:
        print(xml_dict['rpc-reply']['bgp-information']['peer-count'])
    except Exception as e:
        print(e)        
    # logging.info(xml_dict['rpc-reply']['bgp-information']['peer-count'])

if __name__ == '__main__':
    # LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

    connect('10.0.0.14', '830', 'admin', '~/.ssh/id_rsa_srx')