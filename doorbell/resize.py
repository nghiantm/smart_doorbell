import cv2

def resize_and_compress_image(input_image_path, output_image_path, target_width, target_height, compression_quality=95):
    # Read the input image
    image = cv2.imread(input_image_path)

    y1, x2, y2, x1 = 500, 1244, 1016, 728

    cv2.putText(image, "Nghia",(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 200), 2)
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 200), 4)

    # Resize the image to the target dimensions
    resized_image = cv2.resize(image, (target_width, target_height))

    # Set the compression parameters (for JPEG format)
    compression_params = [int(cv2.IMWRITE_JPEG_QUALITY), compression_quality]

    # Save the resized and compressed image
    cv2.imwrite(output_image_path, resized_image, compression_params)

    #resized_compressed_image = cv2.imread(output_image_path)

    #cv2.putText(resized_compressed_image, "Nghia",(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 200), 2)
    #cv2.rectangle(resized_compressed_image, (x1, y1), (x2, y2), (0, 0, 200), 4)

    #cv2.imwrite(output_image_path, resized_compressed_image)

# Example usage:
input_image_path = 'file.jpg'
output_image_path = 'file_resized40_2.jpg'
target_width = 1920
target_height = 1080
compression_quality = 40  # Adjust as needed (0 to 100, higher means better quality)

resize_and_compress_image(input_image_path, output_image_path, target_width, target_height, compression_quality)
