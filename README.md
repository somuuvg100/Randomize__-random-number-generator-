# Randomize 🎲

A sleek, modern Random Number Generator application that provides both a **Web Interface** and a **Desktop GUI**. 

🚀 **Live Web App:** [https://randomize-random-number-generator.vercel.app/](https://randomize-random-number-generator.vercel.app/)

Created by **Somashankar**.

---

## 🌟 Features

- **Dual Interfaces**: Choose between a modern, responsive web application or a clean desktop GUI.
- **Range Selection**: Easily specify custom minimum and maximum values.
- **Instant Generation**: Generate random integers instantly within your chosen range.
- **History Tracking**: Keeps track of your recently generated numbers for quick reference.
- **Copy to Clipboard**: One-click copying of generated results.
- **Sleek UI**: Beautifully designed with rounded corners, subtle shadows, and a modern aesthetic.

---

## 💻 Desktop Application (Tkinter)

The desktop app is built using Python's built-in `tkinter` library, meaning it runs quickly and smoothly with no heavy dependencies.

### Prerequisites
- Python 3.x

### How to Run
Simply execute the following command in your terminal:
```bash
python random_ui_tkinter.py
```

---

## 🌐 Web Application (Flask)

The web application is built using Python's `Flask` framework for the backend, and vanilla HTML/CSS/JS for the frontend.

### Prerequisites
- Python 3.x
- Flask (`pip install Flask`)

### How to Run
1. Install Flask if you haven't already:
   ```bash
   pip install Flask
   ```
2. Start the web server:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to `http://localhost:5000` or `http://127.0.0.1:5000`.

---

## 📁 Project Structure

```text
Randomize/
│
├── app.py                   # Flask server script for the web app
├── random_ui_tkinter.py     # Script to launch the desktop application
├── logo.png                 # Application logo (desktop)
│
├── static/                  # Static assets for the web app
│   ├── style.css            # Stylesheet for web UI
│   ├── script.js            # Interactivity for web UI
│   └── logo.png             # Application logo (web)
│
└── templates/               # HTML templates for Flask
    └── index.html           # Main web page
```

---

## 🛠️ Built With

- **Python**: Core logic and server backend.
- **Flask**: Web framework.
- **Tkinter**: Desktop GUI framework.
- **HTML/CSS/JS**: Frontend for the web interface.

---

*© Somashankar - All rights reserved.*
