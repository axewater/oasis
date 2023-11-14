import requests
r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': 'close up of donald trump',
        'grid_size': '1',
    },

    headers={'api-key': 'bcb6f9a6-287b-4599-9701-4f42596a2c1b'}
)
print(r.json())