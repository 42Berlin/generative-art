import io
import os
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import cv2
import showImage

stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],
    verbose=True,
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)
ret, frame = cap.read()
cropped_frame = frame[:256, int((frame.shape[1] - 512) / 2):int((frame.shape[1] + 512) / 2)]
cv2.imwrite("webcam.png", cropped_frame)
cap.release()

initImg=Image.open("webcam.png")
answers = stability_api.generate(
    prompt = "Van Gogh painting of a woman",
    steps = 50, # defaults to 30 if not specified
    width = 512,
    height = 256,
    init_image=initImg,
    start_schedule=0.4
)

for resp in answers:
    for artifact in resp.artifacts:
        if artifact.finish_reason == generation.FILTER:
            warnings.warn(
                "Your request activated the API's safety filters and could not be processed."
                "Please modify the prompt and try again.")
        if artifact.type == generation.ARTIFACT_IMAGE:
            img = Image.open(io.BytesIO(artifact.binary))
            showImage.showWindow(img)


