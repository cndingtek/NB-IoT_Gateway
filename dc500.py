# Gateway for CNDingtek DC500 people counter NB-IoT version
# change log Nov 20, 2020. change the created threading not close automatically.
# coding:utf-8

import utility
import json


class DC500(object):

    # Func: parse data to attr
    # Param: req_data: input data string in upper format
    #        attr_result: output attr
    #       token_id: token for thingsboard, imei
    # "800001021800000000016800C079C418658230475942465EF2C35100018" heart beat
    # "80000103350100071900031D0865823047594246003131342E3231352E3232312E39383B270F3B3030302E3030302E3030302E3030303B270F3B81" Param
    def parse_data(req_data):
        try:
            data_type = req_data[6:8]
            data_len = int(req_data[8:10], 16)
            global attr_result
            global token_id
            if (
                data_type == "01"
                or data_type == "02"
                or data_type == "04"
                or data_type == "05"
            ) and (data_len == 24):
                token_id = req_data[31:46]
                data_people_counter = int(req_data[10:14], 16)
                data_people_counter_alarm = int(req_data[14:16])
                data_battery_alarm = int(req_data[16:18])
                data_volt = int(req_data[18:22], 16) / 100
                data_rsrp_origin = req_data[22:30]
                data_rsrp = int(utility.LEEE754_Hex_To_Float(data_rsrp_origin))
                data_timestamp = int(req_data[46:54], 16)
                data_frame_counter = int(req_data[54:58], 16)
                print("rsrp is " + str(data_rsrp))
                attribute = {
                    "volt": data_volt,
                    "people_counter": data_people_counter,
                    "people_counter_alarm": data_people_counter_alarm,
                    "battery alarm": data_battery_alarm,
                    "rsrp": data_rsrp,
                    "time_stamp": data_timestamp,
                    "frame_counter": data_frame_counter,
                }
            else:
                token_id = req_data[25:40]
                data_version = int(req_data[10:12], 16) + int(req_data[12:14], 16) / 100
                data_heartbeat_interval = int(req_data[14:16], 16)
                data_periodic_interval = int(req_data[16:18], 16)
                data_people_alarm_threshold = int(req_data[18:22], 16)
                data_battery_alarm_threshold = int(req_data[22:24], 16)

                data_server_mode = int(req_data[40:42], 16)
                index_server_one = req_data.find("3B")
                str_server1 = req_data[42:index_server_one]
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
                    "version": data_version,
                    "heartbeat interval": data_heartbeat_interval,
                    "periodic interval": data_periodic_interval,
                    "people alarm threshold": data_people_alarm_threshold,
                    "battery alarm threshold": data_battery_alarm_threshold,
                    "server mode": data_server_mode,
                    "server IP1": str_asc_server1,
                    "server Port1": port1_number,
                    "server IP2": str_asc_server2,
                    "server Port2": port2_number,
                }

            attr_result = json.dumps(attribute)

        except Exception as e:
            print(e)
        finally:
            return attr_result, token_id
