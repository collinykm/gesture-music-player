import cv2
import numpy as np

# 1. Initialize canvas (e.g., dark blue background)
height, width = 500, 500
image = np.full((height, width, 3), (40, 20, 20), dtype=np.uint8)

# Center and radius parameters
center = (250, 250)
start_angle = 30   # Start angle in degrees
end_angle = 330    # End angle in degrees

outer_radius = 180  # Size of Shape 1 (Pizza)
inner_radius = 80   # Size of Shape 2 (Bite mark)

# 2. Create a single-channel mask (black background)
mask = np.zeros((height, width), dtype=np.uint8)

# 3. Draw Shape 1: Outer sector (White)
cv2.ellipse(
    mask,
    center=center,
    axes=(outer_radius, outer_radius),
    angle=0,
    startAngle=start_angle,
    endAngle=end_angle,
    color=255,
    thickness=-1  # -1 fills the shape
)

# 4. Draw Shape 2: Inner sector (Black) - Subtracts from the mask
cv2.ellipse(
    mask,
    center=center,
    axes=(inner_radius, inner_radius),
    angle=0,
    startAngle=start_angle,
    endAngle=end_angle,
    color=0,
    thickness=-1  # Cuts out the inner region
)

# 5. Apply the subtractive mask to color the final shape (e.g., golden yellow)
shape_color = (0, 215, 255)  # BGR
image[mask == 255] = shape_color

# Display result
cv2.imshow("Subtracted Shape", image)
cv2.waitKey(0)
cv2.destroyAllWindows()