import dearpygui.dearpygui as dpg

from shader_type import ShaderType
from elements import getPixelAt, writePixelAt, equals

connections = {}
node_vars = {}
link_map = {}
node_counter = 0

all_elements = [getPixelAt, writePixelAt, equals]

final_shader = """

"""

shader_before_main = """
#version 430
layout(local_size_x = 16, local_size_y = 16) in;

layout(rgba32f, binding = 0) uniform image2D destTex;
uniform sampler2D srcTex;
"""

shader_inside_main = """
ivec2 pixel_coords = ivec2(gl_GlobalInvocationID.xy);
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

def add_element_node(element):
    global node_counter
    node_counter += 1
    ntag = f"node_{node_counter}"

    with dpg.node(label=element.name, parent="editor", pos=(200, 50 + node_counter * 20)):
        for i, inp in enumerate(element.inputs):
            ptag = f"{ntag}_in_{i}"
            with dpg.node_attribute(tag=ptag, attribute_type=dpg.mvNode_Attr_Input):
                dpg.add_text(inp.value, tag=f"{ptag}_text")

        for i, out in enumerate(element.outputs):
            ptag = f"{ntag}_out_{i}"
            with dpg.node_attribute(tag=ptag, attribute_type=dpg.mvNode_Attr_Output):
                dpg.add_text(out.value, tag=f"{ptag}_text")
        

def on_link(sender, app_data):
    src_text = dpg.get_item_children(app_data[0], slot=1)[0]
    dst_text = dpg.get_item_children(app_data[1], slot=1)[0]
    if str(dpg.get_value(src_text)) == str(dpg.get_value(dst_text)):
        link_tag = dpg.add_node_link(app_data[0], app_data[1], parent="editor")
        src_node = dpg.get_item_parent(app_data[0])
        dst_node = dpg.get_item_parent(app_data[1])
        key = (dpg.get_item_label(src_node), dpg.get_item_label(dst_node))
        connections[key] = dpg.get_value(src_text)
        link_map[link_tag] = key

    print(connections)

def on_delink(sender, app_data):
    dpg.delete_item(app_data)
    key = link_map.pop(app_data, None)
    if key:
        connections.pop(key, None)

    print(connections)

def delete_selected_nodes(sender, app_data):
    selected_nodes = dpg.get_selected_nodes("editor")
    for node in selected_nodes:
        dpg.delete_item(node)
        print(f"Deleted node via hotkey: {node}")

dpg.create_context()

# my better way idea is to have each element have the code/function it aldready has,
# then when we link the things together, each thing (eg "input1") gets replaced with the actuall connection.
# in addition, when the thing is created, the "PLACEHOLDER" gets replaced with a unique name, and this unique name gets added tp the var names list
# the connections dict will change to have the actual varuable names (including type), and it will change from a dict to a list, 
# because i dont see a need for a key-value pair, i just need a list of all the connections, and then i can loop through that list to generate the shader code.
def graph_to_shader():
    global shader_before_main, shader_inside_main
    for key in connections.keys():
        if key[1] == 'getPixelAt':
            shader_inside_main += getPixelAt.function.replace("input1", connections[key][0]).replace("input2", connections[key][1]).replace("PLACEHOLDER", get_unique_name("PLACEHOLDER", taken_variable_names)) + "\n"
        elif key[1] == 'writePixelAt':
            shader_inside_main += writePixelAt.function.replace("input1", connections[key][0]).replace("input2", connections[key][1]).replace("PLACEHOLDER", get_unique_name("PLACEHOLDER", taken_variable_names)) + "\n"
        elif key[1] == 'equals':
            shader_inside_main += equals.function.replace("input1", connections[key][0]).replace("input2", connections[key][1]).replace("PLACEHOLDER", get_unique_name("PLACEHOLDER", taken_variable_names)) + "\n"
    
    final_shader = shader_before_main + "\nvoid main() {\n" + shader_inside_main + "\n}"
    print(final_shader)

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
                print(el)
                dpg.add_button(
                    label=el.name,
                    user_data=el, 
                    callback=lambda s, a, u: add_element_node(u),
                    width=-1
                )
            
        with dpg.handler_registry():
            dpg.add_key_press_handler(key=dpg.mvKey_Delete, callback=delete_selected_nodes)
            dpg.add_key_press_handler(key=dpg.mvKey_Back, callback=delete_selected_nodes)

        # Node editor
        with dpg.node_editor(tag="editor", width=-1, height=-1,
                             callback=on_link, delink_callback=on_delink):

            with dpg.node(label="srcTex", pos=(50, 100)):
                with dpg.node_attribute(tag="out_a", attribute_type=dpg.mvNode_Attr_Output):
                    dpg.add_text(ShaderType.SAMPLER2D.value, tag="out_a_text")

            with dpg.node(label="pixel_coords", pos=(50, 170)):
                with dpg.node_attribute(tag="out_b", attribute_type=dpg.mvNode_Attr_Output):
                    dpg.add_text(ShaderType.VEC2.value, tag="out_b_text")

            with dpg.node(label="destTex", pos=(300, 135)):
                with dpg.node_attribute(tag="in_a", attribute_type=dpg.mvNode_Attr_Input):
                    dpg.add_text(ShaderType.VEC3.value, tag="in_a_text")

dpg.create_viewport(title="Shader Graph", width=900, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("win", True)
dpg.start_dearpygui()
dpg.destroy_context()
