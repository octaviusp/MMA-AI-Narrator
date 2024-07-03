from engine.narrator_system import NarratorSystem
from scripts.process_frame import process_image, process_image_from_bytes

import asyncio

if __name__ == "__main__":
    narrator_system = NarratorSystem(testing_only_vision=False)

    while True:
        #img_path = input("- Image fight path: ")
        img_path = "/Users/octaviopavon/Desktop/kick_c.jpg"
        with open(img_path, "rb") as f:
            img_bytes = f.read()
        asyncio.run(narrator_system.execute([process_image_from_bytes(img_bytes)]))
        break