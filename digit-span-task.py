#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Digit Span Task - PsychoPy Implementation
Version: 1.1
Compatible from PsychoPy 2023.x
"""

from psychopy import visual, event, core, gui, data, sound
import random
import os
import datetime
import csv
from pathlib import Path

# *******************
# CONFIGURATION
# *******************
FULLSCREEN = False  # Set to True for fullscreen
WINDOW_SIZE = [800, 600]  # [width, height]
DATA_DIR = "Data"
FONT = "Arial"
FONT_SIZE = 36

# Age-based timing presets (seconds)
AGE_PRESETS = {
    "Children (6-8)": {"display": 1.0, "isi": 1.0, "response": 30},
    "Children (9-12)": {"display": 0.9, "isi": 0.8, "response": 25},
    "Adolescents (13-17)": {"display": 0.8, "isi": 0.7, "response": 20},
    "Adults (18-65)": {"display": 0.7, "isi": 0.7, "response": 15},
    "Older Adults (65+)": {"display": 1.0, "isi": 1.0, "response": 25},
    "Clinical": {"display": 1.2, "isi": 1.2, "response": 30}
}

# Trial sequence: You can adjust this based on your research needs.
TRIAL_SEQUENCE = [2, 2, 3, 3, 4, 4, 4, 5, 5, 5]

# Audio mode (set to False for visual-only)
AUDIO_MODE = False
AUDIO_FILES = {str(i): f"digit_{i}.wav" for i in range(10)}  # Pre-recorded files

# *******************
# DATA MANAGEMENT
# *******************
def create_data_file(participant_info):
    """Create timestamped CSV file with unique name"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"DigitSpan_{participant_info['ParticipantID']}_{timestamp}.csv"
    filepath = os.path.join(DATA_DIR, filename)
    
    # CSV headers
    headers = [
        "Timestamp", "ParticipantID", "Name", "AgeGroup", "Trial", 
        "SequenceLength", "PresentedDigits", "Response", 
        "Accuracy", "RT", "TimedOut", "TimingUsed", "AudioMode"
    ]
    
    # Create file with headers
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
    
    return filepath

def save_trial_data(filepath, trial_data):
    """Append trial data to CSV file"""
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.datetime.now().isoformat(),
            trial_data.get('participant_id', ''),
            trial_data.get('name', ''),  # Change this if Name is not required....
            trial_data.get('age_group', ''),
            trial_data.get('trial', 0),
            trial_data.get('sequence_length', 0),
            trial_data.get('presented_digits', ''),
            trial_data.get('response', ''),
            trial_data.get('accuracy', 0),
            trial_data.get('rt', 0),
            trial_data.get('timed_out', False),
            trial_data.get('timing_used', ''),
            trial_data.get('audio_mode', False)
        ])

# ********************
# TRIAL GENERATION
# ********************
def generate_digit_sequence(length, no_repeats=True):
    """Generate random digit sequence 0-9 with optional no repeats"""
    digits = list(range(10))
    sequence = []
    
    for _ in range(length):
        if not sequence or not no_repeats:
            digit = random.choice(digits)
        else:
            # Avoid immediate repeats
            available = [d for d in digits if d != sequence[-1]]
            digit = random.choice(available)
        sequence.append(digit)
    
    return sequence

# **********************
# STIMULI PRESENTATION
# **********************
def present_digits_visual(win, digits, display_time, isi_time):
    """Present digits visually one by one"""
    digit_text = visual.TextStim(win, text="", font=FONT, height=FONT_SIZE)
    
    for digit in digits:
        digit_text.text = str(digit)
        digit_text.draw()
        win.flip()
        core.wait(display_time)
        
        # ISI (blank screen)
        win.flip()
        core.wait(isi_time)

def present_digits_audio(win, digits, display_time, isi_time):
    """Present digits as audio files"""
    # Load audio files if available
    sounds = {}
    for i in range(10):
        filepath = AUDIO_FILES.get(str(i))
        if filepath and os.path.exists(filepath):
            sounds[str(i)] = sound.Sound(filepath)
    
    fixation = visual.TextStim(win, text="+", font=FONT, height=FONT_SIZE)
    
    for digit in digits:
        # Show fixation during audio
        fixation.draw()
        win.flip()
        
        # Play audio
        audio_key = str(digit)
        if audio_key in sounds:
            sounds[audio_key].play()
            core.wait(display_time)
        else:
            # Fallback to visual if audio missing
            visual_text = visual.TextStim(win, text=str(digit), font=FONT, height=FONT_SIZE)
            visual_text.draw()
            win.flip()
            core.wait(display_time)
        
        # ISI (silent gap)
        win.flip()
        core.wait(isi_time)

