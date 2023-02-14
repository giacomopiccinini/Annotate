import cv2
from pathlib import Path


class BoundingBoxWidget(object):

    """Class for cropping images"""

    def __init__(self, image_path: str):
        # Convert path to path object
        path = Path(image_path)

        # Extract image, name and extension
        self.image = cv2.imread(image_path)
        self.name = path.stem
        self.extension = path.suffix

        # Get width and height of image
        self.height, self.width = self.image.shape[:2]

        # Get path of set directory
        self.directory = "/".join(image_path.split("/")[:-2])

        # Clone the image for displaying purposes
        self.clone = self.image.copy()

        # Set flag for determining if we are in between the stard
        # and end of the cropping
        self.intermediate = False

        # Store the intermediate image
        self.intermediate_image = None

        # Flag for determining if we are drawing
        self.drawing = False

        # Collect info from mouse
        cv2.namedWindow("BoundingBox")
        cv2.setMouseCallback("BoundingBox", self.extract_coordinates)

        # Bounding box reference points
        self.top_lefts = []
        self.bottom_rights = []

        # Define temp coordinates
        self.temp_coordinates = None

        # Initialise counter for each cropping
        self.counter = 0

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            # Start the drawing mode
            self.drawing = True

            # Store temporary coordinates (might need amendment)
            self.temp_coordinates = (x, y)

        # If we are dragging the mouse around
        elif event != cv2.EVENT_LBUTTONUP:
            # Check we are in drawing mode
            if self.drawing == True:
                # Set intermediate mode
                self.intermediate = True

                # Draw rectangle
                self.intermediate_image = self.clone.copy()
                cv2.rectangle(
                    self.intermediate_image,
                    self.temp_coordinates,
                    (x, y),
                    (255, 255, 255),
                    2,
                )

        # Record ending (x,y) coordintes on left mouse button release
        elif event == cv2.EVENT_LBUTTONUP:
            # Stop drawing and intermediate phase
            self.drawing = False
            self.intermediate = False

            # One dimension is zero
            if self.temp_coordinates[0] == x or self.temp_coordinates[1] == y:
                print("Not allowed!")

            # Temp is top right, (x,y) is bottom left
            elif self.temp_coordinates[0] > x and self.temp_coordinates[1] < y:
                # Rearrange coordinates
                top_left = (x, self.temp_coordinates[1])
                bottom_right = (self.temp_coordinates[0], y)

                # Appennd coordinates
                self.top_lefts.append(top_left)
                self.bottom_rights.append(bottom_right)

            # Temp is bottom right, (x,y) is top left
            elif self.temp_coordinates[0] > x and self.temp_coordinates[1] > y:
                # Rearrange coordinates
                top_left = (x, y)
                bottom_right = self.temp_coordinates

                # Appennd coordinates
                self.top_lefts.append(top_left)
                self.bottom_rights.append(bottom_right)

            # Temp is bottom left, (x, y) is top right
            elif self.temp_coordinates[0] < x and self.temp_coordinates[1] > y:
                # Rearrange coordinates
                top_left = (self.temp_coordinates[0], y)
                bottom_right = (x, self.temp_coordinates[1])

                # Appennd coordinates
                self.top_lefts.append(top_left)
                self.bottom_rights.append(bottom_right)

            # Else, correct ordering
            else:
                # Rearrange coordinates
                top_left = self.temp_coordinates
                bottom_right = (x, y)

                # Appennd coordinates
                self.top_lefts.append(top_left)
                self.bottom_rights.append(bottom_right)

            # Draw rectangle
            cv2.rectangle(self.clone, top_left, bottom_right, (36, 255, 12), 2)

            with open(f"{self.directory}/labels/{self.name}.txt", "a") as file:

                # Create annotation
                annotation = self.create_annotation(top_left, bottom_right)

                # Write to file
                file.write(annotation)

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.image.copy()

    def show_image(self):
        """Show images while annotating"""

        # In intermediate phases, return image with partial annotation
        if self.intermediate:
            return self.intermediate_image
        # At the end of annotation return actual image
        else:
            return self.clone

    def create_annotation(self, top_left, bottom_right, class_identifier=0):
        """Create annotation according to the YOLO notation. That is:

        1. Do not return actual coordinates, but a rescaled version so that the image has height 1 and
            width 1.
        2. The output should be a txt file where every line consists of:
            class_identifier, centre_x, centre_y, width, height
           where class_identifier is an integer to which corresponds a particular class (e.g. 0 -> person),
           centre_x is the normalised x-coordinate of the bounding box centre,
           centre_y is the normalised y_coordinate of the bounding box centre,
           width is the normalised width of the bounding box,
           height is the normalised height of the bounding box"""

        # Find centre coordinates (normalised)
        centre_x = (top_left[0] + bottom_right[0]) / (2 * self.width)
        centre_y = (top_left[1] + bottom_right[1]) / (2 * self.height)

        # Get width and height of bounding box (normalised)
        bb_width = (bottom_right[0] - top_left[0]) / self.width
        bb_height = (bottom_right[1] - top_left[1]) / self.height

        return f"{class_identifier} {centre_x} {centre_y} {bb_width} {bb_height}\n"

    def get_coordinates(self):
        """Return coordinates of top-left and bottom-right
        coordinates of bounding boxes"""

        return self.top_lefts, self.bottom_rights
