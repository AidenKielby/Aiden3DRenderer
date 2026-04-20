class ShaderTarget:
    def __init__(self, name, header, globals_block, main_wrapper, entry_inputs=None, restricted_elements: list[str] = []):
        self.name = name
        self.header = header
        self.globals_block = globals_block
        self.main_wrapper = main_wrapper
        self.entry_inputs = entry_inputs or []
        self.restricted_elements = restricted_elements