import os
import boto3
import wget
import json
import sys
import numpy as np
from cv2 import imread, resize, IMREAD_GRAYSCALE


stack_name = sys.argv[1]
commit_id = sys.argv[2]
endpoint_name = f"{stack_name}-{commit_id[:7]}"

runtime = boto3.client("runtime.sagemaker")

#IMAGE_URL = "https://aws-mlops-samples.s3-eu-west-1.amazonaws.com/mnist_output_10.png"
IMAGE_URL = "https://mlopsworkshoptest.s3.ap-southeast-2.amazonaws.com/img_10.jpg"
test_file = "test.jpg"
wget.download(
    IMAGE_URL,
    test_file,
)

image = imread(test_file, IMREAD_GRAYSCALE)
image = resize(image, (28, 28))
image = image.astype("float32")
image = image.reshape(1, 1, 28, 28)

payload = json.dumps(image.tolist())
response = runtime.invoke_endpoint(
    EndpointName=endpoint_name, Body=payload, ContentType="application/json"
)

result = response["Body"].read()
result = json.loads(result.decode("utf-8"))
print(f"Probabilities: {result}")

np_result = np.asarray(result)
prediction = np_result.argmax(axis=1)[0]
print(f"This is your number: {prediction}")

if prediction != 5:
    print("Model prediction failed.")
    sys.exit(1)

if os.path.exists(test_file):
    os.remove(test_file)
else:
    print("The file does not exist")
