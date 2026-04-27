import pytest

from vm2 import (
    Connection,
    OpenConnectionState,
    ClosedConnectionState,
)


# --- Initial state -----------------------------------------------------------


def test_initial_state_is_closed():
    c = Connection()
    assert isinstance(c.get_state(), ClosedConnectionState)
    assert str(c) == "State: ClosedConnectionState"


# --- Closed state behavior ---------------------------------------------------


def test_read_on_closed_raises():
    c = Connection()
    with pytest.raises(RuntimeError, match="Cannot read closed connection"):
        c.read()


def test_write_on_closed_raises():
    c = Connection()
    with pytest.raises(RuntimeError, match="Cannot write closed connection"):
        c.write("data")


def test_close_on_closed_raises():
    c = Connection()
    with pytest.raises(RuntimeError, match="already closed"):
        c.close()


def test_open_transitions_to_open_state():
    c = Connection()
    c.open()
    assert isinstance(c.get_state(), OpenConnectionState)
    assert str(c) == "State: OpenConnectionState"


# --- Open state behavior -----------------------------------------------------


def test_read_on_open_returns_data_and_keeps_state(capsys):
    c = Connection()
    c.open()

    data = c.read()

    captured = capsys.readouterr()
    assert "Reading" in captured.out

    assert data == "Hello!"
    assert isinstance(c.get_state(), OpenConnectionState)


def test_write_on_open_prints_and_keeps_state(capsys):
    c = Connection()
    c.open()

    c.write("Bye")

    captured = capsys.readouterr()
    assert "Bye" in captured.out
    assert isinstance(c.get_state(), OpenConnectionState)


def test_open_on_open_raises():
    c = Connection()
    c.open()

    with pytest.raises(RuntimeError, match="already open"):
        c.open()


def test_close_on_open_transitions_to_closed():
    c = Connection()
    c.open()

    c.close()

    assert isinstance(c.get_state(), ClosedConnectionState)
    assert str(c) == "State: ClosedConnectionState"


# --- State transition sequence -----------------------------------------------


def test_full_lifecycle():
    c = Connection()

    # closed → open
    c.open()
    assert isinstance(c.get_state(), OpenConnectionState)

    # open → read/write
    assert c.read() == "Hello!"
    c.write("test")

    # open → closed
    c.close()
    assert isinstance(c.get_state(), ClosedConnectionState)


# --- Metaclass behavior ------------------------------------------------------


def test_state_class_str_and_repr():
    # __str__ from metaclass
    assert str(OpenConnectionState) == "State: OpenConnectionState"
    assert str(ClosedConnectionState) == "State: ClosedConnectionState"

    # __repr__ from metaclass
    assert repr(OpenConnectionState) == "<State OpenConnectionState>"
    assert repr(ClosedConnectionState) == "<State ClosedConnectionState>"


# --- Representation of Connection --------------------------------------------


def test_connection_repr_uses_state_class():
    c = Connection()
    assert repr(c) == "<State ClosedConnectionState>"

    c.open()
    assert repr(c) == "<State OpenConnectionState>"
