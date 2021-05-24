# Gateway for CNDingtek DH100 door monitoring sensor NB-IoT version
# change log Nov 26, 2020. change the created threading not close automatically.
# coding:utf-8

import utility
import json


class DH100(object):
    # Func: parse data to attr
    # Param: req_data: input data string in upper format
    #        attr_result: output attr
    #       token_id: token for thingsboard, imei
    # "800001021E0000001400000010012A004077C40000186950504949859381" heart beat/alarm
    # "800001033D0000180000001E1460111172762130000000003131342E3231352E3232312E39383B270F3B3131372E36302E3135372E3133373B16333B81" Param
    def parse_data(req_data):
        try:
            data_type = req_data[6:8]
            data_len = int(req_data[8:10], 16)
            global attr_result
            global token_id
            if (data_type == "01" or data_type == "02") and (data_len == 30):
                token_id = req_data[43:58]
                data_temperature = int(req_data[16:18], 16)
                data_monitor_status = int(req_data[23:24])
                data_door_status = int(req_data[24:25])
                data_battery_status = int(req_data[25:26])
                data_volt = int(req_data[26:30], 16) / 100
                data_rsrp_origin = req_data[30:38]
                data_rsrp = int(utility.LEEE754_Hex_To_Float(data_rsrp_origin))
                # data_timestamp=int(req_data[46:54],16)
                data_frame_counter = int(req_data[38:42], 16)
                # print("rsrp is "+str(data_rsrp))
                attribute = {
                    "volt": data_volt,
                    "battery status": data_battery_status,
                    "temperature": data_temperature,
                    "monitor status": data_monitor_status,
                    "door status": data_door_status,
                    "rsrp": data_rsrp,
                    "frame_counter": data_frame_counter,
                }
            else:
                token_id = req_data[25:40]
                # data_version=int(req_data[10:12],16)+int(req_data[12:14],16)/100
                data_heartbeat_interval = int(req_data[14:16], 16)
                # data_periodic_interval = int(req_data[16:18], 16)
                data_battery_alarm_threshold = int(req_data[22:24], 16)
                data_monitor_status = int(req_data[40:42], 16)
                data_server_mode = int(req_data[46:48], 16)
                index_server_one = req_data.find("3B")
                str_server1 = req_data[48:index_server_one]
                str_asc_server1 = utility.hex_to_ascii(str_server1)

                new_req_data = req_data[index_server_one + 2 : -1]
                index_server_two = new_req_data.find("3B")
                str_port1 = new_req_data[0:index_server_two]
                port1_number = int(str_port1, 16)

                new_req_data = new_req_data[index_server_two + 2 : -1]
                index_server_three = new_req_data.find("3B")
                str_server2 = new_req_data[0:index_server_three]
                str_asc_server2 = utility.hex_to_ascii(str_server2)

                new_req_data = new_req_data[index_server_three + 2 : -1]
                index_server_four = new_req_data.find("3B")
                str_port2 = new_req_data[0:index_server_four]
                port2_number = int(str_port2, 16)

                attribute = {
                    "heartbeat interval": data_heartbeat_interval,
                    "monitor status": data_monitor_status,
                    "battery alarm threshold": data_battery_alarm_threshold,
                    "server mode": data_server_mode,
                    "server IP1": str_asc_server1,
                    "server Port1": port1_number,
                    "server IP2": str_asc_server2,
                    "server Port2": port2_number,
                }

            attr_result = json.dumps(attribute)

            # str_org=str(byte_org)

        except Exception as e:
            print(e)
        finally:
            return attr_result, token_id
