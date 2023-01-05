import io
import os
import warnings
from PIL import Image
import openai
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import showImage

stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],
    verbose=True,
)
openai.api_key = os.getenv("OPENAI_API_KEY")

def generatePrompt():
    model = "text-davinci-003"
    prompt = "Generate a prompt to generate an image with maximum of two sentences from the Hitchhikers guide to the galaxy."
    temperature = 1
    max_tokens = 100
    response = openai.Completion.create(model=model, prompt=prompt, temperature=temperature, max_tokens=max_tokens)
    return response.choices[0]['text'].replace('\"','') + " Digital art"
    

answers = stability_api.generate(
    prompt = generatePrompt(),
    steps = 30, # defaults to 30 if not specified
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
            showImage.showFullScreen(img)