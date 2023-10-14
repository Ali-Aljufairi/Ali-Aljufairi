from typing import List
from PIL import Image
import imageio
import numpy as np
import os 

class GifBackgroundRemover:
    def __init__(self, input_path: str, output_path: str, skip_frames: int = 0):
        self.input_path = input_path
        self.output_path = output_path
        self.skip_frames = skip_frames

    def remove_white_background(self):
        images = self.load_gif(self.input_path)
        processed_images = [self.remove_background(image) for image in images[self.skip_frames:]]
        self.save_gif(self.output_path, processed_images)

    def load_gif(self, file_path: str) -> List[Image.Image]:
        gif = imageio.get_reader(file_path)
        images = [Image.fromarray(frame) for frame in gif]
        return images

    def remove_background(self, image: Image.Image) -> Image.Image:
        img = self.make_transparent_background(image)
        return img

    def make_transparent_background(self, img: Image.Image) -> Image.Image:
        img = img.convert("RGBA")
        data = np.array(img)
        r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]

        mask = (r == 255) & (g == 255) & (b == 255)
        a[mask] = 0

        return Image.fromarray(data)

    def save_gif(self, file_path: str, images: List[Image.Image]):
        images[0].save(
            file_path,
            save_all=True,
            append_images=images[1:],
            loop=0,
            duration=100,  # Set a fixed duration for all frames (in milliseconds)
        )

if __name__ == "__main__":
    input_path = "dist/ocean.gif"
    print("Absolute input path:", os.path.abspath(input_path))

    output_path = "dist/oceantb.gif"
    skip_frames = 5  # Number of frames to skip at the beginning

    gif_remover = GifBackgroundRemover(input_path, output_path, skip_frames)
    gif_remover.remove_white_background()

