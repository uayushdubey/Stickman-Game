import os
import random
import math
from math import sqrt


import cv2
import mediapipe as mp
import pygame

# color codes
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
DARK_RED = (139, 0, 0)

# loading assets
SWORD_WIDTH, SWORD_HEIGHT = 100, 100
SWORD_IMAGE = pygame.transform.rotate(
    pygame.image.load(os.path.join("Assets", "fantasy-sword.png")),
    90)
LEFT_SWORD = pygame.transform.scale(SWORD_IMAGE, (SWORD_WIDTH, SWORD_HEIGHT))
RIGHT_SWORD = pygame.transform.scale(
    pygame.transform.flip(SWORD_IMAGE, True, False),
    (SWORD_WIDTH, SWORD_HEIGHT))

BOSS_WIDTH, BOSS_HEIGHT = 200, 200
BOSS = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "boss.png")),
    (BOSS_WIDTH, BOSS_HEIGHT))
INITIAL_BOSS_SPEED = 10
BOSS_SPEED = INITIAL_BOSS_SPEED
BOSS_INITIAL_HEALTH = 10
BOSS_HEALTH = BOSS_INITIAL_HEALTH

DEVIL_WIDTH, DEVIL_HEIGHT = 120, 120
DEVIL_IMAGE = pygame.image.load(os.path.join("Assets", "skull.png"))
DEVIL = pygame.transform.scale(
    DEVIL_IMAGE,
    (DEVIL_WIDTH, DEVIL_HEIGHT))
INITIAL_DEVIL_SPEED = 7
DEVIL_SPEED = INITIAL_DEVIL_SPEED
MAX_DEVIL_SPEED = DEVIL_SPEED + 30

HEART_FULL_X, HEART_FULL_Y = 10, 10
PLAYER_HEALTH_FULL = pygame.image.load(os.path.join("Assets", "heartfull.png"))
PLAYER_HEALTH = pygame.transform.scale(PLAYER_HEALTH_FULL, (90, 90))

# custom pygame events
DEVIL_HIT = pygame.USEREVENT + 1
DEVIL_MISS = pygame.USEREVENT + 2
BOSS_HIT = pygame.USEREVENT + 3
BOSS_HIT_PLAYER = pygame.USEREVENT + 4
BOSS_REVERSE_DIRECTION = pygame.USEREVENT + 5

# initialize pygame
pygame.init()
pygame.font.init()
# create pygame window
WIDTH, HEIGHT = 1280, 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman-Mediapipe")
pygame.display.toggle_fullscreen()  # go fullscreen
pygame.mouse.set_visible(False)  # hide mouse
# Initialize Clock for FPS
FPS = 30
clock = pygame.time.Clock()
# initialize pygame fonts
FONT = pygame.font.Font(os.path.join("Assets", "font", "OpenSans-VariableFont_wdth_wght.ttf"), 30)
SCOREFONT = pygame.font.Font(os.path.join("Assets", "font", "OpenSans-VariableFont_wdth_wght.ttf"), 20)
TITLE_FONT = pygame.font.Font(os.path.join("Assets", "font", "OpenSans-VariableFont_wdth_wght.ttf"), 80)
SUBTITLE_FONT = pygame.font.Font(os.path.join("Assets", "font", "OpenSans-VariableFont_wdth_wght.ttf"), 40)

with open("story.txt", "r") as f:
    story_text = f.read().split('\n')
story_pages = [FONT.render(page, 1, WHITE) for page in story_text]

# music
pygame.mixer.init()

# Load sound effects
try:
    SWORD_SLASH_SOUND = pygame.mixer.Sound(os.path.join("Assets", "sounds", "sword_slash.wav"))
    DEVIL_DIE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "sounds", "devil_die.wav"))
    BOSS_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "sounds", "boss_hit.wav"))
    PLAYER_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "sounds", "player_hit.wav"))
    MENU_SELECT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "sounds", "menu_select.wav"))
