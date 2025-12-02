import bpy
import json
import mathutils
import os

ARMATURE_NAME = "Esqueleto"  
JSON_PATH = r"C:\Users\DELL\Documents\BLENDER\animacion.json"  # ruta al JSON
START_FRAME = 1               # se enicia en el frame 1

# cargar el JSON
with open(JSON_PATH, "r") as f:
    data = json.load(f)

frames = data["frames"]
bones_list = data.get("bones", ["LeftUpperArm","LeftLowerArm","RightUpperArm","RightLowerArm"])

# obtener objeto esqueleto
arm_obj = bpy.data.objects[ARMATURE_NAME]
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='POSE')

# asegurar el modo cuaternión en los huesos
for bname in bones_list:
    if bname in arm_obj.pose.bones:
        pbone = arm_obj.pose.bones[bname]
        pbone.rotation_mode = 'QUATERNION'

# aplicar la animación frame por frame
for i, frame_data in enumerate(frames):
    frame_num = START_FRAME + i
    bpy.context.scene.frame_set(frame_num)

    for bname in bones_list:
        if bname not in frame_data:
            continue
        if bname not in arm_obj.pose.bones:
            continue

        w, x, y, z = frame_data[bname]

        # crear cuaternión Blender (w,x,y,z)
        q = mathutils.Quaternion((w, x, y, z))

        pbone = arm_obj.pose.bones[bname]
        pbone.rotation_quaternion = q
        pbone.keyframe_insert(data_path="rotation_quaternion", frame=frame_num)

print(f"Animación aplicada. Total de frames: {len(frames)}")