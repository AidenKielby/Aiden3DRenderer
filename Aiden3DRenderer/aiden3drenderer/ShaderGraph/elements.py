try:
	from .element import Element, ElementType
	from .shader_type import ShaderType
except ImportError:
	from element import Element, ElementType
	from shader_type import ShaderType



srcImgFunc = f"uniform sampler2D srcTex;"
srcImg = Element("srcTex", [], [ShaderType.SAMPLER2D], "srcTex", srcImgFunc, ElementType.UNIFORM_LAYOUT, "uniform")

destImgFunc = f"imageStore(destTex, pixel_coords, vec4(input1, 1.0));"
destImg = Element("destTex", [ShaderType.VEC3], [], "destTex", destImgFunc, ElementType.OUTPUT_ONLY, "output")

pixelCoordsFunc = f"ivec2 pixel_coords = ivec2(gl_GlobalInvocationID.xy);"
pixelCoords = Element("pixel_coords", [], [ShaderType.VEC2], "pixel_coords", pixelCoordsFunc, ElementType.MAIN_FUNCTION_EXECUTABLE, "coordinate")

getPixelAtFunc = f"vec3 PLACEHOLDER = texelFetch(input1, ivec2(input2), 0).rgb;"
getPixelAt = Element("getPixelAt", [ShaderType.SAMPLER2D, ShaderType.VEC2], [ShaderType.VEC3], "rgb", getPixelAtFunc, ElementType.MAIN_FUNCTION_EXECUTABLE, "texture")

equalsFunc = f"PLACEHOLDER = input1 == input2;"
equals = Element("equals", [ShaderType.ANY, ShaderType.ANY], [ShaderType.BOOL], "equals_out", equalsFunc, ElementType.MAIN_FUNCTION_EXECUTABLE, "comparison")

lessThan = Element("lessThan", [ShaderType.ANY, ShaderType.ANY], [ShaderType.BOOL], "lt_out", "PLACEHOLDER = input1 < input2;", ElementType.MAIN_FUNCTION_EXECUTABLE, "comparison")

greaterThan = Element("greaterThan", [ShaderType.ANY, ShaderType.ANY], [ShaderType.BOOL], "gt_out", "PLACEHOLDER = input1 > input2;", ElementType.MAIN_FUNCTION_EXECUTABLE, "comparison")

select = Element("mix", [ShaderType.ANY, ShaderType.ANY, ShaderType.FLOAT], [ShaderType.ANY], "mix_out", "PLACEHOLDER = mix(input1, input2, input3);", ElementType.MAIN_FUNCTION_EXECUTABLE, "mix")

add = Element("add", [ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "add_out", "PLACEHOLDER = input1 + input2;", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

subtract = Element("subtract", [ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "sub_out", "PLACEHOLDER = input1 - input2;", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

multiply = Element("multiply", [ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "mul_out", "PLACEHOLDER = input1 * input2;", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

divide = Element("divide", [ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "div_out", "PLACEHOLDER = input1 / input2;", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

dotProduct = Element("dot", [ShaderType.VEC3, ShaderType.VEC3], [ShaderType.FLOAT], "dot_out", "vec3 PLACEHOLDER = dot(input1, input2);", ElementType.MAIN_FUNCTION_EXECUTABLE, "vector")

crossProduct = Element("cross", [ShaderType.VEC3, ShaderType.VEC3], [ShaderType.VEC3], "cross_out", "vec3 PLACEHOLDER = cross(input1, input2);", ElementType.MAIN_FUNCTION_EXECUTABLE, "vector")

normalize = Element("normalize", [ShaderType.VEC3], [ShaderType.VEC3], "norm_out", "vec3 PLACEHOLDER = normalize(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "vector")

lengthVec = Element("length", [ShaderType.VEC3], [ShaderType.FLOAT], "len_out", "vec3 PLACEHOLDER = length(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "vector")

minVal = Element("min", [ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "min_out", "PLACEHOLDER = min(input1, input2);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

maxVal = Element("max", [ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "max_out", "PLACEHOLDER = max(input1, input2);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

clamp = Element("clamp", [ShaderType.ANY, ShaderType.ANY, ShaderType.ANY], [ShaderType.ANY], "clamp_out", "PLACEHOLDER = clamp(input1, input2, input3);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

sinNode = Element("sin", [ShaderType.FLOAT], [ShaderType.FLOAT], "sin_out", "float PLACEHOLDER = sin(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

cosNode = Element("cos", [ShaderType.FLOAT], [ShaderType.FLOAT], "cos_out", "float PLACEHOLDER = cos(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

powNode = Element("pow", [ShaderType.FLOAT, ShaderType.FLOAT], [ShaderType.FLOAT], "pow_out", "float PLACEHOLDER = pow(input1, input2);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

absNode = Element("abs", [ShaderType.ANY], [ShaderType.ANY], "abs_out", "PLACEHOLDER = abs(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "math")

sampleTex = Element("sampleTex", [ShaderType.SAMPLER2D, ShaderType.VEC2], [ShaderType.VEC3], "sample_out", "vec3 PLACEHOLDER = texture(input1, input2).rgb;", ElementType.MAIN_FUNCTION_EXECUTABLE, "texture")

texSize = Element("texSize", [ShaderType.SAMPLER2D], [ShaderType.VEC2], "size_out", "vec2 PLACEHOLDER = textureSize(input1, 0);", ElementType.MAIN_FUNCTION_EXECUTABLE, "texture")

passthrough = Element("pass", [], [ShaderType.FLOAT], "pass_out", "float PLACEHOLDER = input1;", ElementType.USER_DEFINED, "utility")

toVec2 = Element("to_vec_2", [ShaderType.FLOAT], [ShaderType.VEC2], "to_vec_2", "vec2 PLACEHOLDER = vec2(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "utility")

toVec3 = Element("to_vec_3", [ShaderType.FLOAT], [ShaderType.VEC3], "to_vec_3", "vec3 PLACEHOLDER = vec3(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "utility")

toVec4 = Element("to_vec_4", [ShaderType.FLOAT], [ShaderType.VEC4], "to_vec_4", "vec4 PLACEHOLDER = vec4(input1);", ElementType.MAIN_FUNCTION_EXECUTABLE, "utility")