except:
    # If sound files are missing, define empty sounds to avoid errors
    class EmptySound:
        def play(self): pass


    SWORD_SLASH_SOUND = DEVIL_DIE_SOUND = BOSS_HIT_SOUND = PLAYER_HIT_SOUND = MENU_SELECT_SOUND = EmptySound()

# Load and play background music
try:
    pygame.mixer.music.load(os.path.join("Assets", "music", "The-Black-Waltz__Scott-Buckley.mp3"))
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
except:
    pass  # Skip if music file is missing

# game over screen
GAME_OVER = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "game_over.png")),
    (WIDTH, HEIGHT)
)

# Try to load title screen background, use black if not found
try:
    TITLE_BG = pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "title_bg.png")),
        (WIDTH, HEIGHT)
    )
except:
    TITLE_BG = None

# mediapipe module load for pose
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

# various vars
colorforstickman = (7, 242, 207)

score = 0  # game score
health = 5  # miss the devils 3 times and its game over
BOSS_TRIGGER_SCORE = 20  # at every increment of 20 in score, boss level is triggered


def distance(x1, y1, x2, y2):
    # returns integer distance between two points
    return int(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


leftwrist_x, leftwrist_y = 0, 0  # making these global because they're needed for swords AND player body collision rects
rightwrist_x, rightwrist_y = 0, 0
middleshoulder_x, middleshoulder_y = 0, 0  # these are required for the player body collision rects
nose_x, nose_y = 0, 0
lefthip_x, lefthip_y = 0, 0


# Function to create text with shadow effect
def draw_text_with_shadow(text, font, color, shadow_color, x, y, shadow_offset=2):
    # Draw shadow text
    shadow_surface = font.render(text, True, shadow_color)
    window.blit(shadow_surface, (x + shadow_offset, y + shadow_offset))

    # Draw main text
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))
    return text_surface


