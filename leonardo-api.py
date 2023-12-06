import json
import requests

leonardo_api_key = "<YOUR_API_KEY>"
authorization = "Bearer %s" % leonardo_api_key

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}


def generate_real_images():
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    payload = {
        "height": 512,
        "modelId": None,
        "prompt": "An oil painting of a cat",
        "width": 768,
        "alchemy": True,
        "num_images": 1,
        "photoReal": True,
        "presetStyle": "CINEMATIC",
        "photoRealStrength": 0.5
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()['generationId']


generation_id = generate_real_images()
# generation_id = "1c2ba6c1-2bcb-4494-a312-02054a586478"


def get_generated_image(generationid: str):
    url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generationid

    response = requests.get(url, headers=headers)
    generated_images = response.json()['generations_by_pk']['generated_images']
    image_url = []
    for i in range(len(generated_images)):
        image_url.append(generated_images[i]['url'])

    return image_url


images_url = get_generated_image(generation_id)
print(images_url)


def upload_dataset_image(image_file_path: str, response: requests.models.Response) -> requests.models.Response:
    """ 
    Upload an image file to a Leonardo.ai dataset via a presigned URL.

    :image_file_path: Path to an image file to upload
    :response: Response to a request to the datasets/{datasetId}/upload endpoint
    """

    fields = json.loads(response.json()['uploadDatasetImage']['fields'])
    url = response.json()['uploadDatasetImage']['url']
    files = {'file': open(image_file_path, 'rb')}

    return requests.post(url, data=fields, files=files)

