# Smart Traffic Light Controller 🚦 (AI-Based)

This project simulates a real-time smart traffic light controller using **OpenCV**. It dynamically adjusts traffic signals based on vehicle density using video feeds from all four road directions.

---

## 📌 Features

- Detects and counts vehicles using background subtraction (OpenCV)
- Switches GREEN/RED lights based on real-time traffic density
- Changes signal if **no vehicle passes in 5 seconds**
- Overrides if one side is heavily congested
- Simulates traffic lights visually using colored indicators

---

## 📽️ Demo Layout

Video feeds:
- `north.mp4`
- `south.mp4`
- `east.mp4`
- `west.mp4`

**Simulated on-screen signal:**
- 🟢 Green when active
- 🔴 Red when inactive

---

## ⚙️ Technologies Used

- Python 3
- OpenCV (with bgsegm module)
- NumPy

---

## 🧠 Logic Flow

1. Detect moving vehicles using MOG background subtraction.
2. Count vehicles crossing a specific line.
3. If vehicle count is **low** or **none in 5 seconds**, switch signal.
4. Show live simulation with updated signal states.

---

## 🚀 Run This Project

```bash
[pip install opencv-contrib-python
python main.py]
(https://smarttrafficlightcontroller.netlify.app/)
```

---

## 📁 Folder Structure

```
smart-traffic-light-controller/
├── main.py
├── north.mp4
├── south.mp4
├── east.mp4
├── west.mp4
├── .gitignore
└── README.md
```

---

## 👨‍💻 Author

[Sweekar Subedi](https://github.com/sweekar18)
