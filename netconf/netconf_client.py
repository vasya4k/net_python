#!/usr/local/bin/python3
import logging
import sys
import xmltodict
import json
import psutil
import os
import threading
import concurrent.futures
from typing import Any, List, TypeVar, Type, cast, Callable

from ncclient import manager


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


class router:
    # route_engines: List[route_engine]
    last_reboot_reason: str
    mastership_priority: str
    mastership_state: str
    memory_dram_size: str
    memory_installed_size: str
    model: str
    slot: int
    start_time: int
    status: str
    up_time: int
    softwware_version: str

    def add_re_details(self, xml_dict):
        self.last_reboot_reason = from_str(xml_dict.get("last-reboot-reason"))
        self.mastership_priority = from_str(
            xml_dict.get("mastership-priority"))
        self.mastership_state = from_str(xml_dict.get("mastership-state"))
        self.memory_dram_size = from_str(xml_dict.get("memory-dram-size"))
        self.memory_installed_size = from_str(
            xml_dict.get("memory-installed-size"))
        self.model = from_str(xml_dict.get("model"))
        self.slot = from_str(from_str(xml_dict.get("slot")))
        self.status = from_str(xml_dict.get("status"))
        # self.route_engines.append(re)
        # result = conn.command('show chassis routing-engine')
        # xml_dict = xmltodict.parse(result.data_xml)
        # print(json.dumps(xml_dict, indent=4, sort_keys=True))
        # r.add_re_details(xml_dict['rpc-reply']['route-engine-information']['route-engine'])


def read_hosts():
    hosts = []
    try:
        file = open('hosts.txt', "r")
    except Exception as e:
        print('fatal err opening file:', e)
        raise SystemExit
    for line in file:
        hosts.append(line.rstrip('\n\r'))
    return hosts
# print(json.dumps(xml_dict, indent=4, sort_keys=True))
    # print(json.dumps(r.__dict__, indent=4, sort_keys=True))


def connect(host):
    # print('running for host:',host)
    try:
        conn = manager.connect(host=host,
                               port=830,
                               username=sys.argv[1],
                               password=sys.argv[2],
                               key_filename=None,
                               ssh_config='~/.ssh/config',
                               timeout=60,
                               device_params={'name': 'junos'},
                               hostkey_verify=False)

    except Exception as e:
        raise Exception(host, str(e)) from None

    try:
        data = conn.command('show version')
    except Exception as e:
        raise Exception(host, str(e)) from None

    xml_dict = xmltodict.parse(data.data_xml)
    # print(host,xml_dict['rpc-reply']['software-information']['junos-version'])
    return (host, xml_dict['rpc-reply']['software-information']['junos-version'])


if __name__ == '__main__':
    # logging.info(xml_dict['rpc-reply']['bgp-information']['peer-count'])
    # LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
    print('PID', os.getpid())
    process = psutil.Process(os.getpid())

    futures_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        for host in read_hosts():
            f = executor.submit(connect, host)
            futures_list.append(f)

    for future in futures_list:
        try:
            print(future.result())
        except Exception as e:
            print(e)

    print(process.memory_info()[0])

    # logging.info(xml_dict['rpc-reply']['bgp-information']['peer-count'])
