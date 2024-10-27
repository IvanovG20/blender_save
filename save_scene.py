import bpy
import os
import requests
from datetime import datetime


class SaveSendOperator(bpy.types.Operator):
    bl_idname = 'scene.save_send'
    bl_label = 'Save Scene and  Send Data'
    
    
    def execute(self, context):
        file_path = bpy.data.filepath
        if not file_path:
            file_path = bpy.path.abspath('//untitled.blend')
            bpy.ops.wm.save_as_mainfile(filepath=file_path)
        else:
            bpy.ops.wm.save_mainfile()
            
        user_name = os.getlogin()
        
        save_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        data = {
            'username': user_name,
            'save_time': save_time,
            'file_path': file_path,
        }
        url = "http://bybybyby.ddns.net/api/scene/"
        
        try:
            response = requests.post(url, data=data)
            
            if response.status_code == 201:
                self.report({'INFO'}, 'Сцена и данные сохранены!')
            else:
                self.report(
                    {'ERROR'},
                    f'Ошибка сохранения данных. Статус кода: {response.status_code}'
                )
        except Exception as err:
            self.report({'ERROR'}, f'Ошибка сохранения данных: {str(err)}')
        
        return {'FINISHED'}


class SaveSendPanel(bpy.types.Panel):
    bl_label = 'Save Send Panel'
    bl_idname = 'PT_SaveSend'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Save Panel'
    
    def draw(self, context):
        layout = self.layout
        layout.operator('scene.save_send')
        
classes = [
    SaveSendOperator, SaveSendPanel,
]
    
        
def register():
    for cl in classes:
        bpy.utils.register_class(cl)
    
def unregister():
    for cl in classes:
        bpy.utils.unregister_class(cl)
    
    
if __name__ == '__main__':
    register()