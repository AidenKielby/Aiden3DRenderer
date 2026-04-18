try:
    import dearpygui.dearpygui as dpg
except ImportError:
    dpg = None

import ast
import inspect
import re

# Prefer package-relative imports, but fall back to direct imports when
# the module is run without package context (helps local testing/install mixups).
try:
    from .element import Element, ElementType
    from .shader_type import ShaderType
    from . import elements
except ImportError:
    from element import Element, ElementType
    from shader_type import ShaderType
    import elements

changes = []
connections = []
link_map = {}
node_counter = 3

category_headers = {}

all_elements = [
    obj for name, obj in inspect.getmembers(elements)
    if isinstance(obj, Element) and name not in ["srcTex", "destTex", "pixel_coords"]
]

def get_unique_name(placeholder, taken_names):
    if placeholder not in taken_names:
        return placeholder
    
    counter = 1
    new_name = f"{placeholder}{counter}"
    
    while new_name in taken_names:
        counter += 1
        new_name = f"{placeholder}{counter}"
        
    return new_name

taken_variable_names = ["srcTex", "destTex", "pixel_coords"]

def on_text_update(sender, app_data, user_data):
    node = user_data
    output = app_data

    node_data = dpg.get_item_user_data(node)
    elm: Element = node_data["element"]
    spliten = elm.function.split("=")
    elm.function = "= ".join([spliten[0], output]) + ";"

def add_element_node(element: Element):
    global node_counter
    node_counter += 1
    ntag = f"node_{node_counter}"

    element = Element(element.name, element.inputs, element.outputs, element.variable_name, element.function, element.type, element.category)

    element_function_variable_name = get_unique_name(element.variable_name, taken_variable_names)
    element.name = element_function_variable_name
    taken_variable_names.append(element_function_variable_name)

    element.function = element.function.replace("PLACEHOLDER", element.name)

    with dpg.node(label=element.name, parent="editor", pos=(200, 50 + node_counter * 20), user_data={"element":element, "conections":[], "index": node_counter-1}) as node:
        if element.type == ElementType.USER_DEFINED:
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                dpg.add_input_text(
                    label="Value",
                    callback=on_text_update,
                    user_data=node,
                    width=50
                )
        for i, inp in enumerate(element.inputs):
            ptag = f"{ntag}_in_{i}"
            with dpg.node_attribute(
                tag=ptag,
                attribute_type=dpg.mvNode_Attr_Input,
                user_data={"kind": "input", "index": i}
            ):
                dpg.add_text(inp.value)

        for i, out in enumerate(element.outputs):
            ptag = f"{ntag}_out_{i}"
            with dpg.node_attribute(
                tag=ptag,
                attribute_type=dpg.mvNode_Attr_Output,
                user_data={"kind": "output", "index": i}
            ):
                dpg.add_text(out.value)

def on_link(sender, app_data, user_data):
    src_attr = app_data[0]
    dst_attr = app_data[1]

    src_node = dpg.get_item_parent(src_attr)
    dst_node = dpg.get_item_parent(dst_attr)
    src_attr_data = dpg.get_item_user_data(src_attr)
    dst_attr_data = dpg.get_item_user_data(dst_attr)

    src_children = dpg.get_item_children(src_attr, 1)
    dst_children = dpg.get_item_children(dst_attr, 1)

    if not src_children or not dst_children:
        return

    src_text_item = src_children[0]
    dst_text_item = dst_children[0]

    src_text = dpg.get_value(src_text_item)
    dst_text = dpg.get_value(dst_text_item)

    src_node_data = dpg.get_item_user_data(src_node)
    dst_node_data = dpg.get_item_user_data(dst_node)

    dst_index = dst_attr_data["index"]

    if src_text == dst_text or src_text == "any" or dst_text == "any":
        link_tag = dpg.add_node_link(app_data[0], app_data[1], parent="editor")
        
        dst_elm: Element = dst_node_data["element"]
        src_elm: Element = src_node_data["element"]

        if src_elm.outputs[0] == ShaderType.ANY:
            new_func = dst_elm.inputs[dst_index].value + " " + src_elm.function

            new_inp = []
            for i in range(len(src_elm.inputs)):
                new_inp.append(dst_elm.inputs[dst_index])

            src_elm = Element(src_elm.name, new_inp, [new_inp[0]], src_elm.variable_name, new_func, src_elm.type, src_elm.category)
            src_node_data["element"] = src_elm

            for inp_attr in dpg.get_item_children(src_node, 1):
                text_children = dpg.get_item_children(inp_attr, 1)

                if not text_children:
                    continue

                text_item = text_children[0]

                dpg.set_value(text_item, dst_elm.inputs[dst_index].value)
        
        if dst_elm.inputs[dst_index] == ShaderType.ANY:
            new_func = src_elm.outputs[0].value + " " + dst_elm.function

            new_inp = []
            for i in range(len(dst_elm.inputs)):
                new_inp.append(src_elm.outputs[0])

            dst_elm = Element(dst_elm.name, new_inp, [new_inp[0]], dst_elm.variable_name, new_func, dst_elm.type, dst_elm.category)
            dst_node_data["element"] = dst_elm
            
            for inp_attr in dpg.get_item_children(dst_node, 1):
                text_children = dpg.get_item_children(inp_attr, 1)

                if not text_children:
                    continue

                text_item = text_children[0]

                dpg.set_value(text_item, src_elm.outputs[0].value)
        
        new_func = src_elm.function.replace("uniform ", "").replace(";", "")
        src_variable_name = new_func.split(" ")[1]
        dst_function = dst_elm.function

        dst_function1 = dst_function.replace(f"input{dst_index+1}", src_variable_name)

        changes.append([dst_function, dst_function1, dst_elm])
        connections.append({
            "src_node": src_node,
            "dst_node": dst_node,
            "src_index": src_node_data["index"],
            "dst_index": dst_node_data["index"]
        })
        link_map[link_tag] = len(changes)-1

        dst_elm.function = dst_function1


