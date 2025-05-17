Stickman-Game

🎮 Overview
Stickman Game with implementation of OpenCV module and Pygame - just take it, lite and enjoy! This motion-controlled game uses your webcam to track your body movements, allowing you to control a stickman character on screen. Swing your arms to wield virtual swords and defeat the invading devils and boss enemies!
✨ Features

Full Body Motion Control: Control your character using natural body movements
Dual-Wielding Combat: Swing both arms to control two different swords
Progressive Difficulty: Enemies move faster as your score increases
Boss Battles: Face challenging boss enemies at score milestones
Health System: Manage your health while avoiding enemy attacks
Interactive Story Mode: Immerse yourself in the game narrative
Dynamic Sound Effects: Enjoy responsive audio feedback during gameplay

🛠️ Prerequisites

Python 3.7 or higher
Webcam
Sufficient lighting for motion detection
Required Python packages (see Installation)

📋 Installation

Clone this repository:
bashgit clone https://github.com/uayushdubey/Stickman-Game.git
cd Stickman-Game

Install required packages:
bashpip install -r requirements.txt
Or install them manually:
bashpip install pygame opencv-python mediapipe


🎯 How to Play

Run the game:
bashpython app2.py

Position yourself in front of your webcam, ensuring your whole body is visible
On the title screen, press any key to start
Read through the story (or press Skip)
Move your arms to control the swords
Hit the devils with your swords to score points
Avoid letting the devils touch your body
Defeat bosses to earn extra health
Press Q at any time to quit the game

🎮 Controls

Right Arm Movement: Controls the right sword
Left Arm Movement: Controls the left sword
Body Position: Controls the stickman character
Any Key: Advance through story screens
Q Key: Quit game

🧠 Game Mechanics

Score: Increases by 1 with each defeated enemy
Health: Starts with 5 hearts, decreases when enemies hit you
Boss Levels: Triggered every 20 points
Devil Speed: Increases after each hit, making the game progressively harder
Boss Health: Increases with your score, making boss battles more challenging

🏆 Winning Strategy

Keep moving to avoid enemy contact
Use quick, precise arm movements for better sword control
Focus on devils approaching your body
During boss battles, prioritize hitting the boss while avoiding contact
Try to maintain maximum health before boss encounters

🔧 Troubleshooting

Poor Motion Detection: Ensure you have adequate lighting and your full body is visible
Performance Issues: Close other applications to free up system resources
Sound Problems: Check your system's audio settings and volume
Missing Assets: Verify all required files exist in the proper directories

🛣️ Roadmap

 Multiplayer mode
 Additional enemy types
 Power-ups and special abilities
 Customizable character appearance
 Level selection system

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the project
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgements

Pygame - Game development library
MediaPipe - Motion tracking framework
OpenCV - Computer vision library
Scott Buckley - Background music composer


Developed by uayushdubey
"Just take it lite and enjoy!"