def draw_stickman():  # tracks movements and draws stickman
    global leftwrist_x, leftwrist_y
    global rightwrist_x, rightwrist_y
    global middleshoulder_x, middleshoulder_y
    global nose_x, nose_y
    global lefthip_x, lefthip_y

    # pose tracking
    success, image = cap.read()
    image = cv2.flip(image, 1)
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    h, w, c = image.shape
    image = cv2.rectangle(image, (0, 0), (w, h), (0, 0, 0), -1)

    # drawing stickman
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = image.shape

            if int(id) == 11:  # 11 is left shoulder
                leftshoulder_x, leftshoulder_y = int(lm.x * w), int(lm.y * h)
            if int(id) == 12:  # 12 is right shoulder
                rightshoulder_x, rightshoulder_y = int(lm.x * w), int(lm.y * h)
            if int(id) == 23:  # 23 is left hip
                lefthip_x, lefthip_y = int(lm.x * w), int(lm.y * h)
            if int(id) == 24:  # 24 is right hip
                righthip_x, righthip_y = int(lm.x * w), int(lm.y * h)
            if int(id) == 15:  # 15 is left wrist
                leftwrist_x, leftwrist_y = int(lm.x * w), int(lm.y * h)
            if int(id) == 16:  # 16 is right wrist
                rightwrist_x, rightwrist_y = int(lm.x * w), int(lm.y * h)
            if int(id) == 27:  # 27 is left ankle
                leftankle_x, leftankle_y = int(lm.x * w), int(lm.y * h)
            if int(id) == 28:  # 28 is right ankle
                rightankle_x, rightankle_y = int(lm.x * w), int(lm.y * h)
            if int(id) == 0:  # 0 is nose
                nose_x, nose_y = int(lm.x * w), int(lm.y * h)

        # the next lines till 'if' condition is just connecting the points to make a stick figure
        middleshoulder_x = int(leftshoulder_x + rightshoulder_x) // 2
        middleshoulder_y = int(leftshoulder_y + rightshoulder_y) // 2
        pygame.draw.circle(window, colorforstickman, (middleshoulder_x, middleshoulder_y), 5)

        middlehip_x = int(lefthip_x + righthip_x) // 2
        middlehip_y = int(lefthip_y + righthip_y) // 2

        pygame.draw.circle(window, colorforstickman, (middlehip_x, middlehip_y), 5)

        pygame.draw.circle(window, colorforstickman, (leftwrist_x, leftwrist_y), 5)
        pygame.draw.circle(window, colorforstickman, (rightwrist_x, rightwrist_y), 5)
        pygame.draw.circle(window, colorforstickman, (leftankle_x, leftankle_y), 5)
        pygame.draw.circle(window, colorforstickman, (rightankle_x, rightankle_y), 5)

        # arms
        pygame.draw.line(window, colorforstickman, (middleshoulder_x, middleshoulder_y), (rightwrist_x, rightwrist_y),
                         2)
        pygame.draw.line(window, colorforstickman, (middleshoulder_x, middleshoulder_y), (leftwrist_x, leftwrist_y), 2)

        pygame.draw.line(window, colorforstickman, (middleshoulder_x, middleshoulder_y), (middlehip_x, middlehip_y), 2)

        pygame.draw.line(window, colorforstickman, (middlehip_x, middlehip_y), (leftankle_x, leftankle_y))
        pygame.draw.line(window, colorforstickman, (middlehip_x, middlehip_y), (rightankle_x, rightankle_y))
        pygame.draw.line(window, colorforstickman, (middleshoulder_x, middleshoulder_y), (nose_x, nose_y + 50), 2)

        pygame.draw.circle(window, colorforstickman, (nose_x, nose_y), 50, 2)  # face
        pygame.draw.circle(window, RED, (rightwrist_x, rightwrist_y), 10)  # right hand
        pygame.draw.circle(window, RED, (leftwrist_x, leftwrist_y), 10)  # left hand


def draw_window(left_sword, right_sword, devil, devil_right, boss_level=False):
    # draw health hearts
    global health, score

    heart_padding_x = 0
    for i in range(health):
        window.blit(PLAYER_HEALTH, (HEART_FULL_X + heart_padding_x, HEART_FULL_Y))
        heart_padding_x += 40

    # draw score
    score_text = SCOREFONT.render(f"Score: {score}", 1, WHITE)
    window.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    # draw stickman
    draw_stickman()

    # draw swords
    left_sword.x = leftwrist_x - 10
    left_sword.y = leftwrist_y - SWORD_HEIGHT + 10
    right_sword.x = rightwrist_x - SWORD_WIDTH + 10
    right_sword.y = rightwrist_y - SWORD_HEIGHT + 10
    window.blit(LEFT_SWORD, (left_sword.x, left_sword.y))
    window.blit(RIGHT_SWORD, (right_sword.x, right_sword.y))

    if boss_level:
        # draw boss handled elsewhere
        pass
    else:
        # draw devil
        if devil_right:
            devil.x += DEVIL_SPEED
        else:
            devil.x -= DEVIL_SPEED
        window.blit(DEVIL, (devil.x, devil.y))


