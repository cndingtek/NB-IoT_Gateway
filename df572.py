# Add DF572 4G version support.

import utility
import json


class DF572(object):
    # Func: parse data to attr DF572 TCP
    # Param: req_data: input data string in upper format
    #        attr_result: output attr
    #       token_id: token for thingsboard, imei
    # "80 00 71 01 21 1D 75 01 CB 00 00 00 19 0A 00 00 01 66 00 00 39 C4 00 02 18 63 25 10 74 28 28 85 81“ heart beat/alarm without gps
    # "80 00 71 01 29 1D 75 01 CB 01 CD 03 E9 42 EF 27 20 42 00 00 19 0A 00 00 01 66 00 00 39 C4 00 02 18 63 25 10 74 28 28 85 81" event packet with gps
    # "" Param
    def parse_data_DF572(req_data):
        try:
            data_type = req_data[6:8]
            data_len = int(req_data[8:10], 16)
            global attr_result
            global token_id
            if (data_len == len(req_data) / 2):
                if (data_type == "01" or data_type == "02"):
                    if (data_len == 33):
                        token_id = req_data[49:64]
                        data_levelHeight = int(req_data[10:14], 16)
                        data_airHeight = int(req_data[14:18], 16)
                        data_gpsEnabled = int(req_data[18:20], 16)
                        data_temperature = int(req_data[24:26], 16)
                        data_humidity = int(req_data[26:28], 16)
                        data_heightAlarm = int(req_data[28:29], 16)
                        data_temperatureAlarm = int(req_data[29:30], 16)
                        data_batteryAlarm = int(req_data[31:32], 16)
                        data_volt = int(req_data[32:36], 16) / 100
                        data_rsrpOrigin = req_data[36:44]
                        data_rsrp = int(
                            utility.utility.IEEE754_Hex_To_Float(data_rsrpOrigin))
                        data_frameCounter = int(req_data[44:48], 16)
                        # print("rsrp is "+str(data_rsrp))
                        attribute = {
                            "liquidLevel": data_levelHeight,
                            "airHeight": data_airHeight,
                            "gpsEnabled": data_gpsEnabled,
                            "temperature": data_temperature,
                            "humidity": data_humidity,
                            "levelAlarm": data_heightAlarm,
                            "temperatureAlarm": data_temperatureAlarm,
                            "batteryAlarm": data_batteryAlarm,
                            "volt": data_volt,
                            "rsrp": data_rsrp,
                            "frameCounter": data_frameCounter
                        }
                    else:
                        if (data_len == 41):
                            token_id = req_data[65:80]
                            data_levelHeight = int(req_data[10:14], 16)
                            data_airHeight = int(req_data[14:18], 16)
                            data_gpsEnabled = int(req_data[18:20], 16)
                            data_longitudeOrigin = req_data[20:28]
                            data_longitude = utility.utility.IEEE754_Hex_To_Float(
                                data_longitudeOrigin)
                            data_longitude = ("%.6f" % data_longitude)
                            data_latitudeOrigin = req_data[28:36]
                            data_latitude = utility.utility.IEEE754_Hex_To_Float(
                                data_latitudeOrigin)
                            data_latitude = ("%.6f" % data_latitude)
                            data_temperature = int(req_data[40:42], 16)
                            data_humidity = int(req_data[42:44], 16)
                            data_heightAlarm = int(req_data[44:45], 16)
                            data_temperatureAlarm = int(req_data[45:46], 16)
                            data_batteryAlarm = int(req_data[47:48], 16)
                            data_volt = int(req_data[48:52], 16) / 100
                            data_rsrpOrigin = req_data[52:60]
                            data_rsrp = int(
                                utility.utility.IEEE754_Hex_To_Float(data_rsrpOrigin))
                            data_frameCounter = int(req_data[60:64], 16)
                            # print("rsrp is "+str(data_rsrp))
                            attribute = {
                                "liquidLevel": data_levelHeight,
                                "airHeight": data_airHeight,
                                "gpsEnabled": data_gpsEnabled,
                                "longitude": data_longitude,
                                "latitude": data_latitude,
                                "temperature": data_temperature,
                                "humidity": data_humidity,
                                "levelAlarm": data_heightAlarm,
                                "temperatureAlarm": data_temperatureAlarm,
                                "batteryAlarm": data_batteryAlarm,
                                "volt": data_volt,
                                "rsrp": data_rsrp,
                                "frameCounter": data_frameCounter
                            }
                        else:
                            attribute = {}
                else:
                    if (data_len >= 32):
                        token_id = req_data[data_len*2-17:-2]
                        data_firmware_version = str(
                            int(req_data[10:12], 16))+"."+str(int(req_data[12:14], 16))
                        data_upload_interval = int(req_data[14:16], 16)
                        data_detect_interval = int(req_data[16:18], 16)
                        data_height_threshold = int(req_data[18:20], 16)
                        data_temperature_threshold = int(req_data[20:22], 16)
                        data_battery_threshold = int(req_data[24:26], 16)
                        data_suddent_drop_alarm_switch = int(
                            req_data[44:46], 16)
                        data_suddent_drop_alarm_threshold = int(
                            req_data[46:50], 16)
                        data_work_mode = int(req_data[50:52], 16)
                        attribute = {
                            "firmwareVersion": data_firmware_version,
                            "uploadInterval": data_upload_interval,
                            "detectInterval": data_detect_interval,
                            "heightThreshold": data_height_threshold,
                            "TemperatureThreshold": data_temperature_threshold,
                            "BatteryThreshold": data_battery_threshold,
                            "SuddentDropAlarmSwitch": data_suddent_drop_alarm_switch,
                            "SuddentDropAlarmThreshold": data_suddent_drop_alarm_threshold,
                            "workMode": data_work_mode,
                        }
                    else:
                        attribute = {}
                attr_result = json.dumps(attribute)
            else:
                attr_result = json.dumps("")
                token_id = ""
            # time.sleep(1)
        except Exception as e:
            print(e)
            # log.logger.exception(e)
        finally:
            return attr_result, token_id


if __name__ == "__main__":
    try:
        attr_result = ""
        incomingData = "80007103340102180A1E4B1E14186325107428288501000064003132392E3232362E31312E33303B29403B186325107428288581"
        attr_result = DF572.parse_data_DF572(incomingData)
    except Exception as e:
        print(e)
