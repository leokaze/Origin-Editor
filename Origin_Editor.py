bl_info = {
    "name": "Origin Alignement",
    "author": "Leonardo Caceres",
    "version": (1, 0),
    "blender": (2, 70, 0),
    "location": "View3D > Object > ",
    "description": "Modify and align origin object",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

import bpy
#import mathutils
from bpy.props import (
        BoolProperty,
        EnumProperty,
        FloatProperty,
        PointerProperty,
        )
from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        )
from mathutils import Vector

class OriginAlignemetProperties(PropertyGroup):
    zAxis = EnumProperty(
            name="zAxis",
            items=[
                ("pz", "+Z", "", 1),
                ("z", "Z/2", "", 2),
                ("mz", "-Z", "", 3)
                ],
            description="Z axis used to align origin"
            )
    esquina = EnumProperty(
            name = "border",
            items=[
                ("ur", "UR", "", 1),
                ("um", "UM", "", 2),
                ("ul", "UL", "", 3),
                ("mr", "MR", "", 4),
                ("mm", "MM", "", 5),
                ("ml", "ML", "", 6),
                ("br", "BR", "", 7),
                ("bm", "BM", "", 8),
                ("bl", "BL", "", 9)
                ],
            description="point to align origin"
            )
    
#-----------------------------


#------------------------------

def getCorner (obj, corner):
    c = [0.0,0.0,0.0]
    aux = 0
    for i in obj.bound_box[corner]:
        c[aux] = i
        aux += 1
#    print("------------GET CORNER------------")
#    print(c)
    #vec = mathutils.Vector((0.0,0.0,0.0))
    vec = Vector((0.0,0.0,0.0))
    aux = 0
    for i in c:
        #print (i)
        vec[aux] = i * obj.scale[aux]
        aux += 1
    
    return (vec)

def AlignOrigin (obj, props):
    cursor = bpy.context.space_data.cursor_location
    zloc = Vector((0.0,0.0,0.0))
    if props.zAxis == 'z':
        zloc[1]=obj.dimensions.y/2
    elif props.zAxis == 'mz':
        zloc[1]=obj.dimensions.y

    if props.esquina == 'ur':
        cursor = getCorner (obj, 1) + obj.location 
    elif props.esquina == 'um':
        dim = Vector((obj.dimensions.x,0.0,0.0))
        dim[0] = dim[0]/2
        cursor = getCorner(obj,1) + obj.location + dim
    elif props.esquina == 'ul':
        cursor = getCorner (obj, 5) + obj.location
    elif props.esquina == 'mr':
        dim = Vector((0.0,0.0,obj.dimensions.z))
        dim[2]= dim[2]/2
        cursor = getCorner(obj,0) + obj.location + dim
    elif props.esquina == 'mm':
        dim = Vector((obj.dimensions.x/2, 0.0, obj.dimensions.z/2))
        cursor = getCorner(obj, 0)+obj.location+dim
    elif props.esquina == 'ml':
        dim = Vector((0.0,0.0,obj.dimensions.z/2))
        cursor = getCorner(obj, 4) + obj.location + dim
    elif props.esquina == 'br':
        cursor = getCorner(obj, 0) + obj.location
    elif props.esquina == 'bm':
        dim = Vector((obj.dimensions.x/2, 0.0,0.0))
        cursor = getCorner(obj, 0) + obj.location + dim
    elif props.esquina == 'bl':
        cursor = getCorner(obj, 4) + obj.location

    cursor = cursor + zloc
    
    #return (cursor)
    bpy.context.space_data.cursor_location = cursor
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    
    #print (getCorner(obj, 1))


class OriginAlignementOperator(bpy.types.Operator):
    """ToolTip of OriginAlignementOperator"""
    bl_idname = "origin.alignement_operator"
    bl_label = "Origin Alignement Operator"
    bl_options = {'UNDO','REGISTER'}
    
    #posicion = bpy.props.IntProperty()
    
    


    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def execute(self, context):
        #self.report({'INFO'}, "Hello World!")
        #obj = context.active_object
#        objs = []
#        for o in context
        objs = context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')
                
        for obj in objs:
            bpy.data.objects[obj.name].select = True
            bpy.context.scene.objects.active = bpy.data.objects[obj.name]
            pos = AlignOrigin(obj, context.scene.align_origin)
            bpy.data.objects[obj.name].select = False
        
        for obj in objs:
            obj.select = True
            bpy.context.scene.objects.active = obj
        #print (objs)
            
            #bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            
        return {'FINISHED'}
    
    #def invoke(self, context, event):
    #    wm.modal_handler_add(self)
    #    return {'RUNNING_MODAL'}  
    #    return wm.invoke_porps_dialog(self)
    #def modal(self, context, event):
    #def draw(self, context):

class OriginAlignementPanel(bpy.types.Panel):
    """Docstring of OriginAlignementPanel"""
    bl_idname = "VIEW3D_PT_origin_alignement"
    bl_label = "Origin Alignement Panel"
    
#    bl_space_type = 'VIEW_3D'
#    bl_region_type = 'TOOLS'
#    bl_category = 'Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'objectmode'
    bl_category = 'Tools'
    
    #Panels in ImageEditor are using .poll() instead of bl_context.
    #@classmethod
    #def poll(cls, context):
    #    return context.space_data.show_paint
    
    def draw(self, context):
        layout = self.layout
        alignO = context.scene.align_origin
        
        layout.operator(OriginAlignementOperator.bl_idname, text = "Alinear", icon = 'TRIA_RIGHT', )#.posicion=1
        layout.prop(alignO, "zAxis", text="Z axis", expand=True)
        
        layout.prop(alignO, "esquina", text="border align", expand=True)

def register():
    bpy.utils.register_class(OriginAlignementOperator)
    bpy.utils.register_class(OriginAlignementPanel)
    bpy.utils.register_class(OriginAlignemetProperties)
    bpy.types.Scene.align_origin = PointerProperty(type=OriginAlignemetProperties)
    

def unregister():
    bpy.utils.unregister_class(OriginAlignementOperator)
    bpy.utils.unregister_class(OriginAlignementPanel)
    bpy.utils.unregister_class(OriginAlignemetProperties)
    del bpy.types.Scene.align_origin
    
if __name__ == "__main__":
    register()
