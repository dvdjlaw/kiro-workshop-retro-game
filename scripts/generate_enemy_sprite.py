"""
Generate a simple pumpkin enemy sprite for the game
"""
import pygame
import sys

# Initialize Pygame
pygame.init()

# Create a 100x100 surface with transparency
sprite_size = 100
sprite = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)

# Colors
ORANGE = (255, 140, 0)
DARK_ORANGE = (200, 100, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (34, 139, 34)

# Draw pumpkin body (circle)
center_x, center_y = sprite_size // 2, sprite_size // 2 + 5
radius = 35

# Draw pumpkin segments (vertical lines to give it texture)
pygame.draw.circle(sprite, ORANGE, (center_x, center_y), radius)
pygame.draw.circle(sprite, DARK_ORANGE, (center_x, center_y), radius, 3)

# Draw vertical segments
for x_offset in [-15, -5, 5, 15]:
    start_y = center_y - int((radius**2 - x_offset**2)**0.5)
    end_y = center_y + int((radius**2 - x_offset**2)**0.5)
    pygame.draw.line(sprite, DARK_ORANGE, 
                    (center_x + x_offset, start_y), 
                    (center_x + x_offset, end_y), 2)

# Draw stem on top
stem_width = 8
stem_height = 12
stem_x = center_x - stem_width // 2
stem_y = center_y - radius - stem_height
pygame.draw.rect(sprite, GREEN, (stem_x, stem_y, stem_width, stem_height))
pygame.draw.rect(sprite, (20, 100, 20), (stem_x, stem_y, stem_width, stem_height), 2)

# Draw jack-o-lantern face
# Left eye (triangle)
eye_y = center_y - 8
left_eye_points = [
    (center_x - 18, eye_y + 8),
    (center_x - 10, eye_y),
    (center_x - 10, eye_y + 8)
]
pygame.draw.polygon(sprite, BLACK, left_eye_points)
pygame.draw.polygon(sprite, YELLOW, left_eye_points, 0)
pygame.draw.aalines(sprite, BLACK, True, left_eye_points, 2)

# Right eye (triangle)
right_eye_points = [
    (center_x + 10, eye_y + 8),
    (center_x + 18, eye_y),
    (center_x + 18, eye_y + 8)
]
pygame.draw.polygon(sprite, BLACK, right_eye_points)
pygame.draw.polygon(sprite, YELLOW, right_eye_points, 0)
pygame.draw.aalines(sprite, BLACK, True, right_eye_points, 2)

# Draw menacing grin (curved smile with teeth)
mouth_y = center_y + 10
mouth_width = 30

# Draw smile arc
smile_points = []
for i in range(11):
    x = center_x - mouth_width // 2 + (mouth_width * i // 10)
    # Parabolic curve for smile
    y_offset = ((i - 5) ** 2) // 3
    y = mouth_y + y_offset
    smile_points.append((x, y))

pygame.draw.lines(sprite, BLACK, False, smile_points, 3)

# Draw teeth (small triangles along the smile)
for i in range(0, len(smile_points) - 1, 2):
    x, y = smile_points[i]
    tooth_points = [
        (x - 2, y),
        (x, y - 5),
        (x + 2, y)
    ]
    pygame.draw.polygon(sprite, BLACK, tooth_points)

# Save the sprite
pygame.image.save(sprite, 'assets/enemy.png')
print("✅ Enemy sprite generated successfully at assets/enemy.png")

pygame.quit()
