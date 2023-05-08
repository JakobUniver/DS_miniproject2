import multiprocessing
from concurrent.futures import ThreadPoolExecutor

import grpc

import miniproject2_pb2
import miniproject2_pb2_grpc

ALL_PORTS = ["20048", "20049", "20050"]
AVAILABLE_PORTS = []
MY_PORT = ''
MY_NAME = ''
WORKERS = []

DATA_STORES = {}


def get_name(port):
    return "Node-" + str(int(port) - 20047)


class ReadyClient:
    def __init__(self, channel):
        self.stub = miniproject2_pb2_grpc.ReadyServiceStub(channel)

    def server_ready(self, newport):
        request = miniproject2_pb2.ReadyRequest(newport=newport)
        response = self.stub.ServerReady(request)
        return response.ready


class ReadyServicer(miniproject2_pb2_grpc.ReadyServiceServicer):
    def ServerReady(self, request, context):
        new_port = request.newport
        AVAILABLE_PORTS.append(new_port)
        response = miniproject2_pb2.ReadyResponse()
        response.ready = 1
        return response


def broadcast_availability():
    global ALL_PORTS, AVAILABLE_PORTS

    #### TIMESYNC
    for port in ALL_PORTS:
        try:
            with grpc.insecure_channel(f'localhost:{port}') as channel:
                if port != MY_PORT:
                    client = ReadyClient(channel)
                    response = client.server_ready(newport=MY_PORT)
                print(f"Connected with {port}")
                AVAILABLE_PORTS.append(port)
        except grpc.RpcError as e:
            pass


def _run_process(bind_address):
    print('Starting new process.')
    options = (('grpc.so_reuseport', 1),)

    server = grpc.server(ThreadPoolExecutor(
        max_workers=5, ),
        options=options)
    miniproject2_pb2_grpc.add_ReadyServiceServicer_to_server(ReadyServicer(), server)
    server.add_insecure_port(bind_address)
    server.start()

    store_loop()

    print("End")
    server.wait_for_termination()


def localStorePs(threads):
    for worker in WORKERS:
        worker.join()
        with MY_PORT as port:
            bind_address = f"[::]:{port}"
            for _ in range(int(threads)):
                worker = multiprocessing.Process(target=_run_process,
                                                 args=(bind_address,))
                worker.start()
                WORKERS.append(worker)


def store_loop():
    global MY_NAME
    print("Making myself available to peers:")
    broadcast_availability()
    print("Broadcast end")

    MY_NAME = get_name(MY_PORT)

    # time.sleep(1)

    while True:
        args = input(f"{MY_NAME}> ").split(' ')
        command = args[0]
        if command == 'Local-store-ps':
            localStorePs(args[1])
        elif command == 'Create-chain':
            pass
        elif command == 'List-chain':
            pass
        elif command == 'Write-operation':
            pass
        elif command == 'List-books':
            pass
        elif command == 'Read-operation':
            pass
        elif command == 'Time-out':
            pass
        elif command == 'Data-status':
            pass
        elif command == 'Remove-head':
            pass
        elif command == 'Restore-head':
            pass
        elif command == 'list-ports':
            print(AVAILABLE_PORTS)
        elif command == 'stop':
            print("Goodbye!")
            break
        else:
            print("Command not available, try again")


if __name__ == "__main__":
    server = grpc.server(ThreadPoolExecutor(max_workers=5))
    while True:
        try:
            port = input("Insert server port: ")
            server.add_insecure_port("[::]:" + port)
            MY_PORT = port
            break
        except:
            print("This port is taken, try again:")

    miniproject2_pb2_grpc.add_ReadyServiceServicer_to_server(ReadyServicer(), server)
    server.start()
    print("Server CONNECTED to port " + port + "...")

    store_loop()

    for worker in WORKERS:
        worker.join()

    print("End")
    server.wait_for_termination()
