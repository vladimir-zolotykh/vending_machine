#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class StateMeta(type):
    def __repr__(cls):
        return cls.__name__


class Connection:
    def __init__(self):
        self.state = ClosedConnectionState(self)

    def get_state(self) -> "ConnectionState":
        return self.state

    def read(self):
        new_state, data = self.state.read()
        self.state = new_state
        return data

    def write(self, data: str) -> None:
        self.state = self.state.write(data)

    def open(self):
        self.state = self.state.open()

    def close(self):
        self.state = self.state.close()

    def __repr__(self):
        return repr(self.state.__class__)


class ConnectionState(metaclass=StateMeta):
    def __init__(self, conn):
        self.conn = conn

    # fmt: off
    def read(): raise NotImplementedError()  # noqa: E704
    def write(): raise NotImplementedError()  # noqa: E704
    def open(): raise NotImplementedError()  # noqa: E704
    def close(): raise NotImplementedError()  # noqa: E704
    # fmt: on


class OpenConnectionState(ConnectionState):
    def read(self) -> tuple[ConnectionState, str]:
        print("Reading")
        return self.conn.get_state(), "Hello!"

    def write(self, data):
        print(data)
        return self.conn.get_state()

    def open(self):
        raise RuntimeError(f"{self.conn}: already open")

    def close(self) -> ConnectionState:
        return ClosedConnectionState(self.conn)


class ClosedConnectionState(ConnectionState):
    def read(self):
        raise RuntimeError("Cannot read closed connection")

    def write(self, data):
        raise RuntimeError("Cannot write closed connection")

    def open(self) -> ConnectionState:
        return OpenConnectionState(self.conn)

    def close(self):
        raise RuntimeError("Connecton is already closed")


# <__main__.Connection object at 0x7f9e64e28690>
# Not open
# <__main__.Connection object at 0x7f9e64e28690>
# reading
# <__main__.Connection object at 0x7f9e64e28690>

if __name__ == "__main__":
    c = Connection()
    print(c)
    try:
        c.read()
    except RuntimeError as e:
        print(e)

    c.open()
    print(c)
    c.read()
    c.write("Bye")
    c.close()
    print(c)
