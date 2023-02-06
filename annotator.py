import cv2
import sys
from glob import glob
from Code.Annotate.bounding_box_widget import BoundingBoxWidget

if __name__ == "__main__":
    # Get image path
    image_directory = sys.argv[1]

    # Get paths to images
    image_paths = (
        glob(image_directory + "/*.jpg")
        + glob(image_directory + "/*.png")
        + glob(image_directory + "/*.jpeg")
    )

    # Loop over all images
    for image_path in image_paths:
        # Start cropping
        widget = BoundingBoxWidget(image_path)

        while True:
            cv2.imshow("BoundingBox", widget.show_image())
            key = cv2.waitKey(1)

            # Move on to next image with keyboard 'n'
            if key == ord("n"):
                cv2.destroyAllWindows()
                break

            # Close program with keyboard 'q'
            if key == ord("q"):
                cv2.destroyAllWindows()
                exit(1)
