import json
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import pyds
import numpy as np
import ctypes
from pymilvus import connections, Collection

Gst.init(None)
from pymilvus import connections

import requests
from datetime import datetime
import base64
import cv2


connections.connect("default", host="192.168.0.141", port="19530")
collection = Collection("students")
print("Connected to Milvus!")
BACKEND_URL = "http://192.168.0.141:8000"  # Replace with your backend host/IP
JWT_TOKEN ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbjEiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NTQyMDg0NjZ9.9gXb4dmUrS7uq9G4ZPn7Rq9kU19bZ4tN8Nn6RdFrcYg"  # Load from config or env for production

index_to_cam = {}
cam_to_index = {}
camera_info_map = {}

def send_attendance_event(student_id, camera_id, status):
    data = {
        "student_id": student_id,
        "camera_id": camera_id,
        "status": status,  # "entry" or "exit"
        "timestamp": datetime.now().isoformat()
    }
    try:
        res = requests.post(
            f"{BACKEND_URL}/attendance/mark",
            json=data,
            headers={"Authorization": f"Bearer {JWT_TOKEN}"}
        )
        print("Attendance event sent:", res.status_code, res.text)
    except Exception as e:
        print("Failed to send attendance event:", e)

def send_unknown_face(face_crop, camera_id):
    _, buffer = cv2.imencode('.jpg', face_crop)
    face_base64 = base64.b64encode(buffer).decode('utf-8')
    data = {
        "camera_id": camera_id,
        "timestamp": datetime.now().isoformat(),
        "face_crop": face_base64
    }
    try:
        res = requests.post(
            f"{BACKEND_URL}/unknown-faces/",
            json=data,
            headers={"Authorization": f"Bearer {JWT_TOKEN}"}
        )
        print("Unknown face event sent:", res.status_code, res.text)
    except Exception as e:
        print("Failed to send unknown face event:", e)
        

def search_embedding(embedding, threshold=1.0):
    try:
        collection.load()
    except Exception as e:
        print(f"[Milvus] Error loading collection: {e}")
        return None
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    try:
        results = collection.search(
            [embedding], "embedding", search_params, limit=1, output_fields=["student_id"]
        )
        if results and results[0].distances[0] < threshold:
            return results[0].ids[0]
    except Exception as e:
        print(f"[Milvus] Search error: {e}")
    return None

def load_camera_configs(config_path="/app/cameras.json"):
    with open(config_path, "r") as f:
        cameras = json.load(f)
    return cameras

def process_frame(gst_buffer, frame_meta):
    frames = pyds.get_nvds_buf_surface(hash(gst_buffer), frame_meta.batch_id)
    return np.array(frames, copy=False, order='C')

def get_face_crop_from_frame(frame, obj_meta, frame_width, frame_height):
    """
    frame: numpy array (H, W, 3) in BGR or RGB (as returned by get_nvds_buf_surface)
    obj_meta: DeepStream object meta
    frame_width, frame_height: dimensions of the frame
    Returns: cropped face as numpy array
    """
    left = max(int(obj_meta.rect_params.left), 0)
    top = max(int(obj_meta.rect_params.top), 0)
    width = int(obj_meta.rect_params.width)
    height = int(obj_meta.rect_params.height)
    right = min(left + width, frame_width)
    bottom = min(top + height, frame_height)
    face_crop = frame[top:bottom, left:right]
    return face_crop