def cleanup_link(link_tag, remove_visual=True):
    idx = link_map.pop(link_tag, None)
    if idx is None:
        return
    change = changes[idx]
    elm: Element = change[2]
    elm.function = change[0]
    del changes[idx]
    del connections[idx]
    # rebuild link_map values safely (avoid mutating while iterating)
    new_map = {}
    for lt, old_idx in link_map.items():
        new_map[lt] = old_idx - 1 if old_idx > idx else old_idx
    link_map.clear()
    link_map.update(new_map)
    if remove_visual:
        try:
            dpg.delete_item(link_tag)
        except Exception:
            pass

def on_delink(sender, app_data):
    cleanup_link(app_data)

def delete_selected_nodes(sender, app_data):
    selected_nodes = dpg.get_selected_nodes("editor")
    for node in selected_nodes:
        links_to_remove = [
            lt for lt, idx in list(link_map.items())
            if connections[idx]["src_node"] == node or connections[idx]["dst_node"] == node
        ]
        for lt in links_to_remove:
            cleanup_link(lt, remove_visual=True)
        dpg.delete_item(node)

def get_backward_neighbors(node):
    return [
        c["src_node"]
        for c in connections
        if c["dst_node"] == node
    ]

def get_correct_ordering():
    ordered_list = []
    queue = []
    for node in dpg.get_item_children("editor", 1):
        data = dpg.get_item_user_data(node)
        
        if data is None:
            continue
        
        element: Element = data["element"]
        if element.type == ElementType.OUTPUT_ONLY:
            queue.append(node)

    while len(queue) > 0:
        node = queue[0]
        neighbors = get_backward_neighbors(node)
        for n in neighbors:
            queue.append(n)
        
        elm = dpg.get_item_user_data(node)["element"]
        if elm in ordered_list:
            ordered_list.remove(elm)
        ordered_list.insert(0, elm)

        del queue[0]
    
    return ordered_list

def graph_to_shader():

    ordered_list = get_correct_ordering()

    shader_before = """#version 430
layout(local_size_x = 16, local_size_y = 16) in;

layout(rgba32f, binding = 0) uniform image2D destTex;
"""
    shader_inside = ""

    for elm in ordered_list:
        src_elm: Element = elm
        if src_elm.type == ElementType.MAIN_FUNCTION_EXECUTABLE or src_elm.type == ElementType.OUTPUT_ONLY or src_elm.type == ElementType.USER_DEFINED:
            shader_inside += src_elm.function + "\n"
        else:
            shader_before += src_elm.function + "\n"
    
    final_shader = shader_before + "\nvoid main() {\n" + shader_inside + "\n}"
    final_shader1 = final_shader
    final_shader = ""
    return final_shader1

# this func is not mine 
def find_last_import_line(filepath):
    with open(filepath, "r") as f:
        tree = ast.parse(f.read())

    last_line = None

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            last_line = node.lineno

    return last_line

# this func is not mine 
def insert_line(filepath, line_number, new_text):
    with open(filepath, "r") as f:
        lines = f.readlines()

    index = line_number

    if index > len(lines):
        index = len(lines) 

    lines.insert(index, new_text + "\n")

    with open(filepath, "w") as f:
        f.writelines(lines)

def export_shader():
    path = dpg.get_value("file_path_input")
    name = dpg.get_value("shader_name_input").strip() or "shader"

    shader_output = graph_to_shader()  

    with open(path, 'r') as file:
        content = file.read()

    pattern = rf'({name}\s*=\s*)(["\']{{3}})(.*?)(\2)'

    def replacer(match):
        prefix = match.group(1)
        quote = match.group(2)
        return f"{prefix}{quote}{shader_output}{quote}"

    new_content, count = re.subn(pattern, replacer, content, flags=re.DOTALL)

    if count == 0:
        num = find_last_import_line(path)
        if num is None:
            num = 0
        insert_line(path, num, f'{name} = """{shader_output}"""')
    else:
        with open(path, 'w') as file:
            file.write(new_content)

