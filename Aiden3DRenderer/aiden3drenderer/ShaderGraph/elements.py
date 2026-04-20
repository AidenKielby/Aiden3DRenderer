try:
	from .element import Element, ElementType
	from .shader_type import ShaderType
except ImportError:
	from element import Element, ElementType
	from shader_type import ShaderType



srcImgFunc = f"uniform sampler2D srcTex;"
srcImg = Element("SrcTex", [], [ShaderType.SAMPLER2D], "srcTex", srcImgFunc, ElementType.UNIFORM_LAYOUT, "texture")

destImgFunc = f"imageStore(destTex, pixel_coords, vec4(input1, 1.0));"
destImg = Element("ImageWrite", [ShaderType.VEC3], [], "imageStore", destImgFunc, ElementType.OUTPUT_ONLY, "output")

pixelCoordsFunc = f"ivec2 pixel_coords = ivec2(gl_GlobalInvocationID.xy);"
pixelCoords = Element("PixelCoords", [], [ShaderType.VEC2], "pixel_coords", pixelCoordsFunc, ElementType.MAIN_FUNCTION_EXECUTABLE, "coord")

fragOutput = Element(
    "FragColor",
    [ShaderType.VEC3],
    [],
    "FragColor",
    "FragColor = vec4(input1, 1.0);",
    ElementType.OUTPUT_ONLY,
    "output"
)

vertexOutput = Element(
    "VertexPos",
    [ShaderType.VEC3],
    [],
    "gl_Position",
    "gl_Position = MVP * vec4(input1, 1.0);",
    ElementType.OUTPUT_ONLY,
    "output"
)

getPixelAtFunc = f"vec3 PLACEHOLDER = texelFetch(input1, ivec2(input2), 0).rgb;"
getPixelAt = Element("FetchTexel", [ShaderType.SAMPLER2D, ShaderType.VEC2], [ShaderType.VEC3], "rgb", getPixelAtFunc, ElementType.MAIN_FUNCTION_EXECUTABLE, "texture")

equalsFunc = f"bool PLACEHOLDER = input1 == input2;"
equals = Element("Equal", [ShaderType.ANY, ShaderType.ANY], [ShaderType.BOOL], "equals_out", equalsFunc, ElementType.MAIN_FUNCTION_EXECUTABLE, "compare")

lessThan = Element("Less", [ShaderType.ANY, ShaderType.ANY], [ShaderType.BOOL], "lt_out", "bool PLACEHOLDER = input1 < input2;", ElementType.MAIN_FUNCTION_EXECUTABLE, "compare")

greaterThan = Element("Greater", [ShaderType.ANY, ShaderType.ANY], [ShaderType.BOOL], "gt_out", "bool PLACEHOLDER = input1 > input2;", ElementType.MAIN_FUNCTION_EXECUTABLE, "compare")

select = Element("Mix", [ShaderType.ANY, ShaderType.ANY, ShaderType.FLOAT], [ShaderType.ANY], "mix_out", "PLACEHOLDER = mix(input1, input2, input3);", ElementType.MAIN_FUNCTION_EXECUTABLE, "blend")

