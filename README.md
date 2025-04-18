**Sword Master: A Motion-Controlled Game**
Overview
Sword Master is an interactive motion-controlled game that uses your webcam to track your body movements. Play as a stickman warrior who battles enemies using sword gestures tracked through your real-life movements.
Features

Motion-Controlled Gameplay: Control a stickman character with your actual body movements
Dual Sword Combat: Use both hands to wield virtual swords and slash enemies
Progressively Challenging Levels: Enemy speed increases as you defeat more foes
Boss Battles: Special challenging enemies appear every 20 points
Health System: Track your remaining lives with heart icons
Sound Effects and Music: Immersive audio experience with battle sounds and background music
Interactive Story Mode: Learn the game's lore through a series of story screens
Attractive UI: Polished title screens and game over screen

Requirements

Python 3.x
Webcam
Libraries:

pygame
OpenCV (cv2)
MediaPipe
math
os
random



Installation

Clone the repository or download the ZIP file
Install the required dependencies:
pip install pygame opencv-python mediapipe

Ensure you have all the assets in the correct directories:

Assets/

fantasy-sword.png
boss.png
skull.png
heartfull.png
game_over.png
title_bg.png (optional)
font/

OpenSans-VariableFont_wdth_wght.ttf


sounds/

sword_slash.wav
devil_die.wav
boss_hit.wav
player_hit.wav
menu_select.wav


music/

The-Black-Waltz__Scott-Buckley.mp3




story.txt (containing story pages separated by newlines)



How to Play

Run the game:
python sword_master.py

Position yourself in front of your webcam where your full body is visible
At the title screen, press any key to start
Read through the story or press the SKIP button
Control the game with your body:

Your body movements control the stickman
Your hands control the positions of the swords
Hit the enemy skulls with your sword movements
Avoid letting enemies touch your body or head
Defeat boss enemies for bonus points and health



Controls

Body Movement: Controls the stickman's position
Hand Movement: Controls the sword positions
Press Q: Quit the game at any time

Gameplay Tips

Keep a good distance from your webcam so your whole body is visible
Make deliberate slashing motions to hit enemies
Watch for boss enemies that appear after every 20 points
Bosses move faster as they take damage
Try to maintain maximum health for boss battles
Defeating a boss rewards you with extra health

Game Mechanics

Enemies speed up as you defeat more of them
Bosses have multiple hit points and get progressively harder
Missing an enemy or getting hit reduces your health
Game ends when health reaches zero
Final score is displayed on the game over screen
