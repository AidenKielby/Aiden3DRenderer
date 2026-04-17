from element import Element, ElementType
from shader_type import ShaderType

getPixelAtFunc = f"vec3 PLACEHOLDER = texelFetch(input1, ivec2(input2), 0).rgb;"
getPixelAt = Element("getPixelAt", [ShaderType.SAMPLER2D, ShaderType.VEC2], [ShaderType.VEC3], "rgb", getPixelAtFunc, ElementType.MAIN_FUNCTION_EXECUTABLE)

writePixelAtFunc = "imageStore(destTex, input1, vec4(input2, 1.0));"
writePixelAt = Element("writePixelAt", [ShaderType.VEC2, ShaderType.VEC2], [], None, writePixelAtFunc, ElementType.MAIN_FUNCTION_EXECUTABLE)

equalsFunc = f"PLACEHOLDER = input1 == input2;"
equals = Element("equals", [ShaderType.ANY, ShaderType.ANY], [ShaderType.BOOL], "equals_out", equalsFunc, ElementType.MAIN_FUNCTION_EXECUTABLE)
