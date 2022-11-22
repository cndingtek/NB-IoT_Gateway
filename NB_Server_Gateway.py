# Gateway for CNDingtek kindes sensor NB-IoT version gateway
# change log Nov 28, 2020. change the created threading not close automatically.
# coding:utf-8

import socket

# import json
# import struct
# import base64
# from multiprocessing import Process
import Logger
import threading
import http.client
import time

# import utility
#import df200
#import df400
#import do200


import df702
import df555
# import dc500
#import dt310


# import dh100

port_number = 9000
max_clients = 10
attr_result = ""
token_id = ""
log = Logger.Logger("all.log", level="debug")


# Func: upload data to thingsboard by http post
# param: attr: json pairs
#       token: token id
# remark: use your application server and port to replace below domain name and port number YYYY
def upload_data(attr, token):
    try:
        # params = urllib.parse.urlencode(attr)
        print("try to upload data ")
        str_url = "/api/v1/" + token + "/telemetry"
        len_attr = len(attr)
        headers = {
            "Host": "www.dingtek.com:YYYY",
            "User-Agent": "curl/7.55.1",
            "Accept-Language": "*/*",
            "Content-Type": "application/json",
            "Content-Length": str(len_attr),
        }
        '''use your own http application domain name /ip/port replace below. of course if you use 
           other type application, please change to the corresponsing protocol.
        '''
        conn = http.client.HTTPConnection("www.dingtek.com:6000", timeout=10)
        conn.request("POST", str_url, attr, headers)
        r1 = conn.getresponse()
        print("response is ", str(r1.getcode()))
        log.logger.debug("upload_data: response is " + str(r1.getcode()))
        # 关闭连接
        conn.close()
        # print("close socket in upload_data")
        log.logger.debug("upload_data: close socket in upload_data")
        # return 1
    except Exception as ex:
        print(ex)
        log.logger.exception("upload_data", ex)
    finally:
        return 1


# reponse sensor upload data
# param: client: client socket
#       data: response data in string
def response_sensor(client, data):
    try:
        client.send(bytes(data, "utf-8"))
    except Exception as ex:
        # print(e)
        log.logger.exception(ex)


# handle client request
# param: client: client socket
#       address:client address
def handle_client(client, address):
    """
    处理客户端请求,
    """
    try:
        client.settimeout(10)
        # 超时时间
        request_bytes = b""
        global attr_result
        request_str = ""
        global token_id
        find_result1 = -1
        while True:
            if not client._closed:
                request_bytes = request_bytes + client.recv(1024)
            if not request_bytes:
                # print("Connection closed")
                break
                # client.close()
            request_str = request_bytes.hex()
            find_result1 = str(request_str).find("8000")
            if find_result1 != -1:
                print(request_str)
                break
            # print(request_data)
        str_subreq = str(request_str[find_result1:])
        data_type = str_subreq[4:6]
        log.logger.debug("packet is %s, data_type is DF%s0", str_subreq, data_type)

        # parse and upload

        # for other data_type, there are several module sensors, use different listening port to recognize them.

        if data_type == "01":
            attr_result, token_id = df555.DF555.parse_data_DF555(str_subreq.strip().upper())
            #attr_result, token_id = dt310.DT310.parse_data(str_subreq.strip().upper())
        print("attr is"+attr_result+".token_id is "+token_id)
        log.logger.debug("attr is"+attr_result+".token_id is "+token_id)
        if attr_result != "" and token_id != "":
            upload_data(attr_result, token_id)
            log.logger.debug("after upload data ")
        else:
            log.logger.debug("invalid data ")
        time.sleep(1)
        client.close()
        time.sleep(1)
        log.logger.debug("close device connection ")
    except socket.timeout:
        print("time out")
        client.close()


if __name__ == "__main__":
    try:
        attr_result = ""
        token_deviceid = ""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", port_number))
        server_socket.listen(max_clients)
        while True:
            client_socket, client_address = server_socket.accept()
            log.logger.debug(str(client_address) + "user connected!")
            thread = threading.Thread(
                target=handle_client, args=(client_socket, client_address)
            )
            thread.start()
            log.logger.debug("after handle_client_process close!")
    except Exception as e:
        print(e)
        log.logger.error(e)
