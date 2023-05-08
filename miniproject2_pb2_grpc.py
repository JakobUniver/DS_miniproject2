# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import miniproject2_pb2 as miniproject2__pb2


class ReadyServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ServerReady = channel.unary_unary(
                '/ReadyService/ServerReady',
                request_serializer=miniproject2__pb2.ReadyRequest.SerializeToString,
                response_deserializer=miniproject2__pb2.ReadyResponse.FromString,
                )


class ReadyServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ServerReady(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReadyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ServerReady': grpc.unary_unary_rpc_method_handler(
                    servicer.ServerReady,
                    request_deserializer=miniproject2__pb2.ReadyRequest.FromString,
                    response_serializer=miniproject2__pb2.ReadyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ReadyService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ReadyService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ServerReady(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReadyService/ServerReady',
            miniproject2__pb2.ReadyRequest.SerializeToString,
            miniproject2__pb2.ReadyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ChainServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetProcesses = channel.unary_unary(
                '/ChainService/GetProcesses',
                request_serializer=miniproject2__pb2.ProcessesRequest.SerializeToString,
                response_deserializer=miniproject2__pb2.ProcessesResponse.FromString,
                )
        self.PassChain = channel.unary_unary(
                '/ChainService/PassChain',
                request_serializer=miniproject2__pb2.PassChainRequest.SerializeToString,
                response_deserializer=miniproject2__pb2.PassChainResponse.FromString,
                )


class ChainServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetProcesses(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PassChain(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChainServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetProcesses': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProcesses,
                    request_deserializer=miniproject2__pb2.ProcessesRequest.FromString,
                    response_serializer=miniproject2__pb2.ProcessesResponse.SerializeToString,
            ),
            'PassChain': grpc.unary_unary_rpc_method_handler(
                    servicer.PassChain,
                    request_deserializer=miniproject2__pb2.PassChainRequest.FromString,
                    response_serializer=miniproject2__pb2.PassChainResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ChainService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChainService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetProcesses(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChainService/GetProcesses',
            miniproject2__pb2.ProcessesRequest.SerializeToString,
            miniproject2__pb2.ProcessesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PassChain(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChainService/PassChain',
            miniproject2__pb2.PassChainRequest.SerializeToString,
            miniproject2__pb2.PassChainResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
