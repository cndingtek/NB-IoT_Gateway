#/***********************************************************************************************************
# * Manhole Detector with level measurement DC400 Codec for nb-iot version.
# * Version 1.0  Date 2024-02-23 
# * 
# * 
# ***********************************************************************************************************/

from utility import utility
import json

class DC400(object):
    # Func: parse data to attr DC400 TCP
    # Param: req_data: input data string in upper format
    #        attr_result: output attr
    #       token_id: token for thingsboard, imei
    # "800001011E04E20019012500100168008064C40002186505704285330381" heart beat/alarm without gps    
    # "" Param
    def parse_data_DC400(req_data):
        try:
            data_type = req_data[6:8]
            data_len = int(req_data[8:10], 16)
            global attr_result
            global token_id

            if (data_len == len(req_data) / 2):
                if (data_type == "01" or data_type == "02"):
                    if (data_len == 30):
                        token_id = req_data[43:58]                        
                        data_temperature = int(req_data[16:18], 16)
                        data_angle = int(req_data[20:22], 16) if (int(req_data[18:20], 16) == 0) else (
                                0 - int(req_data[20:22], 16))                                               
                        data_tilt_alarm = int(req_data[24:25], 16)
                        data_battery_alarm = int(req_data[25:26], 16)
                        data_volt = int(req_data[26:30], 16) / 100
                        data_rsrp_origin = req_data[30:38]
                        data_rsrp = int(utility.IEEE754_Hex_To_Float(data_rsrp_origin))
                        data_frame_counter = int(req_data[38:42], 16)
                        # print("rsrp is "+str(data_rsrp))
                        attribute = {                            
                            "temperature": data_temperature,                                                        
                            "tilt_alarm": data_tilt_alarm,
                            "battery_alarm": data_battery_alarm,
                            "volt": data_volt,
                            "angle": data_angle,
                            "rsrp": data_rsrp,
                            "frame_counter": data_frame_counter
                        }
                        attr_result = json.dumps(attribute)
                    else:
                        pass
                else:
                    if (data_type == "03"):
                        token_id = req_data[data_len*2-17:data_len*2-2]
                        data_version = str(int(req_data[10:12], 16))+"."+str(int(req_data[12:14], 16))
                        data_upload_interval = int(req_data[14:16], 16)
                        data_cyclic_interval = int(req_data[16:18], 16)                          
                        data_tilt_threshold = int(req_data[22:24], 16)  
                        data_tilt_switch = int(req_data[40:42], 16) 
                        data_work_mode = int(req_data[44:46], 16)   
                        # print("rsrp is "+str(data_rsrp))
                        attribute = {
                            "firmware": data_version,
                            "uploadInterval": data_upload_interval,
                            "detectInterval": data_cyclic_interval, 
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
        #incomingData = "800001011E04E20019012500100168008064C40002186505704285330381"
        #test data of 03 type packet.
        incomingData = "80000103410309180A1E4B1E1460113024932380010101003132302E39322E38392E3132323B23823B3135392E3133382E342E363B22B83B186505704285330381"
        attr_result = DC400.parse_data_DC400(incomingData)        
    except Exception as e:
        print(e)