# *******************
# RESPONSE HANDLING
# *******************
def collect_response(win, max_time, presented_digits):
    """Collect numeric response with real-time display"""
    response = []
    start_time = core.getTime()
    response_text = visual.TextStim(win, text="", font=FONT, height=FONT_SIZE, pos=(0, -100))
    prompt = visual.TextStim(win, text="Type the digits you saw (press Enter when done):", 
                             font=FONT, height=24, pos=(0, 50))
    timer_text = visual.TextStim(win, text="", font=FONT, height=24, pos=(0, 150))
    
    clock = core.Clock()
    
    while True:
        # Calculate remaining time
        elapsed = core.getTime() - start_time
        remaining = max(0, max_time - elapsed)
        
        # Check for timeout
        if remaining <= 0:
            return {"response": "", "rt": max_time, "timed_out": True}
        
        # Update display
        prompt.draw()
        response_text.text = " ".join(response) if response else "---"
        response_text.draw()
        timer_text.text = f"Time remaining: {remaining:.1f}s"
        timer_text.draw()
        win.flip()
        
        # Check for keypress
        keys = event.getKeys(keyList=['0','1','2','3','4','5','6','7','8','9',
                                      'backspace', 'delete', 'return', 'enter', 'x'])
        
        for key in keys:
            if key in ['x', 'escape']:
                # Exit session
                win.close()
                core.quit()
                
            elif key in ['backspace', 'delete']:
                if response:
                    response.pop()
                    
            elif key in ['return', 'enter']:
                rt = core.getTime() - start_time
                response_str = "".join(response)
                return {"response": response_str, "rt": rt, "timed_out": False}
                
            elif key.isdigit() and len(response) < len(presented_digits):
                response.append(key)
                # Real-time update happens in next loop iteration

# *******************
# FEEDBACK DISPLAY
# *******************
def show_trial_feedback(win, presented_digits, response_str, is_correct, trial_num, total_trials):
    """Show feedback after each trial"""
    
    # Determine feedback color and message
    if is_correct:
        color = "green"
        result_text = "CORRECT! ✓"
    else:
        color = "red"
        result_text = "INCORRECT ✗"
    
    # Create feedback display
    feedback_text = visual.TextStim(win, text=result_text, 
                                    font=FONT, height=48, color=color, pos=(0, 100))
    
    # Show what was presented vs what was entered
    presented_text = visual.TextStim(win, 
                                     text=f"Sequence: {' '.join(str(d) for d in presented_digits)}",
                                     font=FONT, height=28, pos=(0, 30))
    
    response_text = visual.TextStim(win, 
                                    text=f"Your answer: {' '.join(response_str) if response_str else '(no response)'}",
                                    font=FONT, height=28, pos=(0, -10))
    
    # Trial progress
    progress_text = visual.TextStim(win, 
                                    text=f"Trial {trial_num} of {total_trials}",
                                    font=FONT, height=24, pos=(0, -70))
    
    # Continue prompt
    continue_text = visual.TextStim(win, 
                                    text="Press any key to continue",
                                    font=FONT, height=20, pos=(0, -120))
    
    # Draw all elements
    feedback_text.draw()
    presented_text.draw()
    response_text.draw()
    progress_text.draw()
    continue_text.draw()
    
    win.flip()
    event.waitKeys()  # Wait for any key press
    win.flip()  # Clear screen
    core.wait(0.3)  # Brief pause before next trial