def devil_collision_detect(devil, left_sword, right_sword, boss_level):
    # player's body collision vars
    global nose_x, nose_y
    global middleshoulder_x, middleshoulder_y

    # checking if devil collides with either sword
    if devil.colliderect(left_sword) or devil.colliderect(right_sword):
        if boss_level:
            pygame.event.post(
                pygame.event.Event(BOSS_HIT)
            )
            BOSS_HIT_SOUND.play()
        else:
            pygame.event.post(
                pygame.event.Event(DEVIL_HIT)
            )
            DEVIL_DIE_SOUND.play()

    # checking if devil goes off the screen
    if boss_level:
        if devil.x > WIDTH or devil.x < -BOSS_WIDTH:
            pygame.event.post(
                pygame.event.Event(BOSS_REVERSE_DIRECTION)
            )
    else:
        if devil.x > WIDTH or devil.x < -DEVIL_WIDTH:
            pygame.event.post(
                pygame.event.Event(DEVIL_MISS)
            )

    # devil collision with player's face, arms or neck
    # face
    face = pygame.Rect(nose_x - 50, nose_y - 50, 100, 100)

    if devil.colliderect(face):
        if boss_level:
            pygame.event.post(
                pygame.event.Event(BOSS_HIT_PLAYER)
            )
        else:
            pygame.event.post(
                pygame.event.Event(DEVIL_MISS)  # can be used because DEVIL_MISS reduces health and respawns a devil
            )
        PLAYER_HIT_SOUND.play()

    # neck and arms
    hit_neck_or_arms = devil.clipline((nose_x, nose_y), (middleshoulder_x, middleshoulder_y)) or devil.clipline(
        (middleshoulder_x, middleshoulder_y), (leftwrist_x, leftwrist_y)) or devil.clipline(
        (middleshoulder_x, middleshoulder_y), (rightwrist_x, rightwrist_y))

    if hit_neck_or_arms:
        if boss_level:
            pygame.event.post(
                pygame.event.Event(BOSS_HIT_PLAYER)
            )
        else:
            pygame.event.post(
                pygame.event.Event(DEVIL_MISS)
            )
        PLAYER_HIT_SOUND.play()


