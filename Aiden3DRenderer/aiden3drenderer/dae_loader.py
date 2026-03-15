from lxml import etree
import numpy as np

def get_dae(file_path, texture_index, offset=(0,0,0), scale=1):
    tree = etree.parse(file_path)
    root = tree.getroot()
    
    ns = {'c': root.nsmap[None]} if None in root.nsmap else {}
    
    vertices = []
    tex_coords = []
    vertex_faces = []
    texture_faces = []
    scale = max(scale, 0)
    
    geometries = root.xpath('.//c:geometry', namespaces=ns) if ns else root.xpath('.//geometry')
    
    for geom in geometries:
        mesh = geom.xpath('./c:mesh', namespaces=ns) if ns else geom.xpath('./mesh')
        if not mesh:
            continue
        mesh = mesh[0]
        
        source_map = {}
        
        sources = mesh.xpath('.//c:source', namespaces=ns) if ns else mesh.xpath('.//source')
        for source in sources:
            source_id = source.get('id')
            float_array = source.xpath('./c:float_array', namespaces=ns) if ns else source.xpath('./float_array')
            
            if float_array and float_array[0].text:
                data = [float(x) for x in float_array[0].text.split()]
                accessor = source.xpath('.//c:accessor', namespaces=ns) if ns else source.xpath('.//accessor')
                stride = int(accessor[0].get('stride', 3)) if accessor else 3
                source_map[source_id] = (data, stride)
        
        vert_elem = mesh.xpath('./c:vertices', namespaces=ns) if ns else mesh.xpath('./vertices')
        position_source = None
        
        if vert_elem:
            vert_elem = vert_elem[0]
            inputs = vert_elem.xpath('./c:input', namespaces=ns) if ns else vert_elem.xpath('./input')
            for inp in inputs:
                if inp.get('semantic') == 'POSITION':
                    position_source = inp.get('source').lstrip('#')
                    break
        
        if position_source and position_source in source_map:
            pos_data, stride = source_map[position_source]
            for i in range(0, len(pos_data), stride):
                vertices.append([pos_data[i], pos_data[i+1], pos_data[i+2]])
        
        for prim_type in ['triangles', 'polylist', 'polygons']:
            prims = mesh.xpath(f'./c:{prim_type}', namespaces=ns) if ns else mesh.xpath(f'./{prim_type}')
            
            for prim in prims:
                inputs = prim.xpath('./c:input', namespaces=ns) if ns else prim.xpath('./input')
                offset_map = {}
                max_offset = 0
                texcoord_source = None
                
                for inp in inputs:
                    semantic = inp.get('semantic')
                    offset = int(inp.get('offset', 0))
                    max_offset = max(max_offset, offset)
                    
                    if semantic == 'VERTEX':
                        offset_map['VERTEX'] = offset
                    elif semantic == 'TEXCOORD':
                        offset_map['TEXCOORD'] = offset
                        texcoord_source = inp.get('source').lstrip('#')
                
                stride = max_offset + 1
                
                if texcoord_source and texcoord_source in source_map and not tex_coords:
                    uv_data, uv_stride = source_map[texcoord_source]
                    for i in range(0, len(uv_data), uv_stride):
                        tex_coords.append([uv_data[i], uv_data[i+1]])
                
                p_elem = prim.xpath('./c:p', namespaces=ns) if ns else prim.xpath('./p')
                if not p_elem or not p_elem[0].text:
                    continue
                
                indices = [int(x) for x in p_elem[0].text.split()]
                
                if prim_type == 'triangles':
                    for i in range(0, len(indices), stride * 3):
                        v_idx = []
                        t_idx = []
                        
                        for j in range(3):
                            base = i + j * stride
                            if 'VERTEX' in offset_map:
                                v_idx.append(indices[base + offset_map['VERTEX']])
                            if 'TEXCOORD' in offset_map:
                                t_idx.append(indices[base + offset_map['TEXCOORD']])
                        
                        if len(v_idx) == 3:
                            vertex_faces.append(tuple(v_idx))
                            if len(t_idx) == 3:
                                texture_faces.append(tuple(t_idx))
                
                elif prim_type == 'polylist':
                    vcount_elem = prim.xpath('./c:vcount', namespaces=ns) if ns else prim.xpath('./vcount')
                    if not vcount_elem or not vcount_elem[0].text:
                        continue
                    
                    vcounts = [int(x) for x in vcount_elem[0].text.split()]
                    idx = 0
                    
                    for count in vcounts:
                        v_idx = []
                        t_idx = []
                        
                        for j in range(count):
                            base = idx + j * stride
                            if 'VERTEX' in offset_map:
                                v_idx.append(indices[base + offset_map['VERTEX']])
                            if 'TEXCOORD' in offset_map:
                                t_idx.append(indices[base + offset_map['TEXCOORD']])
                        
                        if len(v_idx) == 3:
                            vertex_faces.append(tuple(v_idx))
                            if len(t_idx) == 3:
                                texture_faces.append(tuple(t_idx))
                        elif len(v_idx) > 3:
                            for k in range(1, len(v_idx) - 1):
                                vertex_faces.append((v_idx[0], v_idx[k], v_idx[k+1]))
                                if t_idx:
                                    texture_faces.append((t_idx[0], t_idx[k], t_idx[k+1]))
                        
                        idx += count * stride
    
    if vertices:
        arr = np.array(vertices, dtype=float)
        pivot = (arr.min(axis=0) + arr.max(axis=0)) * 0.5
        vertices = ((arr - pivot) * scale + pivot + offset).tolist()
    
    return [vertices, vertex_faces, tex_coords, texture_faces, False, texture_index]
