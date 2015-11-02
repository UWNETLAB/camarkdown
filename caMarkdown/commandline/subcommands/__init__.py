from .init import startInit
from .status import startStatus
from .add import startAdd
from .table import startTable

subCommands = {
    "init" : startInit,
    "status" : startStatus,
    "add" : startAdd,
    "table" : startTable,
}
