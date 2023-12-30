from dataclasses import dataclass


class Event:
    pass

class CloseApp(Event):
    pass

class OpenRepo(Event):
    pass

@dataclass
class Decorate(Event):
    select: list[int] = None
    deselect: list[int] = None
    hover: list[int] = None
    dehover: list[int] = None
    highlight: list[int] = None
    dehighlight: list[int] = None

@dataclass
class Decorate2(Event):
    select: tuple[bool, bool] = None
    hover: tuple[bool, bool] = None
    highlight: tuple[bool, bool] = None
    blks: list[tuple[select,hover,highlight]] = None

@dataclass
class NewWindow(Event):
    header: str
    body: str