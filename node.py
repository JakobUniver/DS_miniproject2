import contextlib
import multiprocessing
import random
from concurrent.futures import ThreadPoolExecutor
import socket

import grpc

import miniproject2_pb2
import miniproject2_pb2_grpc

ALL_PORTS = ["20048", "20049", "20050"]
AVAILABLE_PORTS = []
MY_PORT = ''
MY_NAME = ''
WORKERS = {}

CHAIN = []


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


class ChainClient:
    def __init__(self, channel):
        self.stub = miniproject2_pb2_grpc.ChainServiceStub(channel)

    def get_processes(self):
        request = miniproject2_pb2.ProcessesRequest()
        response = self.stub.GetProcesses(request)
        return response.pnumber

    def pass_chain(self, chain):
        request = miniproject2_pb2.PassChainRequest(chain=chain)
        response = self.stub.PassChain(request)
        return response.success


class ChainServicer(miniproject2_pb2_grpc.ChainServiceServicer):

    def GetProcesses(self, request, context):
        response = miniproject2_pb2.ProcessesResponse()
        response.pnumber = len(WORKERS)
        return response

    def PassChain(self, request, context):
        global CHAIN
        CHAIN = request.chain
        response = miniproject2_pb2.PassChainResponse()
        response.success = True
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


@contextlib.contextmanager
def _reserve_port(port):
    socket.SO_REUSEPORT = 1
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 0:
        raise RuntimeError("Failed to set SO_REUSEPORT.")
    sock.bind(("", int(port)))
    try:
        yield sock.getsockname()[1]
    finally:
        sock.close()


def _run_process(bind_address):
    print('Starting new process.')
    options = [('grpc.so_reuseport', 1)]

    server = grpc.server(ThreadPoolExecutor(
        max_workers=10),
        options=options)
    miniproject2_pb2_grpc.add_ReadyServiceServicer_to_server(ReadyServicer(), server)
    server.add_insecure_port(bind_address)
    server.start()
    server.wait_for_termination()


def localStorePs(threads):
    with _reserve_port(MY_PORT) as port:
        bind_address = f"[::]:{port}"
        for i in range(int(threads)):
            worker = multiprocessing.Process(target=_run_process,
                                             args=(bind_address,))
            worker.start()
            WORKERS[MY_NAME + "-ps" + str(i + 1)] = worker

        for worker in WORKERS.values():
            worker.join()


def createChain():
    all_workers = []
    for port in AVAILABLE_PORTS:
        with grpc.insecure_channel(f'localhost:{port}') as channel:
            client = ChainClient(channel)
            processes = client.get_processes()
            for i in range(processes):
                all_workers.append(str(get_name(port) + '-ps' + str(i + 1)))

    random.shuffle(all_workers)
    for port in AVAILABLE_PORTS:
        with grpc.insecure_channel(f'localhost:{port}') as channel:
            client = ChainClient(channel)
            passed = client.pass_chain(all_workers)
    print(f"Chain created")


def listChain():
    print(CHAIN)


def store_loop():
    global MY_NAME
    print("Broadcasting myself to peers:")
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
            createChain()
        elif command == 'List-chain':
            listChain()
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
        elif command == 'List-Processes':
            print(WORKERS)
        elif command == 'Stop':
            print("Goodbye!")
            break
        elif command == '':
            pass
        else:
            print("Command not available, try again")


if __name__ == "__main__":
    options = [("grpc.so_reuseport", 1),
               ("grpc.use_local_subchannel_pool", 1)]
    server = grpc.server(ThreadPoolExecutor(max_workers=10), options=options)
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
    print(WORKERS)

    print("End")
    server.stop(None)
