import Logger
import json
import utility


class DO200(object):
    # Func: parse data to attr
    # Param: req_data: input data string in upper format
    #        attr_result: output attr
    #       token_id: token for thingsboard, imei
    # "800002012B0686000000016C004050C40000404301EB5DF347C60015FFE700230000186950504949859381" heart beat/alarm
    # "" Param
    def parse_data_DO200(req_data):
        try:
            data_type = req_data[6:8]
            data_len = int(req_data[8:10], 16)
            global attr_result
            global token_id

            if data_len == len(req_data) / 2:
                if (data_type == "01" or data_type == "02") and (data_len == 43):
                    token_id = req_data[69:84]
                    data_height = int(req_data[10:14], 16)
                    data_park_status = int(req_data[14:15], 16)
                    data_ultra_status = int(req_data[15:16], 16)
                    data_magnet_status = int(req_data[16:17], 16)
                    data_battery_status = int(req_data[17:18], 16)
                    data_signal = int(req_data[18:20], 16)
                    data_volt = int(req_data[20:24], 16) / 100
                    data_rsrp_origin = req_data[24:32]
                    data_rsrp = int(utility.LEEE754_Hex_To_Float(data_rsrp_origin))
                    data_snr_origin = req_data[32:40]
                    data_snr = int(utility.LEEE754_Hex_To_Float(data_snr_origin))
                    data_timestamp = int(req_data[44:52], 16)
                    data_magnet_x = int(req_data[52:56], 16)
                    if data_magnet_x >= 32768:
                        data_magnet_x = data_magnet_x - 65536

                    data_magnet_y = int(req_data[56:60], 16)
                    if data_magnet_y >= 32768:
                        data_magnet_y = data_magnet_y - 65536

                    data_magnet_z = int(req_data[60:64], 16)
                    if data_magnet_z >= 32768:
                        data_magnet_z = data_magnet_z - 65536

                    data_frame_counter = int(req_data[64:68], 16)
                    # print("rsrp is "+str(data_rsrp))
                    attribute = {
                        "volt": data_volt,
                        "battery_status": data_battery_status,
                        "height": data_height,
                        "park_status": data_park_status,
                        "ultra_status": data_ultra_status,
                        "magnet_status": data_magnet_status,
                        "magnet_x": data_magnet_x,
                        "magnet_y": data_magnet_y,
                        "magnet_z": data_magnet_z,
                        # "timestamp": data_timestamp,
                        "singal": data_signal,
                        "rsrp": data_rsrp,
                        "snr": data_snr,
                        "frame_counter": data_frame_counter,
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
