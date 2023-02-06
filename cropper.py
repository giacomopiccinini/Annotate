import cv2
import sys
from Code.Crop.crop_widget import CropWidget

if __name__ == "__main__":
    # Get image path
    image_path = sys.argv[1]

    # Start cropping
    widget = CropWidget(image_path)

    while True:
        cv2.imshow("Cropping", widget.show_image())
        key = cv2.waitKey(1)

        # Close program with keyboard 'q'
        if key == ord("q"):
            cv2.destroyAllWindows()
            exit(1)
