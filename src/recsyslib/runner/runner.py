import socket
from abc import ABC, abstractmethod
from argparse import ArgumentParser

import rpyc
from rpyc.utils.server import ThreadedServer


class IRunnerService(ABC):
    @abstractmethod
    def fit(self): ...

    @abstractmethod
    def predict(self): ...

    @abstractmethod
    def evaluate(self): ...


class RunnerService(rpyc.Service, IRunnerService, ABC):
    def fit(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError

    def evaluate(self):
        raise NotImplementedError

    def _fit(self): ...
    def _predict(self): ...
    def _evaluate(self): ...


class Runner:
    def __init__(self) -> None:
        self._server = ThreadedServer(
            RunnerService(), port=33741
        )  # HACK: Remove this hard coded port

    def get_address(self):
        host = socket.gethostbyname(socket.gethostname())
        return host, self._server.port

    def start(self):
        self._server.start()


# class RunnerClient:
#     def __init__(self, host: IPv4Address | IPv6Address, port: int, secret: str) -> None:
#         conn = rpyc.connect(str(host), port)
#         remote: IRunnerService = conn.root


def main():
    parser = ArgumentParser()
    parser.add_argument("secret", type=str)

    args = parser.parse_args()

    server = RunnerServer()
    address = server.get_address()
    print(f"{address[0]} {address[1]}")
    server.start()


if __name__ == "__main__":
    main()
