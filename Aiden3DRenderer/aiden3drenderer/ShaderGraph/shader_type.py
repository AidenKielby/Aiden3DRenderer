from enum import Enum

class ShaderType(Enum):
    FLOAT   = "float"
    INT     = "int"
    BOOL    = "bool"
    VEC2    = "vec2"
    VEC3    = "vec3"
    VEC4    = "vec4"
    MAT2    = "mat2"
    MAT3    = "mat3"
    MAT4    = "mat4"
    SAMPLER2D = "sampler2D"
    ANY     = "any"

    @classmethod
    def from_str(cls, label: str):
        return cls(label)