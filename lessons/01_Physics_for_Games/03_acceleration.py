import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
SQUARE_SIZE = 50
SQUARE_COLOR = (255, 0, 0)  # Red
FPS = 60
K = 3 # Spring constant, controls how strong the spring force is

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Accelerating Red Square")

# Square starting position
x_pos = 20
y_pos = (SCREEN_HEIGHT - SQUARE_SIZE) // 2

d_t = 1 / FPS  # Time step for physics calculations

mass = 2.0 # Mass of the square, used to calculate acceleration
velocity = 0

# Movement direction: 1 for right, -1 for left
direction = 1

# Main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
         
    # Calculate the spring force, which is the force that pulls the square back
    # to the center, as if it was attached to a spring
<<<<<<< HEAD:lessons/01_Motion_and_Physics/03_acceleration.py
    print(-K * (x_pos - (SCREEN_WIDTH-SQUARE_SIZE) // 2))
    a = -K * (x_pos - (SCREEN_WIDTH-SQUARE_SIZE) // 2)
=======

    
    # Calculate the spring force, accounting for mass (F = -k*x)
    # Force divided by mass gives acceleration (F = ma → a = F/m)
    a = (-K * (x_pos - (SCREEN_WIDTH-SQUARE_SIZE) // 2)) / mass
>>>>>>> fde5e2410fc5d7efe6b612da7fd047946b1ceee4:lessons/01_Physics_for_Games/03_acceleration.py

    # Update the velocity with the acceleration. Notice that we change
    # the velocity by adding the acceleration, not setting it to the acceleration, 
    # and we change it a bit each frame. 
    velocity += a * d_t
    
    # Update the position with the velocity. Like with the velocity, we change
    # the position by adding the velocity, not setting it to the velocity, and
    # we change it a bit each frame.
    x_pos += velocity * d_t

    # Fill the screen with black (clears previous frame)
    screen.fill((0, 0, 0))

    # Draw the red square
    pygame.draw.rect(screen, SQUARE_COLOR, (x_pos, y_pos, SQUARE_SIZE, SQUARE_SIZE))

    # Update the display
    pygame.display.flip()

    # Frame rate control
    pygame.time.Clock().tick(FPS)

# Quit Pygame
pygame.quit()
