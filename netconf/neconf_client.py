#!/usr/bin/python3
import logging
import sys
import xmltodict
import json
from typing import Any, List, TypeVar, Type, cast, Callable

from ncclient import manager


    # print(result.__dir__())


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x

# class route_engine:
#     last_reboot_reason: str    
#     mastership_priority: str
#     mastership_state: str    
#     memory_dram_size: str
#     memory_installed_size: str
#     model: str
#     slot: int
#     start_time: int
#     status: str
#     up_time: int
    
#     def __init__(self, xml_dict):
#         # xml_dict['rpc-reply']['route-engine-information']['route-engine']['last-reboot-reason']
#         self.last_reboot_reason = from_str(xml_dict.get("last-reboot-reason"))
#         self.mastership_priority = from_str(xml_dict.get("mastership-priority"))
#         self.mastership_state = from_str(xml_dict.get("mastership-state"))
#         self.memory_dram_size = from_str(xml_dict.get("memory-dram-size"))
#         self.memory_installed_size = from_str(xml_dict.get("memory-installed-size"))
#         self.model = from_str(xml_dict.get("model"))
#         self.slot = from_str(from_str(xml_dict.get("slot")))       
#         self.status = from_str(xml_dict.get("status"))
#         # self.up_time 
#         # self.start_time 

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
    
    def add_re_details(self, xml_dict):
        self.last_reboot_reason = from_str(xml_dict.get("last-reboot-reason"))
        self.mastership_priority = from_str(xml_dict.get("mastership-priority"))
        self.mastership_state = from_str(xml_dict.get("mastership-state"))
        self.memory_dram_size = from_str(xml_dict.get("memory-dram-size"))
        self.memory_installed_size = from_str(xml_dict.get("memory-installed-size"))
        self.model = from_str(xml_dict.get("model"))
        self.slot = from_str(from_str(xml_dict.get("slot")))       
        self.status = from_str(xml_dict.get("status"))
        # self.route_engines.append(re)

        

def connect(host, port, user, key):
    conn = manager.connect(host=host,
                           port=port,
                           username=user,                           
                           key_filename=key,
                           timeout=60,
                           device_params={'name': 'junos'},
                           hostkey_verify=False)

    result = conn.command('show chassis routing-engine')

    xml_dict = xmltodict.parse(result.data_xml)
    
    print(json.dumps(xml_dict, indent=4, sort_keys=True))
    
    r = router()    
    r.add_re_details(xml_dict['rpc-reply']['route-engine-information']['route-engine'])

    print(json.dumps(r.__dict__, indent=4, sort_keys=True))
    
    result = conn.command('show chassis hardware')

    xml_dict = xmltodict.parse(result.data_xml)
    
    print(json.dumps(xml_dict, indent=4, sort_keys=True))
    
    # try:
    #     print(xml_dict['rpc-reply']['route-engine-information']['route-engine'])
    # except Exception as e:
    #     print(e)        
    # logging.info(xml_dict['rpc-reply']['bgp-information']['peer-count'])

if __name__ == '__main__':
    # LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)

    connect('10.0.0.14', '830', 'admin', '~/.ssh/id_rsa_srx')