#/***********************************************************************************************************
# * Ultrasonic+Magnet Parking Lots Detector DO201 Codec for nb-iot version.
# * Version 1.0  Date 2024-02-22 
# * 
# * 
# ***********************************************************************************************************/
import Logger
import json
from utility import utility


class DO201(object):
    # Func: parse data to attr
    # Param: req_data: input data string in upper format
    #        attr_result: output attr
    #       token_id: token for thingsboard, imei
    # "8000310226270F00000165010DFC31F8681D13000070C4659CF8060001186973806917580581" heart beat/alarm
    # "" Param
    def parse_data_DO201(req_data):
        try:
            data_type = req_data[6:8]
            data_len = int(req_data[8:10], 16)
            global attr_result
            global token_id

            if data_len == len(req_data) / 2:
                if (data_type == "01" or data_type == "02") and (data_len ==38 ):
                    token_id = req_data[59:74]
                    data_height = int(req_data[10:14], 16)
                    data_park_status = int(req_data[14:15], 16)
                    data_ultra_status = int(req_data[15:16], 16)
                    data_magnet_status = int(req_data[16:17], 16)
                    data_battery_status = int(req_data[17:18], 16)                    
                    data_volt = int(req_data[18:22], 16) / 100
                    data_rsrp_origin = req_data[38:46]
                    data_rsrp = int(utility.IEEE754_Hex_To_Float(data_rsrp_origin))                    
                    data_timestamp = int(req_data[46:54], 16)
                    data_magnet_x = int(req_data[22:26], 16)
                    if data_magnet_x >= 32768:
                        data_magnet_x = data_magnet_x - 65536

                    data_magnet_y = int(req_data[26:30], 16)
                    if data_magnet_y >= 32768:
                        data_magnet_y = data_magnet_y - 65536

                    data_magnet_z = int(req_data[30:34], 16)
                    if data_magnet_z >= 32768:
                        data_magnet_z = data_magnet_z - 65536
                    data_temperature = int(req_data[34:36], 16)
                    if data_temperature >= 128:
                        data_temperature = data_temperature - 256
                    data_humidity = int(req_data[36:38], 16)
                    data_frame_counter = int(req_data[54:58], 16)
                    # print("rsrp is "+str(data_rsrp))
                    attribute = {
                        "volt": data_volt,
                        "alarmBattery": data_battery_status,
                        "level": data_height,
                        "alarmPark": data_park_status,
                        "alarmLevel": data_ultra_status,
                        "alarmMagnet": data_magnet_status,
                        "xMagnet": data_magnet_x,
                        "yMagnet": data_magnet_y,
                        "zMagnet": data_magnet_z,
                        "timestamp": data_timestamp,  
                        "temperature": data_temperature,  
                        "humidity": data_humidity,                     
                        "rsrp": data_rsrp,                        
                        "frame_counter": data_frame_counter,
                    }
                    attr_result = json.dumps(attribute)
                else:
                    if (data_type == "03"):
                        token_id = req_data[data_len*2-17:data_len*2-2]
                        data_version = str(int(req_data[10:12], 16))+"."+str(int(req_data[12:14], 16))
                        data_upload_interval = int(req_data[14:16], 16)
                        data_cyclic_interval = int(req_data[16:18], 16)
                        data_height_threshold = int(req_data[18:20], 16)
                        data_magnet_threshold = int(req_data[20:24], 16)  
                        data_battery_threshold = int(req_data[24:26], 16)                 
                        
                        # print("rsrp is "+str(data_rsrp))
                        attribute = {
                            "firmware": data_version,
                            "uploadInterval": data_upload_interval,
                            "detectInterval": data_cyclic_interval,
                            "levelThreshold": data_height_threshold,
                            "magnetThreshold": data_magnet_threshold,
                            "batteryThreshold": data_battery_threshold,                        
                        }
                        attr_result = json.dumps(attribute)                    
                    else:
                        pass
            else:
                pass

            # str_org=str(byte_org)

        except Exception as e:
            print(e)
            # log.logger.exception(e)
        finally:
            return attr_result, token_id


if __name__ == "__main__":
    try:
        attr_result = ""
        #incomingData = "8000310226270F11100165010DFC31F868FD13000070C4659CF8060001186973806917580581"
        incomingData = "8000310327010218053C003C143132302E39322E38392E3132323B23823B186973806917580581"
        attr_result = DO201.parse_data_DO201(incomingData)        
    except Exception as e:
        print(e)
        