# *******************
# MAIN EXPERIMENT
# *******************
def run_experiment():
    # Collect participant info with dropdown for AgeGroup
    participant_info = {
        "ParticipantID": "",
        "Name": "",
        "AgeGroup": list(AGE_PRESETS.keys())[3],  # Default to Adults
        "Gender": ["Male", "Female", "Other", "Prefer not to say"]
    }
    
    # Create custom dialog with dropdown for AgeGroup
    info_dlg = gui.Dlg(title="Participant Information", size=(500, 400))
    
    # Add fields with appropriate input types
    info_dlg.addField('Participant ID:', participant_info["ParticipantID"])
    info_dlg.addField('Name:', participant_info["Name"])
    
    # Add dropdown for AgeGroup with all preset options
    info_dlg.addField('Age Group:', 
                     initial=participant_info["AgeGroup"],
                     choices=list(AGE_PRESETS.keys()))
    
    # Add dropdown for Gender
    info_dlg.addField('Gender:', 
                     initial=participant_info["Gender"][0],
                     choices=participant_info["Gender"])
    
    # Show dialog
    dlg_data = info_dlg.show()
    
    if not info_dlg.OK:
        print("Experiment cancelled")
        return
    
    # Extract data from dialog
    participant_info["ParticipantID"] = dlg_data[0]
    participant_info["Name"] = dlg_data[1]
    participant_info["AgeGroup"] = dlg_data[2]
    participant_info["Gender"] = dlg_data[3]
    
    # Create window
    win = visual.Window(
        size=WINDOW_SIZE,
        fullscr=FULLSCREEN,
        monitor="testMonitor",
        units="pix",
        color="black"
    )
    
    # Create data file
    data_file = create_data_file(participant_info)
    
    # Get timing for selected age group
    timing = AGE_PRESETS[participant_info["AgeGroup"]]
    
    # Instructions
    instructions = visual.TextStim(win, 
        text=("DIGIT SPAN TASK\n\n"
              "You will see a sequence of numbers.\n"
              "Remember them in the order shown.\n"
              "After the sequence, type the numbers\n"
              "in the same order.\n\n"
              "Use number keys to type.\n"
              "Backspace to correct mistakes.\n"
              "Press Enter to submit.\n\n"
              "You will see feedback after each trial.\n\n"
              "Press any key to begin."),
        font=FONT, height=24, wrapWidth=700)
    instructions.draw()
    win.flip()
    event.waitKeys()
    
    # Initialize scoring
    total_correct = 0
    total_trials = len(TRIAL_SEQUENCE)
    trial_results = []
    
    # Run trials
    for trial_num, seq_length in enumerate(TRIAL_SEQUENCE, 1):
        # Ready screen
        ready = visual.TextStim(win, text="Ready?", font=FONT, height=36)
        ready.draw()
        win.flip()
        core.wait(1.0)
        
        # Generate digit sequence
        sequence = generate_digit_sequence(seq_length, no_repeats=True)
        seq_str = "".join(map(str, sequence))
        
        # Present digits
        if AUDIO_MODE:
            present_digits_audio(win, sequence, timing["display"], timing["isi"])
        else:
            present_digits_visual(win, sequence, timing["display"], timing["isi"])
        
        # Collect response
        response_data = collect_response(win, timing["response"], sequence)
        
        # Score response
        presented_str = "".join(map(str, sequence))
        response_str = response_data["response"]
        
        # Preserve exact order (no regrouping)
        is_correct = presented_str == response_str
        accuracy = 1 if is_correct else 0
        total_correct += accuracy
        
        # Prepare trial data
        trial_data = {
            'participant_id': participant_info['ParticipantID'],
            'name': participant_info['Name'],  # Remove this if Name is not needed.
            'age_group': participant_info['AgeGroup'],
            'trial': trial_num,
            'sequence_length': seq_length,
            'presented_digits': seq_str,
            'response': response_str,
            'accuracy': accuracy,
            'rt': response_data['rt'],
            'timed_out': response_data['timed_out'],
            'timing_used': f"{timing['display']}/{timing['isi']}/{timing['response']}",
            'audio_mode': AUDIO_MODE
        }
        
        # Auto-save after each trial
        save_trial_data(data_file, trial_data)
        trial_results.append(trial_data)
        
        # Show feedback after each trial
        show_trial_feedback(win, sequence, response_str, is_correct, trial_num, total_trials)
        
        # Brief pause between trials (already included in feedback function)
    
    # Calculate final score
    score_percent = (total_correct / total_trials) * 100
    
    # Show final score
    score_text = visual.TextStim(win,
        text=(f"TEST COMPLETE\n\n"
              f"Your score: {total_correct} out of {total_trials} correct\n"
              f"Accuracy: {score_percent:.1f}%\n\n"
              f"Press any key to continue."),
        font=FONT, height=28, wrapWidth=700)
    score_text.draw()
    win.flip()
    event.waitKeys()
    
    # Show data save location 
    save_info = visual.TextStim(win,
        text=(f"Data saved to:\n{data_file}\n\n"
              f"Thank you for participating!\n\n"
              f"Press any key to exit."),
        font=FONT, height=24, wrapWidth=700)
    save_info.draw()
    win.flip()
    event.waitKeys()
    
    win.close()

# *******************
# ENTRY POINT
# *******************
if __name__ == "__main__":
    try:
        run_experiment()
    except Exception as e:
        print(f"Error occurred: {e}")
        input("Press Enter to exit...")