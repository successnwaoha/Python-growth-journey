from PIL import Image, ImageFilter
import os

def open_image(path):
    """Open an image file."""
    return Image.open(path)


def save_image(image, output_path):
    """Save image to output path."""
    image.save(output_path)


def resize_image(image, width, height):
    return image.resize((width, height))


def rotate_image(image, angle):
    return image.rotate(angle, expand=True)


def grayscale_image(image):
    return image.convert("L")


def blur_image(image, radius=2):
    return image.filter(ImageFilter.GaussianBlur(radius))

def crop_image(image, left, top, right, bottom):
    """
    Crops the image. 
    Coordinates: (0,0) is top-left.
    """
    return image.crop((left, top, right, bottom))

def get_all_images(directory):
    """
    Filters a directory to find only image files.
    """
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    return [f for f in os.listdir(directory) if f.lower().endswith(valid_extensions)]