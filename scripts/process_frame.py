from PIL import Image
import io
import base64

def process_image_from_bytes(img_bytes, quality=70, resolution=(1024, 1024)):
    """
    Process an image by compressing, resizing, and converting it to base64.

    :param img_bytes: Raw bytes of the image
    :param quality: Compression quality (default is 70)
    :param resolution: Target resolution (default is 1024x1024)
    :return: Base64 encoded string of the processed image
    """
    # Open the image from bytes
    img = Image.open(io.BytesIO(img_bytes))

    # Resize the image
    img = img.resize(resolution)

    # Save the image to a BytesIO buffer with specified quality
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)

    # Convert the image buffer to a base64 string
    base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return base64_img

def process_image(img_path, quality=70, resolution=(1024, 1024)):
    """
    Process an image by compressing, resizing, and converting it to base64.

    :param img_path: Path to the image file
    :param quality: Compression quality (default is 70)
    :param resolution: Target resolution (default is 1024x1024)
    :return: Base64 encoded string of the processed image
    """
    # Open the image
    img = Image.open(img_path)

    # Resize the image
    img = img.resize(resolution)

    # Save the image to a BytesIO buffer with specified quality
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)

    # Convert the image buffer to a base64 string
    base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')

    print(len(base64_img))
    return base64_img