FROM nvcr.io/nvidia/deepstream:7.1-triton-multiarch

WORKDIR /app

# Copy your DeepStream pipeline code, camera fetch script, and configs
COPY . /app

# Install Python dependencies
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install pymilvus onnxruntime opencv-python requests

# (Optional) Set environment variables
ENV PYTHONUNBUFFERED=1

# Set entrypoint (change as needed)
CMD ["python3", "pipeline.py"]