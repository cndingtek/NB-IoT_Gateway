#/***********************************************************************************************************
# * Microwave Radar People Counter DC520 Codec for nb-iot version.
# * Version 1.0  Date 2024-02-22 
# * 
# * 
# ***********************************************************************************************************/
import Logger
import json
from utility import utility


class DC520(object):
    # Func: parse data to attr
    # Param: req_data: input data string in upper format
    #        attr_result: output attr
    #       token_id: token for thingsboard, imei
    # "800052022300010002000100000000008031C4657960E0000001186195906498934181" heart beat/alarm
    # "" Param
    def parse_data_DC520(req_data):
        try:
            data_type = req_data[6:8]
            data_len = int(req_data[8:10], 16)
            global attr_result
            global token_id

            if data_len == len(req_data) / 2:
                if (data_type == "01" or data_type == "02") and (data_len ==35 ):
                    token_id = req_data[53:68]                    
                    data_balance_counter = int(req_data[10:14], 16)
                    data_in_counter = int(req_data[14:18], 16)
                    data_out_counter = int(req_data[18:22], 16)
                    data_alarm_balance = int(req_data[22:23], 16)      
                    data_alarm_in = int(req_data[23:24], 16) 
                    data_alarm_out = int(req_data[24:25], 16) 
                    data_alarm_battery = int(req_data[25:26], 16)               
                    data_volt = int(req_data[26:30], 16) / 100
                    data_rsrp_origin = req_data[30:38]
                    data_rsrp = int(utility.IEEE754_Hex_To_Float(data_rsrp_origin))                   
                    data_timestamp = int(req_data[38:46], 16)
                    data_errorcode = int(req_data[46:48], 16)
                    data_frame_counter = int(req_data[48:52], 16)
                    # print("rsrp is "+str(data_rsrp))
                    attribute = {
                        "balanceCounter": data_balance_counter,
                        "inCounter": data_in_counter,
                        "outCounter": data_out_counter,
                        "alarmBalance": data_alarm_balance,
                        "alarmIn": data_alarm_in,
                        "alarmOut": data_alarm_out,
                        "alarmBattery": data_alarm_battery,
                        "volt": data_volt,
                        "errorCode": data_errorcode,     
                        "timestamp": data_timestamp, 
                        "rsrp": data_rsrp,                                  
                        "frame_counter": data_frame_counter,
                    }
                    attr_result = json.dumps(attribute)
                else:
                    if (data_type == "03"):
                        token_id = req_data[data_len*2-17:data_len*2-2]
                        data_version = str(int(req_data[10:12], 16))+"."+str(int(req_data[12:14], 16))
                        data_upload_interval = int(req_data[14:16], 16)
                        data_balance_original = int(req_data[16:20], 16)                        
                        data_balance_threshold = int(req_data[20:24], 16)  
                        data_in_threshold = int(req_data[24:28], 16)  
                        data_out_threshold = int(req_data[28:32], 16)  
                        data_battery_threshold = int(req_data[32:34], 16)                 
                        
                        # print("rsrp is "+str(data_rsrp))
                        attribute = {
                            "firmware": data_version,
                            "uploadInterval": data_upload_interval,
                            "originalBalance": data_balance_original,                            
                            "balanceThreshold": data_balance_threshold,
                            "inThreshold": data_in_threshold,
                            "outThreshold": data_out_threshold,
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
        #test data of 02 type packet.
        #incomingData = "800052022300010002000100000000008031C4657960E0000001186195906498934181"
        #test data of 03 type packet.
        incomingData = "800052033301020100050064003200141414600819595049063132302E39322E38392E3132323B23783B186195906498934181"
        attr_result = DC520.parse_data_DC520(incomingData)        
    except Exception as e:
        print(e)
        