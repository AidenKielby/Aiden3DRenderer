
from enum import Enum


class ElementType(Enum):
    FUNCTION = "function"
    UNIFORM_LAYOUT = "uniform or layout"
    MAIN_FUNCTION_EXECUTABLE = "main function execitable"
    OUTPUT_ONLY = "output only"
    USER_DEFINED = "user defined"

class Element:
    def __init__(self, name: str, inputs: list[type], outputs: list[type], variable_name: str, function: str, type: ElementType, category: str = "misc"):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.variable_name = variable_name
        self.function = function
        self.type = type
        self.category = category
        self.last_missing_input_index = None
