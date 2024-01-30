import cv2
import base64

def resize_and_compress_image(input_image_path, target_width, target_height, compression_quality=90):
    # Read the input image
    image = cv2.imread(input_image_path)

    # Resize the image to the target dimensions
    resized_image = cv2.resize(image, (target_width, target_height))

    # Set the compression parameters (for JPEG format)
    compression_params = [int(cv2.IMWRITE_JPEG_QUALITY), compression_quality]

    # Encode the resized and compressed image as JPEG in-memory
    _, encoded_image = cv2.imencode('.jpg', resized_image, compression_params)

    # Convert the encoded image to a base64-encoded string
    base64_encoded_image = base64.b64encode(encoded_image).decode('utf-8')

    return base64_encoded_image

# Example usage:
#input_image_path = 'doorbell/temp_images/file.jpg'
#output_image_path = 'file_resized40_1920_1080.jpg'
#target_width = 1920
#target_height = 1080
#compression_quality = 40  # Adjust as needed (0 to 100, higher means better quality)

#output = resize_and_compress_image(input_image_path, target_width, target_height, compression_quality)