def custom_uniform():
    unifrom_name = dpg.get_value("custom_uniform_name")
    unifrom_dtype = dpg.get_value("custom_uniform_dtype")
    users_uniform = Element(unifrom_name, [], [ShaderType.from_str(unifrom_dtype)], unifrom_name, f"uniform {unifrom_dtype} {unifrom_name};", ElementType.UNIFORM_LAYOUT, "uniform")

    all_elements.append(users_uniform)
    if users_uniform.category not in category_headers:
        category_headers[users_uniform.category] = dpg.add_collapsing_header(
            label=users_uniform.category,
            default_open=False,
            parent="sidebar"
        )

    dpg.add_button(
        label=users_uniform.name,
        user_data=users_uniform,
        callback=lambda s, a, u: add_element_node(u),
        parent=category_headers[users_uniform.category],
        width=-1
    )

def build_ui():
    with dpg.window(tag="win"):
        with dpg.group(horizontal=True):
            
            # Sidebar
            with dpg.child_window(tag="sidebar", width=150, height=-1):
                dpg.add_text("Done?")
                dpg.add_separator()
                btn = dpg.add_button(label="Export Shader")
                custom_uniform_btn = dpg.add_button(label="Custom Uniform")
                
                dpg.add_spacing(count = 3)

                dpg.add_text("Elements")
                dpg.add_separator()
                
                for el in all_elements:

                    # create category if it doesn't exist
                    if el.category not in category_headers:
                        category_headers[el.category] = dpg.add_collapsing_header(
                            label=el.category,
                            default_open=False,
                            parent="sidebar"
                        )

                    # add button inside that category
                    dpg.add_button(
                        label=el.name,
                        user_data=el,
                        callback=lambda s, a, u: add_element_node(u),
                        parent=category_headers[el.category],
                        width=-1
                    )
                
            with dpg.popup(btn, mousebutton=dpg.mvMouseButton_Left):
                dpg.add_text("Export Shader")
                dpg.add_input_text(label="Shader Name", tag="shader_name_input")
                dpg.add_input_text(label="File Path", tag="file_path_input")
                dpg.add_button(label="Export", callback=export_shader)

            with dpg.popup(custom_uniform_btn, mousebutton=dpg.mvMouseButton_Left):
                dpg.add_text("Custom Uniform")
                dpg.add_input_text(label="Name", tag="custom_uniform_name")
                dpg.add_combo(
                    items=[
                        ShaderType.FLOAT.value,
                        ShaderType.INT.value,
                        ShaderType.BOOL.value,
                        ShaderType.VEC2.value,
                        ShaderType.VEC3.value,
                        ShaderType.VEC4.value,
                        ShaderType.MAT2.value,
                        ShaderType.MAT3.value,
                        ShaderType.MAT4.value,
                        ShaderType.SAMPLER2D.value,
                    ],
                    label="Type",
                    tag="custom_uniform_dtype",
                    default_value=ShaderType.FLOAT.value,
                )
                dpg.add_button(label="Add", callback=custom_uniform)

            with dpg.handler_registry():
                dpg.add_key_press_handler(key=dpg.mvKey_Delete, callback=delete_selected_nodes)
                dpg.add_key_press_handler(key=dpg.mvKey_Back, callback=delete_selected_nodes)

            # Node editor
            with dpg.node_editor(tag="editor", width=-1, height=-1,
                                callback=on_link, delink_callback=on_delink):

                with dpg.node(label="srcTex", pos=(50, 100), user_data={"element":elements.srcImg, "connections":[], "index": 0}):
                    with dpg.node_attribute(tag="out_a", attribute_type=dpg.mvNode_Attr_Output):
                        dpg.add_text(ShaderType.SAMPLER2D.value, tag="out_a_text")

                with dpg.node(label="pixel_coords", pos=(50, 170), user_data={"element":elements.pixelCoords, "connections":[], "index": 1}):
                    with dpg.node_attribute(tag="out_b", attribute_type=dpg.mvNode_Attr_Output):
                        dpg.add_text(ShaderType.VEC2.value, tag="out_b_text")

                with dpg.node(label="destTex", pos=(300, 135), user_data={"element":elements.destImg, "connections":[], "index": 2}):
                    with dpg.node_attribute(tag="in_a", attribute_type=dpg.mvNode_Attr_Input, user_data={"kind": "input", "index": 0}):
                        dpg.add_text(ShaderType.VEC3.value, tag="in_a_text")

def run():
    if dpg is None:
        raise RuntimeError("DearPyGui is not installed. Install with: pip install 'aiden3drenderer[shadergraph]'")
    dpg.create_context()
    build_ui()
    dpg.create_viewport(title="Shader Graph", width=900, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("win", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    run()
