# 🕹️ Stickman-Game

**A webcam-based motion-controlled game using OpenCV, MediaPipe, and Pygame.**  
Just take it lite and enjoy!

---

## 🎮 Overview

**Stickman-Game** is an interactive motion-controlled game where your body becomes the controller! Using your webcam, the game tracks your full-body movements to let you control a stickman character on screen. Swing your arms to control swords and defeat waves of invading devils and powerful boss enemies.

---

## ✨ Features

- 🔁 **Full Body Motion Control** – Move your arms and body to control the stickman character and swords.
- ⚔️ **Dual-Wielding Combat** – Use both arms to control two different swords.
- 📈 **Progressive Difficulty** – Enemies get faster as your score increases.
- 👹 **Boss Battles** – Face tough bosses at score milestones.
- ❤️ **Health System** – Start with 5 hearts and avoid getting hit.
- 📖 **Interactive Story Mode** – Enjoy a simple narrative before gameplay.
- 🔊 **Dynamic Sound Effects** – Responsive audio feedback during gameplay.

---

## 🛠️ Prerequisites

- Python 3.7 or higher
- Webcam
- Proper lighting for accurate motion detection

---

## 📦 Installation

### 🔁 Clone the Repository

```bash
git clone https://github.com/uayushdubey/Stickman-Game.git
cd Stickman-Game
```

### 📥 Install Dependencies

#### Option 1: Using `requirements.txt`
```bash
pip install -r requirements.txt
```

#### Option 2: Manual Installation
```bash
pip install pygame opencv-python mediapipe
```

---

## 🎯 How to Play

```bash
python app2.py
```

1. Stand in front of your webcam (your full body should be visible).
2. On the title screen, press any key to start.
3. Read the story or press **Skip**.
4. Move your arms to control swords.
5. Hit devils to earn points and avoid letting them touch your body.
6. Defeat bosses for extra health.
7. Press **Q** anytime to quit the game.

---

## 🎮 Controls

| Action            | Control             |
|-------------------|---------------------|
| Move Right Arm    | Right Sword         |
| Move Left Arm     | Left Sword          |
| Body Movement     | Stickman Movement   |
| Any Key           | Advance Story       |
| Q Key             | Quit Game           |

---

## 🧠 Game Mechanics

- **Score**: +1 for every enemy hit.
- **Health**: Starts with 5 hearts, decreases when hit.
- **Boss Battles**: Appear every 20 points.
- **Enemy Speed**: Increases with each hit.
- **Boss Health**: Scales with score.

---

## 🏆 Winning Strategy

- Stay mobile to avoid hits.
- Use sharp, controlled arm movements.
- Prioritize enemies near your body.
- Prepare for boss battles with maximum health.

---

## 🛠️ Troubleshooting

| Issue                  | Solution                                              |
|------------------------|-------------------------------------------------------|
| Poor Motion Detection  | Ensure good lighting and full-body visibility        |
| Lag/Performance        | Close other apps to improve performance              |
| No Sound               | Check system audio settings                          |
| Missing Assets         | Verify that all required files exist properly        |

---

## 🛣️ Roadmap

- [ ] Multiplayer mode  
- [ ] Additional enemy types  
- [ ] Power-ups & special abilities  
- [ ] Customizable character skins  
- [ ] Level selection system  

---

## 🤝 Contributing

Contributions are welcome! 🎉

1. Fork the repository  
2. Create your feature branch:  
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add AmazingFeature"
   ```
4. Push to the branch:  
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **[Pygame](https://www.pygame.org/)** – Game development library  
- **[MediaPipe](https://mediapipe.dev/)** – Motion tracking framework  
- **[OpenCV](https://opencv.org/)** – Computer vision library  
- **Scott Buckley** – Background music composer  

---

> Developed by [@uayushdubey](https://github.com/uayushdubey) — _"Just take it lite and enjoy!"_