add = Element("Add", [ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "add_out", "PLACEHOLDER = input1 + input2;", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

subtract = Element("Sub", [ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "sub_out", "PLACEHOLDER = input1 - input2;", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

multiply = Element("Mul", [ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "mul_out", "PLACEHOLDER = input1 * input2;", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

divide = Element("Div", [ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "div_out", "PLACEHOLDER = input1 / input2;", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

dotProduct = Element("Dot", [ShaderType.VEC3, ShaderType.VEC3], [ShaderType.FLOAT], "dot_out", "float PLACEHOLDER = dot(input1, input2);", ElementType.MAIN_FUNCTION_EXECUTABLE, "vector")

crossProduct = Element("Cross", [ShaderType.VEC3, ShaderType.VEC3], [ShaderType.VEC3], "cross_out", "vec3 PLACEHOLDER = cross(input1, input2);", ElementType.MAIN_FUNCTION_EXECUTABLE, "vector")

normalize = Element("Normalize", [ShaderType.VEC3], [ShaderType.VEC3], "norm_out", "vec3 PLACEHOLDER = normalize(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "vector")

lengthVec = Element("Length", [ShaderType.VEC3], [ShaderType.FLOAT], "len_out", "float PLACEHOLDER = length(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "vector")

minVal = Element("Min", [ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "min_out", "PLACEHOLDER = min(input1, input2);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

maxVal = Element("Max", [ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "max_out", "PLACEHOLDER = max(input1, input2);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

clamp = Element("Clamp", [ShaderType.ANY, ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "clamp_out", "PLACEHOLDER = clamp(input1, input2, input3);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

sinNode = Element("Sin", [ShaderType.FLOAT], [ShaderType.FLOAT], "sin_out", "float PLACEHOLDER = sin(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

cosNode = Element("Cos", [ShaderType.FLOAT], [ShaderType.FLOAT], "cos_out", "float PLACEHOLDER = cos(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

powNode = Element("Pow", [ShaderType.FLOAT, ShaderType.FLOAT], [ShaderType.FLOAT], "pow_out", "float PLACEHOLDER = pow(input1, input2);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

absNode = Element("Abs", [ShaderType.ANY], [ShaderType.ANY], "abs_out", "PLACEHOLDER = abs(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

sampleTex = Element("SampleTex", [ShaderType.SAMPLER2D, ShaderType.VEC2], [ShaderType.VEC3], "sample_out", "vec3 PLACEHOLDER = texture(input1, input2).rgb;", ElementType.MAIN_FUNCTION_EXECUTABLE, "texture")

texSize = Element("TexSize", [ShaderType.SAMPLER2D], [ShaderType.VEC2], "size_out", "vec2 PLACEHOLDER = textureSize(input1, 0);", ElementType.MAIN_FUNCTION_EXECUTABLE, "texture")

passthroughFloat = Element("Pass a Float", [], [ShaderType.FLOAT], "pass_out", "float PLACEHOLDER = input1;", ElementType.USER_DEFINED, "util")
passthroughBool = Element("Pass a Bool", [], [ShaderType.BOOL], "pass_out", "bool PLACEHOLDER = input1;", ElementType.USER_DEFINED, "util")
passthroughVec3 = Element("Pass a Vec3", [], [ShaderType.VEC3], "pass_out", "vec3 PLACEHOLDER = input1;", ElementType.USER_DEFINED, "util")

toVec2 = Element("ToVec2", [ShaderType.FLOAT], [ShaderType.VEC2], "to_vec_2", "vec2 PLACEHOLDER = vec2(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "convert")

toVec3 = Element("ToVec3", [ShaderType.FLOAT], [ShaderType.VEC3], "to_vec_3", "vec3 PLACEHOLDER = vec3(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "convert")

toVec4 = Element("ToVec4", [ShaderType.FLOAT], [ShaderType.VEC4], "to_vec_4", "vec4 PLACEHOLDER = vec4(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "convert")

fromVec2 = Element("FromVec2", [ShaderType.FLOAT, ShaderType.VEC2], [ShaderType.FLOAT], "from_vec_2", "float PLACEHOLDER = input2[int(input1)];", ElementType.MAIN_FUNCTION_EXECUTABLE, "extract")

fromVec3 = Element("FromVec3", [ShaderType.FLOAT, ShaderType.VEC3], [ShaderType.FLOAT], "from_vec_3", "float PLACEHOLDER = input2[int(input1)];", ElementType.MAIN_FUNCTION_EXECUTABLE, "extract")

fromVec4 = Element("FromVec4", [ShaderType.FLOAT, ShaderType.VEC4], [ShaderType.FLOAT], "from_vec_4", "float PLACEHOLDER = input2[int(input1)];", ElementType.MAIN_FUNCTION_EXECUTABLE, "extract")

floatToInt = Element("FloatToInt", [ShaderType.FLOAT], [ShaderType.INT], "float_to_int", "int PLACEHOLDER = int(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "convert")

intToFloat = Element("IntToFloat", [ShaderType.INT], [ShaderType.FLOAT], "int_to_float", "float PLACEHOLDER = float(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "convert")

ternaryIf = Element("Ternary", [ShaderType.BOOL, ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "terIf", "PLACEHOLDER = input1 ? input2 : input3;", ElementType.MAIN_FUNCTION_EXECUTABLE, "flow")