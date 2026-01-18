#  Mini Game Hub

**A modern, immersive Python-based gaming platform.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/CustomTkinter-5.2.2-blue?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)]()

---

##  Overview

**Mini Game Hub** is a desktop application that bundles multiple classic games into a single, unified interface. Built with modern design principles, it features a sleek dark-mode UI, secure user authentication, and persistent statistical tracking.

Whether you want to challenge your memory, test your vocabulary, or solve complex mazes, Mini Game Hub provides a seamless experience.

##  Key Features

###  Modern Experience
*   **Sleek UI**: Built using **CustomTkinter** for a professional, responsive look with a native dark mode.
*   **Immersive**: Launches in **Full Screen / Maximized** mode by default for focused gameplay.
*   **Responsive**: Fluid layouts that adapt to your screen size.

###  Security & Persistence
*   **Secure Auth**: User registration and login protected by industry-standard **bcrypt** password hashing.
*   **Local Database**: All user profiles, game history, and statistics are stored securely in a local **SQLite** database.

###  The Games
| Game | Description | Highlights |
|------|-------------|------------|
|  **Maze Path** | Navigate through procedural mazes. | Pathfinding algorithms, multiple difficulties. |
|  **Memory Card** | Classic tile-matching puzzle. | Time tracking, move efficiency scoring. |
|  **Hangman** | Guess the word before time runs out. | Visual progression, multiple categories. |
|  **Typing Defense** | Type falling words to destroy them. | Action typing, increasing speed. |
|  **Simon Says** | Repeat the flashing color sequence. | Memory challenge, progressive difficulty. |

##  Tech Stack

*   **Language**: Python 3.8+
*   **GUI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Modern wrapper for Tkinter)
*   **Database**: SQLite
*   **Security**: bcrypt
*   **Architecture**: Modular MVC-like structure

##  Getting Started

### Prerequisites
*   Python 3.8 or higher installed on your system.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/mini-game-hub.git
    cd mini-game-hub
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**:
    ```bash
    python main.py
    ```

##  Project Structure

```text
mini_game_hub/
├── main.py                  #  Application entry point
├── requirements.txt         #  Project dependencies
├── auth/                    #  Authentication logic & handlers
├── database/                #  Database connection & models
├── games/                   #  Game classes & logic
├── ui/                      #  User Interface components
└── utils/                   #  Helper functions & validators
```

## Screenshots



##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

##  License

This project is licensed under the MIT License - see the `LICENSE` file for details.
