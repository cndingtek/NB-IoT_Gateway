import json
from utility import utility


class DF200(object):
    # Func: parse data to attr
    # Param: req_data: input data string in upper format
    #        attr_result: output attr
    #       token_id: token for thingsboard, imei
    # "8000200119015D00CC0001000000000001186105004544355681" heart beat/alarm
    # "" Param
    def parse_data_DF200(req_data):
        try:
            data_type = req_data[6:8]
            data_len = int(req_data[8:10], 16)
            global attr_result
            global token_id
            if data_len == len(req_data) / 2:
                if (data_type == "01" or data_type == "02") and (data_len == 26):
                    token_id = req_data[35:50]

                    data_volt = int(req_data[10:14], 16) / 100
                    data_volt_status = int(req_data[14:16], 16)
                    data_temperature = int(req_data[16:18], 16)
                    data_level = int(req_data[18:20], 16)
                    data_level_status = int(req_data[20:22], 16)
                    data_rsrp_origin = req_data[22:30]
                    data_rsrp = int(
                        utility.IEEE754_Hex_To_Float(data_rsrp_origin))
                    # data_timestamp=int(req_data[46:54],16)
                    data_frame_counter = int(req_data[30:34], 16)
                    # print("rsrp is "+str(data_rsrp))
                    attribute = {
                        "volt": data_volt,
                        "volt status": data_volt_status,
                        "temperature": data_temperature,
                        "level": data_level,
                        "level status": data_level_status,
                        "rsrp": data_rsrp,
                        "frame_counter": data_frame_counter,
                    }
                else:
                    token_id = req_data[23:38]
                    data_version = (
                        int(req_data[10:12], 16) +
                        int(req_data[12:14], 16) / 100
                    )
                    data_upload_interval = int(req_data[14:16], 16)
                    data_detect_interval = int(req_data[16:18], 16)

                    data_battery_alarm_threshold = int(req_data[18:20], 16)
                    data_level_alarm_threshold = int(req_data[20:22], 16)
                    data_server_mode = int(req_data[38:40], 16)
                    index_server_one = req_data.find("3B")
                    str_server1 = req_data[40:index_server_one]
                    str_asc_server1 = utility.hex_to_ascii(str_server1)

                    new_req_data = req_data[index_server_one + 2: -1]
                    index_server_two = new_req_data.find("3B")
                    str_port1 = new_req_data[0:index_server_two]
                    port1_number = int(str_port1, 16)

                    new_req_data = new_req_data[index_server_two + 2: -1]
                    index_server_three = new_req_data.find("3B")
                    str_server2 = new_req_data[0:index_server_three]
                    str_asc_server2 = utility.hex_to_ascii(str_server2)

                    new_req_data = new_req_data[index_server_three + 2: -1]
                    index_server_four = new_req_data.find("3B")
                    str_port2 = new_req_data[0:index_server_four]
                    port2_number = int(str_port2, 16)

                    attribute = {
                        "version": data_version,
                        "upload interval": data_upload_interval,
                        "detect interval": data_detect_interval,
                        "battery alarm threshold": data_battery_alarm_threshold,
                        "level alarm threshold": data_level_alarm_threshold,
                        "server mode": data_server_mode,
                        "server IP1": str_asc_server1,
                        "server Port1": port1_number,
                        "server IP2": str_asc_server2,
                        "server Port2": port2_number,
                    }

                attr_result = json.dumps(attribute)
            else:
                attr_result = json.dumps("")
                token_id = ""

            # str_org=str(byte_org)

        except Exception as e:
            print(e)
            # log.logger.exception(e)
        finally:
            return attr_result, token_id
