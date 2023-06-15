# ToDo: will add DF556 nb-iot support in near future.

import utility
import json

class DF556(object):
    # Func: parse data to attr DF556 TCP
    # Param: req_data: input data string in upper format
    #        attr_result: output attr
    #       token_id: token for thingsboard, imei
    # "80 00 16 02 1E 0265 00 00 0000 0000 0168 008045C4 1865385060029872 0001 81“ heart beat/alarm without gps
    # "80 00 16 03 20 0405 003C 0A 1E 4B 1E 14 1460081912008446 00 1865385060029872 81" event packet with gps
    # "" Param
    def parse_data_DF556(req_data):
        try:
            data_type = req_data[6:8]
            data_len = int(req_data[8:10], 16)
            global attr_result
            global token_id
            if (data_len == len(req_data) / 2):
                if (data_type == "01" or data_type == "02"):
                    if (data_len == 30):
                        token_id = req_data[43:58]
                        data_height = int(req_data[10:14], 16)
                        data_gps_enabled = int(req_data[14:16], 16)
                        data_empty_alarm = int(req_data[22:23], 16)
                        data_battery_alarm = int(req_data[25:26], 16)
                        data_volt = int(req_data[26:30], 16) / 100
                        data_rsrp_origin = req_data[30:38]
                        data_rsrp = int(utility.utility.IEEE754_Hex_To_Float(data_rsrp_origin))
                        data_frame_counter = int(req_data[54:58], 16)
                        # print("rsrp is "+str(data_rsrp))
                        attribute = {
                            "height": data_height,
                            "gps_enabled": data_gps_enabled,
                            "empty_alarm": data_empty_alarm,
                            "battery_alarm": data_battery_alarm,
                            "volt": data_volt,
                            "rsrp": data_rsrp,
                            "frame_counter": data_frame_counter
                        }
                    else:
                        if(data_len == 38):
                            token_id = req_data[59:74]
                            data_height = int(req_data[10:14], 16)
                            data_gps_enabled = int(req_data[14:16], 16)
                            data_longitude_origin = req_data[16:24]
                            data_longitude = utility.utility.IEEE754_Hex_To_Float(data_longitude_origin)
                            data_longitude = ("%.6f" % data_longitude)
                            data_latitude_origin = req_data[24:32]
                            data_latitude = utility.utility.IEEE754_Hex_To_Float(data_latitude_origin)
                            data_latitude = ("%.6f" % data_latitude)
                            data_empty_alarm = int(req_data[38:39], 16)
                            data_battery_alarm = int(req_data[41:42], 16)
                            data_volt = int(req_data[42:46], 16) / 100
                            data_rsrp_origin = req_data[46:54]
                            data_rsrp = int(utility.utility.IEEE754_Hex_To_Float(data_rsrp_origin))
                            data_frame_counter = int(req_data[70:74], 16)
                            # print("rsrp is "+str(data_rsrp))
                            attribute = {
                                "height": data_height,
                                "gps_enabled": data_gps_enabled,
                                "longitude": data_longitude,
                                "latitude": data_latitude,
                                "empty_alarm": data_empty_alarm,
                                "battery_alarm": data_battery_alarm,
                                "volt": data_volt,
                                "rsrp": data_rsrp,
                                "frame_counter": data_frame_counter
                            }
                        else:
                            attribute = {}
                else:
                    if(data_len == 32):
                        token_id = req_data[data_len*2-17:-2]
                        data_firmware_version=str(int(req_data[10:12],16))+"."+str(int(req_data[12:14],16))
                        data_upload_interval = int(req_data[14:18],16)
                        data_detect_interval = int(req_data[18:20], 16)
                        data_height_threshold = int(req_data[20:22], 16)
                        data_battery_threshold = int(req_data[26:28], 16)
                        data_imsi = req_data[29:44]
                        data_work_mode = int(req_data[44:46], 16)
                        attribute = {
                            "firmware_version": data_firmware_version,
                            "upload_interval": data_upload_interval,
                            "detect_interval": data_detect_interval,
                            "height_threshold": data_height_threshold,
                            "battery_threshold": data_battery_threshold,
                            "imsi": data_imsi,
                            "work_mode": data_work_mode,
                        }
                    else:
                        attribute = {}
                attr_result = json.dumps(attribute)
            else:
                attr_result = json.dumps("")
                token_id = ""
            #time.sleep(1)
        except Exception as e:
            print(e)
            #log.logger.exception(e)
        finally:
            return attr_result, token_id