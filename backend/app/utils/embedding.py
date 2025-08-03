import cv2
import numpy as np
import onnxruntime as ort
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")  # or your Milvus host

collection_name = "students"
embedding_dim = 3309  # Use your model's output dimension

# if collection_name in utility.list_collections():
#     Collection(collection_name).drop()

# Create collection if not exists
if collection_name not in utility.list_collections():
    fields = [
        FieldSchema(name="student_id", dtype=DataType.VARCHAR, max_length=64, is_primary=True, auto_id=False),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=embedding_dim)
    ]
    schema = CollectionSchema(fields, description="Student face embeddings")
    collection = Collection(collection_name, schema=schema)
    print(f"Created Milvus collection: {collection_name}")
else:
    collection = Collection(collection_name)
    print(f"Milvus collection '{collection_name}' already exists.")

# Create index if not exists
if not collection.has_index():
    print("Creating index on 'embedding' field...")
    collection.create_index(
        field_name="embedding",
        index_params={
            "index_type": "IVF_FLAT",  # or "IVF_SQ8", "HNSW", etc.
            "metric_type": "L2",
            "params": {"nlist": 128}
        }
    )
    print("Index created.")

# Always load the collection before search
collection.load()

# Load ONNX model once
ONNX_PATH = "/home/debjit/Videos/debjit_project/face_attendence/Student_attendence_managment/models/1k3d68.onnx"
sess = ort.InferenceSession(ONNX_PATH, providers=["CPUExecutionProvider"])

def generate_embedding(photo_path: str) -> np.ndarray:
    img = cv2.imread(photo_path)
    if img is None:
        raise ValueError(f"Failed to load image: {photo_path}")
    H, W = 192, 192  # Use your model's input size
    img = cv2.resize(img, (W, H))
    arr = (img.astype(np.float32) - 127.5) / 128.0
    arr = arr.transpose(2, 0, 1)[None]  # (1, 3, H, W)
    input_name = sess.get_inputs()[0].name
    embedding = sess.run(None, {input_name: arr})[0][0]
    embedding = embedding / np.linalg.norm(embedding)
    return embedding

def insert_embedding_to_milvus(student_id: str, embedding: np.ndarray):
    collection.insert([[student_id], [embedding.tolist()]])
    print(f"Inserted embedding for {student_id} into Milvus.")