try:
    import dearpygui.dearpygui as dpg
except ImportError:
    dpg = None

import inspect

# Prefer package-relative imports, but fall back to direct imports when
# the module is run without package context (helps local testing/install mixups).
try:
    from .element import Element, ElementType
    from .shader_type import ShaderType
    from . import elements
except Exception:
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

final_shader = """

"""

shader_before_main = """
#version 430
layout(local_size_x = 16, local_size_y = 16) in;

layout(rgba32f, binding = 0) uniform image2D destTex;
"""

shader_inside_main = """
"""

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

def add_element_node(element: Element):
    global node_counter
    node_counter += 1
    ntag = f"node_{node_counter}"

    element_function_variable_name = get_unique_name(element.variable_name, taken_variable_names)
    element.function = element.function.replace("PLACEHOLDER", element_function_variable_name)

    with dpg.node(label=element.name, parent="editor", pos=(200, 50 + node_counter * 20), user_data={"element":element, "conections":[], "index": node_counter-1}):
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

    if str(src_text == dst_text):
        link_tag = dpg.add_node_link(app_data[0], app_data[1], parent="editor")
        src_node = dpg.get_item_parent(app_data[0])
        dst_node = dpg.get_item_parent(app_data[1])
        
        dst_elm: Element = dst_node_data["element"]
        src_elm: Element = src_node_data["element"]
        
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


def on_delink(sender, app_data):
    dpg.delete_item(app_data)
    key = link_map.pop(app_data, None)
    if key:
        change = changes[key]
        elm: Element = change[2]
        elm.function = change[0]
        # delete old connections and changes
        

def delete_selected_nodes(sender, app_data):
    selected_nodes = dpg.get_selected_nodes("editor")
    for node in selected_nodes:
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
        
        ordered_list.insert(0, dpg.get_item_user_data(node)["element"])

        del queue[0]
    
    return ordered_list

def graph_to_shader():
    global shader_before_main, shader_inside_main

    ordered_list = get_correct_ordering()

    for elm in ordered_list:
        src_elm: Element = elm
        if src_elm.type == ElementType.MAIN_FUNCTION_EXECUTABLE or src_elm.type == ElementType.OUTPUT_ONLY:
            shader_inside_main += src_elm.function + "\n"
        else:
            shader_before_main += src_elm.function + "\n"
    
    final_shader = shader_before_main + "\nvoid main() {\n" + shader_inside_main + "\n}"
    print(final_shader)


def build_ui():
    with dpg.window(tag="win"):
        with dpg.group(horizontal=True):
            
            # Sidebar
            with dpg.child_window(tag="sidebar", width=150, height=-1):
                dpg.add_text("Done?")
                dpg.add_separator()
                dpg.add_button(label="Make Shader Code", callback=graph_to_shader)
                
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