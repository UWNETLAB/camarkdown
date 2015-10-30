from .init import startInit
from .status import startStatus
from .add import startAdd

subCommands = {
    "init" : startInit,
    "status" : startStatus,
    "add" : startAdd,
}