def show_title_screen():
    """
    Display an attractive title screen with animations
    Returns True when player is ready to start game
    """
    title_y = -100  # Start position above screen
    target_y = HEIGHT // 4  # Target position

    # Create a pulsing "Press any key" text
    pulse_size = 0
    pulse_direction = 1

    # Load sword images for decoration
    left_sword_title = pygame.transform.scale(LEFT_SWORD, (150, 150))
    right_sword_title = pygame.transform.scale(RIGHT_SWORD, (150, 150))

    # Main animation loop
    running = True
    while running:
        clock.tick(FPS)
        window.fill(BLACK)

        # Draw background if available
        if TITLE_BG:
            window.blit(TITLE_BG, (0, 0))

        # Draw title with animation
        if title_y < target_y:
            title_y += 5

        # Draw title text with shadow effect
        title_text = "SWORD MASTER"
        draw_text_with_shadow(title_text, TITLE_FONT, GOLD, DARK_RED,
                              WIDTH // 2 - TITLE_FONT.size(title_text)[0] // 2, title_y, 4)

        # Draw decorative swords
        window.blit(left_sword_title, (WIDTH // 2 - 250, title_y + 20))
        window.blit(right_sword_title, (WIDTH // 2 + 100, title_y + 20))

        # Draw subtitle
        subtitle_text = "A Motion-Controlled Adventure"
        draw_text_with_shadow(subtitle_text, SUBTITLE_FONT, WHITE, DARK_RED,
                              WIDTH // 2 - SUBTITLE_FONT.size(subtitle_text)[0] // 2, title_y + 100)

        # Draw pulsing "Press any key" text
        pulse_size += 0.05 * pulse_direction
        if pulse_size > 1.2 or pulse_size < 0.8:
            pulse_direction *= -1

        press_key_font = pygame.font.Font(os.path.join("Assets", "font", "OpenSans-VariableFont_wdth_wght.ttf"),
                                          int(30 * pulse_size))
        press_key_text = "Press any key to start"
        press_key_surface = press_key_font.render(press_key_text, True, WHITE)
        window.blit(press_key_surface,
                    (WIDTH // 2 - press_key_surface.get_width() // 2, HEIGHT * 3 // 4))

        # Draw instructions
        instructions = [
            "Use your body to control the stickman",
            "Move your hands to control the swords",
            "Hit the devils with your swords to score points",
            "Avoid letting devils touch your body",
            "Defeat bosses to earn extra health"
        ]

        instruction_y = HEIGHT // 2
        for instruction in instructions:
            instruction_surface = FONT.render(instruction, True, WHITE)
            window.blit(instruction_surface,
                        (WIDTH // 2 - instruction_surface.get_width() // 2, instruction_y))
            instruction_y += 40

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                MENU_SELECT_SOUND.play()
                return True

        pygame.display.update()


def show_story_screen():
    """
    Display story screens with better transitions and a skip button
    """
    global story_pages

    page = 0
    fade_alpha = 0  # For fade effect
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)

    # Create a skip button with attractive styling
    skip_button_rect = pygame.Rect(WIDTH - 120, HEIGHT - 60, 100, 40)
    button_color = GOLD
    button_hover_color = (255, 235, 120)  # Lighter gold for hover
    button_is_hovered = False

    # Animation variables for button pulsing effect
    pulse_size = 1.0
    pulse_direction = 0.03
    page_transition_speed = 5

    while page < len(story_pages):
        clock.tick(FPS)
        window.fill(BLACK)

        # Draw current story page with a gentle float animation
        vertical_offset = math.sin(pygame.time.get_ticks() * 0.001) * 5  # Subtle floating effect
        window.blit(story_pages[page], (WIDTH // 2 - story_pages[page].get_width() // 2,
                                        HEIGHT // 2 - story_pages[page].get_height() // 2 + vertical_offset))

        # Get mouse position for button interaction
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is hovering over skip button
        button_is_hovered = skip_button_rect.collidepoint(mouse_pos)

        # Draw skip button with pulsing animation when hovered
        if button_is_hovered:
            # Pulse effect when hovered
            pulse_size += pulse_direction
            if pulse_size > 1.1 or pulse_size < 0.9:
                pulse_direction *= -1

            # Draw larger button when hovered with pulse effect
            button_width = int(skip_button_rect.width * pulse_size)
            button_height = int(skip_button_rect.height * pulse_size)
            button_x = skip_button_rect.centerx - button_width // 2
            button_y = skip_button_rect.centery - button_height // 2

            pygame.draw.rect(window, button_hover_color,
                             (button_x, button_y, button_width, button_height),
                             border_radius=10)
        else:
            # Regular button
            pygame.draw.rect(window, button_color, skip_button_rect, border_radius=10)

        # Draw button text
        skip_text = FONT.render("SKIP", True, BLACK if button_is_hovered else WHITE)
        window.blit(skip_text, (skip_button_rect.centerx - skip_text.get_width() // 2,
                                skip_button_rect.centery - skip_text.get_height() // 2))

        # Draw page indicator
        page_indicator_text = f"Page {page + 1}/{len(story_pages)}"
        page_indicator_surface = SCOREFONT.render(page_indicator_text, True, WHITE)
        window.blit(page_indicator_surface, (20, HEIGHT - 40))

        # Handle fade in/out effect
        if fade_alpha > 0:
            fade_surface.set_alpha(fade_alpha)
            window.blit(fade_surface, (0, 0))
            fade_alpha -= page_transition_speed

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                # Skip to next page immediately on key press
                fade_alpha = 255  # Start fade effect
                page += 1
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if skip_button_rect.collidepoint(event.pos):
                        # Skip all pages when button is clicked
                        MENU_SELECT_SOUND.play()
                        return True
                    # REMOVED: The else clause that was advancing to the next page when clicking anywhere

        pygame.display.update()

        # Auto-advance after delay if no key press
        if fade_alpha <= 0:
            # Wait a bit on each page
            counter = 0
            waiting = True
            while waiting and counter < FPS * 5:  # Wait for 5 seconds
                clock.tick(FPS)
                counter += 1

                # Continue checking for mouse input during wait
                mouse_pos = pygame.mouse.get_pos()
                button_is_hovered = skip_button_rect.collidepoint(mouse_pos)

                # Draw everything again during wait to keep button interactive
                window.fill(BLACK)
                window.blit(story_pages[page], (WIDTH // 2 - story_pages[page].get_width() // 2,
                                                HEIGHT // 2 - story_pages[page].get_height() // 2 + vertical_offset))

                # Update button animation
                if button_is_hovered:
                    pulse_size += pulse_direction
                    if pulse_size > 1.1 or pulse_size < 0.9:
                        pulse_direction *= -1

                    button_width = int(skip_button_rect.width * pulse_size)
                    button_height = int(skip_button_rect.height * pulse_size)
                    button_x = skip_button_rect.centerx - button_width // 2
                    button_y = skip_button_rect.centery - button_height // 2

                    pygame.draw.rect(window, button_hover_color,
                                     (button_x, button_y, button_width, button_height),
                                     border_radius=10)
                else:
                    pygame.draw.rect(window, button_color, skip_button_rect, border_radius=10)

                # Redraw button text
                skip_text = FONT.render("SKIP", True, BLACK if button_is_hovered else WHITE)
                window.blit(skip_text, (skip_button_rect.centerx - skip_text.get_width() // 2,
                                        skip_button_rect.centery - skip_text.get_height() // 2))

                # Redraw page indicator
                window.blit(page_indicator_surface, (20, HEIGHT - 40))

                pygame.display.update()

                # Allow skipping during wait
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return False
                    if event.type == pygame.KEYDOWN:
                        waiting = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            if skip_button_rect.collidepoint(event.pos):
                                # Skip all pages
                                MENU_SELECT_SOUND.play()
                                return True
                            # REMOVED: The else clause that was advancing to the next page when clicking anywhere

            # Move to next page with fade effect
            fade_alpha = 255
            page += 1

    return True

def main():
    global score, health
    global DEVIL_SPEED, MAX_DEVIL_SPEED, INITIAL_DEVIL_SPEED
    global BOSS_WIDTH, BOSS_HEIGHT, BOSS_SPEED, BOSS_INITIAL_HEALTH, BOSS_HEALTH
    global nose_x, nose_y
    global story_pages

    # Display the title screen
    if not show_title_screen():
        return

    # Display the story screen
    if not show_story_screen():
        return

    # main game loop
    draw_stickman()

    left_sword = pygame.Rect(leftwrist_x, leftwrist_y - SWORD_HEIGHT, SWORD_WIDTH, SWORD_HEIGHT)
    right_sword = pygame.Rect(rightwrist_x - SWORD_WIDTH, rightwrist_y - SWORD_HEIGHT, SWORD_WIDTH, SWORD_HEIGHT)

    devil = pygame.Rect(0, 350, DEVIL_WIDTH, DEVIL_HEIGHT)
    devil.x = -DEVIL_WIDTH
    devil_right = True  # to track if devil is moving right or left

    boss_level = False  # to track if on boss level
    boss = pygame.Rect(0, 20, BOSS_WIDTH, BOSS_HEIGHT)
    boss.x = -BOSS_WIDTH
    boss.y = 0
    boss_right = True

    running = True
    while (running):
        clock.tick(FPS)

        # handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:  # press Q to force quit game
                if event.key == pygame.K_q:
                    running = False

            if event.type == DEVIL_HIT:  # handle devil hit sword event
                if random.randint(0, 1):
                    devil.x = -DEVIL_WIDTH
                    devil_right = True
                else:
                    devil.x = WIDTH
                    devil_right = False

                devil.y = random.randrange(0, 351)

                score += 1
                DEVIL_SPEED += 2  # increase devil speed with every collision

            if event.type == DEVIL_MISS:  # same as DEVIL_HIT, but reduce health only
                health -= 1

                if random.randint(0, 1):
                    devil.x = -DEVIL_WIDTH
                    devil_right = True
                else:
                    devil.x = WIDTH
                    devil_right = False

                devil.y = random.randrange(0, 351)

                DEVIL_SPEED += 2  # increase devil speed with every collision

            if event.type == BOSS_HIT:
                boss.x = random.randrange(0, WIDTH - BOSS_WIDTH)
                BOSS_HEALTH -= 1
                BOSS_SPEED += 2

                if BOSS_HEALTH <= 0:
                    boss_level = False

                    boss.y = 0

                    BOSS_HEALTH = BOSS_INITIAL_HEALTH + (score % BOSS_TRIGGER_SCORE)
                    BOSS_SPEED = INITIAL_BOSS_SPEED + (score % BOSS_TRIGGER_SCORE)

                    score += 1

                    if health + 2 > 5:
                        health = 5
                    else:
                        health += 2

            if event.type == BOSS_HIT_PLAYER:
                boss.x = random.randrange(0, WIDTH - BOSS_WIDTH)
                BOSS_SPEED += 1
                health -= 2

            if event.type == BOSS_REVERSE_DIRECTION:
                pass  # handled manually below. TODO: remove this event later

        window.fill((0, 0, 0))  # clearing the pygame display

        # draws the whole game window
        draw_window(left_sword, right_sword, devil, devil_right, boss_level)

        # check if boss level reached
        if score % BOSS_TRIGGER_SCORE == 0:
            if score == 0:
                boss_level = False
            else:
                boss_level = True

        # boss level or normal devils
        if boss_level:
            devil_collision_detect(boss, left_sword, right_sword, boss_level)
        else:
            # detect collisions with the devil and post HIT or MISS events
            devil_collision_detect(devil, left_sword, right_sword, boss_level)

            if DEVIL_SPEED >= MAX_DEVIL_SPEED:  # if devil speed reaches max devil speed, boss level is trigered
                INITIAL_DEVIL_SPEED += 2  # increase game hardness by incrementing initial devil speed
                DEVIL_SPEED = INITIAL_DEVIL_SPEED

        # handling boss drawing here
        if boss_level:
            # right-left and gradual downward movement
            if boss.x > WIDTH:
                boss_right = False
                boss.y += BOSS_HEIGHT // 2
                BOSS_SPEED += 1
            elif boss.x < -BOSS_WIDTH:
                boss_right = True
                boss.y += BOSS_HEIGHT // 2
                BOSS_SPEED += 1

            # collisions are handled above

            # detect if boss goes vertically out of the screen, triggering game over
            if boss.y > HEIGHT:
                break

            if boss_right:
                boss.x += BOSS_SPEED
            else:
                boss.x -= BOSS_SPEED

            window.blit(BOSS, (boss.x, boss.y))
            bosshealth = FONT.render(f"Boss Health: {BOSS_HEALTH}", 1, WHITE)
            window.blit(bosshealth, (WIDTH - bosshealth.get_width() - 10, 40))

        pygame.display.update()  # update the actual display

        if health <= 0:
            break

    # GAME OVER screen with final score
    window.fill(BLACK)
    window.blit(GAME_OVER, (0, 0))

    # Display final score at the top right corner
    final_score_text = f"Final Score: {score}"
    # Calculate position for top right with some padding
    score_x = WIDTH - TITLE_FONT.size(final_score_text)[0] - 20  # 20px padding from right edge
    score_y = 20  # 20px padding from top edge
    draw_text_with_shadow(final_score_text, TITLE_FONT, GOLD, DARK_RED, score_x, score_y)

    # Display "Press any key to exit" message
    exit_text = "Press any key to exit"
    draw_text_with_shadow(exit_text, FONT, WHITE, DARK_RED,
                          WIDTH // 2 - FONT.size(exit_text)[0] // 2, HEIGHT * 3 // 4)

    pygame.display.update()
    # Wait for any key press before exiting
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False


if __name__ == "__main__":
    main()
