import dearpygui.dearpygui as dpg

from shader_type import ShaderType
from elements import getPixelAt, writePixelAt, equals

connections = {}
link_map = {}
node_counter = 0

all_elements = [getPixelAt, writePixelAt, equals]

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

def graph_to_shader():
    print("in progress")

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

            with dpg.node(label="Source Image", pos=(50, 100)):
                with dpg.node_attribute(tag="out_a", attribute_type=dpg.mvNode_Attr_Output):
                    dpg.add_text(ShaderType.SAMPLER2D.value, tag="out_a_text")

            with dpg.node(label="Pixel Pos", pos=(50, 170)):
                with dpg.node_attribute(tag="out_b", attribute_type=dpg.mvNode_Attr_Output):
                    dpg.add_text(ShaderType.VEC2.value, tag="out_b_text")

            with dpg.node(label="Output", pos=(300, 135)):
                with dpg.node_attribute(tag="in_a", attribute_type=dpg.mvNode_Attr_Input):
                    dpg.add_text(ShaderType.VEC3.value, tag="in_a_text")

dpg.create_viewport(title="Shader Graph", width=900, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("win", True)
dpg.start_dearpygui()
dpg.destroy_context()