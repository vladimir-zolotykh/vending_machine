#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Connection:
    def __init__(self):
        self.state = OpenConnectionState(self)

    def read(self):
        data, new_state = self.state.read()
        self.state = new_state
        return data

    def write(self, data: str) -> None:
        self.state = self.state.write(data)

    def open(self):
        self.state = self.state.open()

    def close(self):
        self.state = self.state.close()


class ConnectionState:
    def __init__(self, conn):
        self.conn = conn

    # fmt: off
    def read(): raise NotImplementedError()  # noqa: E704
    def write(): raise NotImplementedError()  # noqa: E704
    def open(): raise NotImplementedError()  # noqa: E704
    def close(): raise NotImplementedError()  # noqa: E704
    # fmt: on


class OpenConnectionState(ConnectionState):
    def read(self):
        print("Reading")
        return self.conn.get_state()

    def write(self):
        print("Writing")
        return self.conn.get()

    def open(self):
        raise RuntimeError("Already open")

    def close(self) -> ConnectionState:
        return ClosedConnectionState(self.conn)


class ClosedConnectionState(ConnectionState):
    def read(self):
        raise RuntimeError("Cannot read closed connection")

    def write(self):
        raise RuntimeError("Cannot write closed connection")

    def open(self) -> ConnectionState:
        return OpenConnectionState(self.conn)

    def close(self):
        raise RuntimeError("Connecton is already closed")


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
    c.close()
    print(c)
