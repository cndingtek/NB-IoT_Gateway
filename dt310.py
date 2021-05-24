# Gateway for CNDingtek DT310 temperature/humidity sensor NB-IoT version
# change log Nov 16, 2020. change the created threading not close automatically.
# coding:utf-8

import utility
import json


class DT310(object):
    # Func: parse data to attr
    # Param: req_data: input data string in upper format
    #        attr_result: output attr
    #       token_id: token for thingsboard, imei
    def parse_data(req_data):
        try:
            data_type = req_data[6:8]
            data_len = int(req_data[8:10], 16)
            global attr_result
            global token_id
            if (data_type == "01" or data_type == "02") and (data_len == 30):
                token_id = req_data[43:58]
                data_volt = int(req_data[10:14], 16) / 100
                data_battery_alarm = int(req_data[14:16])
                data_temperature_sign = int(req_data[16:18])
                data_temperature = int(req_data[18:22]) / 100
                if data_temperature_sign == 1:
                    data_temperature = -data_temperature
                data_humidity = int(req_data[22:26]) / 100
                data_high_temperature_alarm = int(req_data[26:27])
                data_low_temperature_alarm = int(req_data[27:28])
                data_high_humidity_alarm = int(req_data[28:29])
                data_low_humidity_alarm = int(req_data[29:30])
                data_frame_counter = int(req_data[38:42], 16)
                # data_rsrp=
                attribute = {
                    "volt": data_volt,
                    "temperature": data_temperature,
                    "humidity": data_humidity,
                    "high temperature alarm": data_high_temperature_alarm,
                    "low temperature alarm": data_low_temperature_alarm,
                    "high humidity alarm": data_high_humidity_alarm,
                    "low humidity alarm": data_low_humidity_alarm,
                    "frame_counter": data_frame_counter,
                }
            elif data_len == len(req_data) / 2:
                token_id = req_data[31:46]
                data_version = int(req_data[10:12], 16) + int(req_data[12:14], 16) / 100
                data_upload_interval = int(req_data[14:16], 16)
                data_detect_interval = int(req_data[16:18], 16)
                data_high_temp_threshold = int(req_data[18:22], 16)
                data_low_temp_threshold_sign = int(req_data[22:24], 16)
                data_low_temp_threshold = int(req_data[24:26], 16)
                if data_low_temp_threshold_sign == 1:
                    data_low_temp_threshold = -data_low_temp_threshold
                data_high_humidity_threshold = int(req_data[26:28], 16)
                data_low_humidity_threshold = int(req_data[28:30], 16)
                data_work_mode = int(req_data[46:48], 16)
                data_server_mode = int(req_data[48:50], 16)
                index_server_one = req_data.find("3B")
                str_server1 = req_data[50:index_server_one]
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
                    "detect interval": data_detect_interval,
                    "upload interval": data_upload_interval,
                    "high temperature threshold": data_high_temp_threshold,
                    "low temperature threshold": data_low_temp_threshold,
                    "high humidity threshold": data_high_humidity_threshold,
                    "low humidity threshold": data_low_humidity_threshold,
                    "work mode": data_work_mode,
                    "server mode": data_server_mode,
                    "server IP1": str_asc_server1,
                    "server Port1": port1_number,
                    "server IP2": str_asc_server2,
                    "server Port2": port2_number,
                    "frame_counter": 2,
                }

            attr_result = json.dumps(attribute)

            # str_org=str(byte_org)

        except Exception as e:
            print(e)
        finally:
            return attr_result, token_id
