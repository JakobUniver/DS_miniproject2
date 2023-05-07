import grpc
import datetime
import time
from concurrent.futures import ThreadPoolExecutor
import miniproject2_pb2
import miniproject2_pb2_grpc

PORTS = ["20048", "20049", "20050"]
MY_PORT = ''
MASTER_PORT = '20048'


class ReadyClient:
    def __init__(self, channel):
        self.stub = miniproject2_pb2_grpc.ReadyServiceStub(channel)

    def server_ready(self):
        request = miniproject2_pb2.ReadyRequest()
        response = self.stub.ServerReady(request)
        return response.ready


class ReadyServicer(miniproject2_pb2_grpc.ReadyServiceServicer):
    def ServerReady(self, request, context):
        response = miniproject2_pb2.ReadyResponse()
        response.ready = 1
        return response


def servers_ready():
    global PORTS

    #### TIMESYNC
    try:
        for port in PORTS:
            with grpc.insecure_channel(f'localhost:{port}') as channel:
                client = ReadyClient(channel)
                response = client.server_ready()
    except grpc.RpcError as e:
        print("Trying to contact peers again!")


if __name__ == "__main__":
    server = grpc.server(ThreadPoolExecutor(max_workers=5))
    while True:
        try:
            port = input("Insert server port: ")
            server.add_insecure_port("[::]:" + port)
            PORTS.remove(port)
            MY_PORT = port
            break
        except:
            print("This port is taken, try again:")

    miniproject2_pb2_grpc.add_ReadyServiceServicer_to_server(ReadyServicer(), server)
    server.start()
    print("Server CONNECTED to port " + port + "...")

    # store_loop()

    print("End")
    server.wait_for_termination()
