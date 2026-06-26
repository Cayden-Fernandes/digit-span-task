# Digit Span Task – (PsychoPy Implementation)

This repository contains a **Digit Span Task** implemented in **PsychoPy (v2023.x)**.  
The task is designed for **academic and research use**, supporting age-based timing, optional audio presentation, and automatic data logging.

---

## 📌 Project Overview

The Digit Span Task measures short-term memory by presenting a sequence of digits that participants must recall **in the same order**. Digits are presented sequentially, followed by a response phase where participants type the digits they remember.

The system follows common neuropsychological conventions for example "WAIS/WISC", where digits are presented at approximately **one digit per second**, with controlled interstimulus intervals.

---

## ✨ Features

- Visual digit presentation (one digit at a time)
- Optional **audio-based presentation** using `.wav` files
- Age-based timing presets (Children → Clinical)
- No immediate repeated digits
- Ready screen before each trial
- Real-time response display with edit support
- Reaction time measurement
- Immediate feedback after each trial
- Automatic CSV data saving after every trial
- Fully offline operation

---

## 🧩 Default Task Configuration

- **Number of trials:** 10  
- **Sequence lengths:**  
[2, 2, 3, 3, 4, 4, 4, 5, 5, 5]

These values can be edited directly in the code to tailor to your needs.

---

## Installation

### 1. Install PsychoPy

The recommended way to install PsychoPy is using the standalone installer:

https://www.psychopy.org/download.html


# How to Use
## 1. Run the Experiment

- Open a terminal in the project directory and run:

digit-span-task.py

## 2. Enter Participant Information

When the program starts:

- Enter the participant ID and name

- Select the age group and gender

- Press OK to continue

## 3. Complete the Task

- Digits will be shown (or played) one at a time

- Memorise the digits in the order presented

- Type the digits using the keyboard

- Use Backspace to correct mistakes

- Press Enter to submit the response

- Feedback is shown after each trial

## 4. Data Output

- Data is saved automatically after every trial

- A CSV file is created in the Data/ folder

- The file name includes the participant ID and timestamp

- The save location is shown at the end of the experiment

# Disclaimer

This software is intended for educational and research purposes only.
It is not a clinical diagnostic tool.