def on_new_sample(_, info, user_data=0):
    gst_buffer = info.get_buffer()
    if not gst_buffer:
        sys.stderr.write("Unable to get GstBuffer\n")
        return
    batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    l_frame = batch_meta.frame_meta_list
    while l_frame is not None:
        try:
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
            print("Frame number ", frame_meta.frame_num, frame_meta.source_id)
            camera_id = index_to_cam.get(frame_meta.source_id)
            camera_info = camera_info_map.get(camera_id, {})
            status = camera_info.get("type", "entry")  # "entry" or "exit"
            l_obj = frame_meta.obj_meta_list
            while l_obj is not None:
                obj_meta = pyds.NvDsObjectMeta.cast(l_obj.data)
                l_user_meta = obj_meta.obj_user_meta_list
                while l_user_meta:
                    user_meta_class = pyds.NvDsUserMeta.cast(l_user_meta.data)
                    if user_meta_class.base_meta.meta_type == pyds.NvDsMetaType.NVDSINFER_TENSOR_OUTPUT_META:
                        tensor_meta = pyds.NvDsInferTensorMeta.cast(user_meta_class.user_meta_data)
                        for i in range(tensor_meta.num_output_layers):
                            layer = pyds.get_nvds_LayerInfo(tensor_meta, i)
                            ptr = ctypes.cast(pyds.get_ptr(layer.buffer), ctypes.POINTER(ctypes.c_float))                            
                            embedding = np.array(np.ctypeslib.as_array(ptr, shape=(layer.dims.numElements,)), copy=True)
                            embedding = embedding / np.linalg.norm(embedding)
                            student_id = search_embedding(embedding)
                            if student_id:
                                print("Matched student:", student_id)
                                send_attendance_event(
                                    student_id=student_id,
                                    camera_id=camera_id,
                                    status=status  # or "exit", based on your logic
                                )
                            else:
                                print("No match found")
                                frame = process_frame(gst_buffer, frame_meta)
                                face_crop = get_face_crop_from_frame(frame, obj_meta,frame_width=1920,frame_height=1080)
                                send_unknown_face(face_crop, camera_id)
                    l_user_meta = l_user_meta.next
                l_obj = l_obj.next
            l_frame = l_frame.next
        except Exception as e:
            print(f"[ERROR] Metadata probe failed: {e}")
            break
    return Gst.PadProbeReturn.OK

def set_callbacks(pipeline):
    try:
        nvosd = pipeline.get_by_name("sink")
        pad = nvosd.get_static_pad("sink")
        pad.add_probe(Gst.PadProbeType.BUFFER, on_new_sample, 0)
    except Exception as e:
        print(e)

def build_pipeline_str(cameras):
    pipeline_str = ''
    for idx, cam in enumerate(cameras):
        pipeline_str += (
            f'nvurisrcbin uri={cam["rtsp_url"]} latency=100 num-extra-surfaces=1 gpu-id=0 '
            f'rtsp-reconnect-interval=180 cudadec-memtype=0 ! m.sink_{idx} '
        )
    batch_size = len(cameras)
    pipeline_str += (
        f'nvstreammux name=m live-source=1 batch-size={batch_size} width=1920 height=1080 batched-push-timeout=250 '
        '! nvvideoconvert '
        '! nvinfer config-file-path=/opt/nvidia/deepstream/deepstream-7.1/faceRecognition/models/face/face.txt '
        '! nvtracker ll-lib-file=/opt/nvidia/deepstream/deepstream-7.1/lib/libnvds_nvmultiobjecttracker.so '
        'll-config-file=/opt/nvidia/deepstream/deepstream-7.1/samples/configs/deepstream-app/config_tracker_NvDCF_perf.yml '
        'tracker-width=512 tracker-height=512 '
        '! nvinfer config-file-path=/opt/nvidia/deepstream/deepstream-7.1/faceRecognition/models/faceEmbeddings/faceEmbeddings.txt '
        '! nvmultistreamtiler width=1920 height=1080 '
        '! nvvideoconvert '
        '! nvdsosd name=nvdsosd display-text=1 '
        '! nveglglessink name=sink'  # Use fakesink for headless, or nveglglessink for display
    )
    return pipeline_str

def main():
    global index_to_cam, cam_to_index,camera_info_map
    cameras = load_camera_configs("/opt/nvidia/deepstream/deepstream-7.1/faceRecognition/app/cameras.json")
    camera_ids = [cam["id"] for cam in cameras]
    # Initialize the mappings
    index_to_cam = {i: cam["id"] for i, cam in enumerate(cameras)}
    cam_to_index = {cam["id"]: i for i, cam in enumerate(cameras)}
    camera_info_map = {cam["id"]: cam for cam in cameras}
    pipeline_str = build_pipeline_str(cameras)
    print("gst-launch-1.0 " + pipeline_str)
    pipeline = Gst.parse_launch(pipeline_str)
    set_callbacks(pipeline)
    pipeline.set_state(Gst.State.PLAYING)
    loop = GObject.MainLoop()
    try:
        loop.run()
    except Exception as e:
        pipeline.set_state(Gst.State.NULL)
        print("Pipeline error:", e)
        pass

if __name__ == "__main__":
    main()