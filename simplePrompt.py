import io
import os
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import showImage

stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],
    verbose=True,
)
answers = stability_api.generate(
    prompt = "Spaceship painted by Vincent Van Gogh",
    steps = 50, # defaults to 30 if not specified
    width = 512,
    height = 256
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