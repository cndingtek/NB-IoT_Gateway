# ToDo: will add DF703 nb-iot support in near future.

from utility import utility
import json

class DF703(object):
    # Func: parse data to attr DF703 TCP
    # Param: req_data: input data string in upper format
    #        attr_result: output attr
    #       token_id: token for thingsboard, imei
    # "800001021E0649001B00000101015F008054440000186882104303887681“ heart beat/alarm without gps
    # "8000010126064901CD03E942EF2720421B00000101015F008054440000186882104303887681" event packet with gps
    # "" Param
    def parse_data_DF703(req_data):
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
                        data_temperature = int(req_data[16:18], 16)
                        data_angle = int(req_data[20:22], 16) if (int(req_data[18:20], 16) == 0) else (
                                0 - int(req_data[20:22], 16))
                        data_full_alarm = int(req_data[22:23], 16)
                        data_fire_alarm = int(req_data[23:24], 16)
                        data_tilt_alarm = int(req_data[24:25], 16)
                        data_battery_alarm = int(req_data[25:26], 16)
                        data_volt = int(req_data[26:30], 16) / 100
                        data_rsrp_origin = req_data[30:38]
                        data_rsrp = int(utility.IEEE754_Hex_To_Float(data_rsrp_origin))
                        data_frame_counter = int(req_data[38:42], 16)
                        # print("rsrp is "+str(data_rsrp))
                        attribute = {
                            "height": data_height,
                            "temperature": data_temperature,
                            "full_alarm": data_full_alarm,
                            "fire_alarm": data_fire_alarm,
                            "tilt_alarm": data_tilt_alarm,
                            "battery_alarm": data_battery_alarm,
                            "volt": data_volt,
                            "angle": data_angle,
                            "rsrp": data_rsrp,
                            "frame_counter": data_frame_counter
                        }
                        attr_result = json.dumps(attribute)
                    else:
                        token_id = req_data[59:74]
                        data_height = int(req_data[10:14], 16)
                        data_longitude_origin = req_data[16:24]
                        data_longitude = utility.IEEE754_Hex_To_Float(data_longitude_origin)
                        data_longitude = ("%.6f" % data_longitude)
                        data_latitude_origin = req_data[24:32]
                        data_latitude = utility.IEEE754_Hex_To_Float(data_latitude_origin)
                        data_latitude = ("%.6f" % data_latitude)
                        data_temperature = int(req_data[32:34], 16)
                        data_angle = int(req_data[36:38], 16) if (int(req_data[34:36], 16) == 0) else (
                                0 - int(req_data[36:38], 16))
                        data_full_alarm = int(req_data[38:39], 16)
                        data_fire_alarm = int(req_data[39:40], 16)
                        data_tilt_alarm = int(req_data[40:41], 16)
                        data_battery_alarm = int(req_data[41:42], 16)
                        data_volt = int(req_data[42:46], 16) / 100
                        data_rsrp_origin = req_data[46:54]
                        data_rsrp = int(utility.IEEE754_Hex_To_Float(data_rsrp_origin))
                        data_frame_counter = int(req_data[54:58], 16)
                        # print("rsrp is "+str(data_rsrp))
                        attribute = {
                            "height": data_height,
                            "longitude": data_longitude,
                            "latitude": data_latitude,
                            "temperature": data_temperature,
                            "full_alarm": data_full_alarm,
                            "fire_alarm": data_fire_alarm,
                            "tilt_alarm": data_tilt_alarm,
                            "battery_alarm": data_battery_alarm,
                            "volt": data_volt,
                            "angle": data_angle,
                            "rsrp": data_rsrp,
                            "frame_counter": data_frame_counter
                        }
                        attr_result = json.dumps(attribute)
                else:
                    if (data_type == "03"):
                        token_id = req_data[data_len*2-17:data_len*2-2]
                        data_version = str(int(req_data[10:12], 16))+"."+str(int(req_data[12:14], 16))
                        data_upload_interval = int(req_data[14:16], 16)
                        data_cyclic_interval = int(req_data[16:18], 16)  
                        data_level_threshold = int(req_data[18:20], 16)   
                        data_fire_threshold = int(req_data[20:22], 16)                     
                        data_tilt_threshold = int(req_data[22:24], 16)  
                        data_tilt_switch = int(req_data[40:42], 16) 
                        data_work_mode = int(req_data[44:46], 16)                 
                        
                        # print("rsrp is "+str(data_rsrp))
                        attribute = {
                            "firmware": data_version,
                            "uploadInterval": data_upload_interval,
                            "detectInterval": data_cyclic_interval,                            
                            "levelThreshold": data_level_threshold,
                            "fireThreshold": data_fire_threshold,
                            "fallThreshold": data_tilt_threshold,
                            "fallEnable": data_tilt_switch,
                            "workMode":data_work_mode,                        
                        }
                        attr_result = json.dumps(attribute)                    
                    else:
                        pass
                    
            else:
                pass
            #time.sleep(1)
        except Exception as e:
            print(e)
            #log.logger.exception(e)
        finally:
            return attr_result, token_id
        


if __name__ == "__main__":
    try:
        attr_result = ""
        #test data of 02 type packet.
        #incomingData = "8000010126069201CD03E942EF2720421A00000000016E008027C40001186962703655111781"
        #test data of 03 type packet.
        incomingData = "800001021E0649001B00000101015F008054440000186882104303887681"
        attr_result = DF703.parse_data_DF703(incomingData)        
    except Exception as e:
        print(e)