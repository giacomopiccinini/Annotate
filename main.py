import cv2
from Code.Modules.bounding_box import BoundingBoxWidget

if __name__ == '__main__':
    
    # Start bounding box
    boundingbox_widget = BoundingBoxWidget("Input/BoundingBox/real.jpg")
    
    while True:
        cv2.imshow("Annotation", boundingbox_widget.show_image())
        key = cv2.waitKey(1)

        # Close program with keyboard 'q'
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(1)