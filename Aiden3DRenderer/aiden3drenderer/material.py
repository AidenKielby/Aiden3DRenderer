
class Material:
    def __init__(self, name:str, texture_path:str, texture_index:int, base_color: tuple[float] = (155, 0, 0), transparent:bool = False, alpha:float = 1.0):
        self.name = name
        self.texture_path = texture_path
        self.texture_index = texture_index
        self.base_color = base_color
        self.is_trasparent = transparent
        self.alpha = alpha
    
    def get_material_from_file(self, file_path:str):
        """Gets material from .mat file"""
        if file_path.split(".")[-1] != "mat":
            raise SyntaxError(f"Unrecognized file ending: {file_path.split('.')[-1]}. Please use '.mat'")
        with open(file_path, "r") as mat_file:
            i = 0
            for line in mat_file:
                if i == 0:
                    self.name=line.replace('"', '').strip()
                    i+=1
                else:
                    line_segments = line.split("=")
                    if line_segments[0].strip().replace('"', '') == "TextureIndex":
                        self.texture_index = int(line_segments[1].strip())
                    if line_segments[0].strip().replace('"', '') == "TexturePath":
                        self.texture_path = str(line_segments[1].strip())
                    if line_segments[0].strip().replace('"', '') == "BaseColor":
                        self.base_color = tuple(int(x.strip()) for x in line_segments[1].split(','))
                    if line_segments[0].strip().replace('"', '') == "Transparent":
                        self.transparent = bool(line_segments[1].strip())
                    if line_segments[0].strip().replace('"', '') == "Alpha":
                        self.alpha = int(line_segments[1].strip())
        