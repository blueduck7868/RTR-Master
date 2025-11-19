import keyboard
import time
import random
import pyautogui
import os

# --- Import all user settings from the config.py file ---
from config import *

# ===================================================================
# --- SCRIPT LOGIC (DO NOT EDIT BELOW THIS LINE) ---
# ===================================================================

# --- Setup ---
SCROLL_AMOUNT = -500
script_dir = os.path.dirname(os.path.abspath(__file__))


# Robust path joining to handle .png vs .PNG case sensitivity
def get_image_path(filename):
    base = os.path.join(script_dir, filename)
    if os.path.exists(base): return base
    if filename.lower().endswith('.png'):
        alt = base[:-4] + ".PNG"
        if os.path.exists(alt): return alt
    return base


BUTTON_1_IMAGE = get_image_path(BUTTON_1_IMAGE_NAME)
CHECKBOX_IMAGE = get_image_path(CHECKBOX_IMAGE_NAME)
PHONE_BOX_IMAGE = get_image_path(PHONE_BOX_IMAGE_NAME)
PAY_BUTTON_IMAGE = get_image_path(PAY_BUTTON_IMAGE_NAME)
UPI_IMAGE = get_image_path(UPI_IMAGE_NAME)
FINAL_PAY_BUTTON_IMAGE = get_image_path(FINAL_PAY_BUTTON_IMAGE_NAME)
SCANNER_IMAGE = get_image_path(SCANNER_IMAGE_NAME)
CONTINUE_BUTTON_IMAGE = get_image_path(CONTINUE_BUTTON_IMAGE_NAME)


# --- Helper Functions ---

def find_and_click(image_path, description, wait_after=0.5, grayscale=False, confidence=0.9):
    """Standard single-pass image click with smart options."""
    try:
        location = pyautogui.locateCenterOnScreen(
            image_path,
            confidence=confidence,
            grayscale=grayscale
        )
        if location:
            pyautogui.click(location)
            time.sleep(wait_after)
            return True
        return False
    except Exception:
        return False


def wait_and_click_indefinitely(image_path, description, wait_after=0.5, grayscale=False, confidence=0.9):
    """Waits indefinitely for an image to appear."""
    print(f"[{description}] Searching...", end="\r")
    while not keyboard.is_pressed('esc'):
        try:
            if find_and_click(image_path, description, wait_after=wait_after, grayscale=grayscale,
                              confidence=confidence):
                print(f"\n[SUCCESS] Found and clicked {description}")
                return True

            # --- HIGH SPEED OPTIMIZATION ---
            time.sleep(0.05)

        except Exception:
            time.sleep(0.05)

    print("\n[STOPPED] ESC pressed.")
    return False


def ultra_human_type(text):
    for char in text:
        delay = random.uniform(0.03, 0.12)
        if char.isalpha() or char.isdigit():
            delay += random.uniform(0.05, 0.15)
        pyautogui.write(char)
        time.sleep(delay * FORM_PAGE_SPEED_MULTIPLIER)
    time.sleep(random.uniform(0.3, 0.5) * FORM_PAGE_SPEED_MULTIPLIER)


# --- NEW: HIGH SPEED TYPING FUNCTION ---
def instant_type(text):
    """Types text instantly (machine speed) without any human delay."""
    pyautogui.write(text)


def type_age_safely(age_text):
    print(f"[{age_text}] Typing Age (Safe Mode)...")
    for char in age_text:
        pyautogui.write(char)
        time.sleep(random.uniform(0.08, 0.2))
    time.sleep(0.5)


def paste_file_path_instantly(path_text):
    print(f"[{path_text}] Pasting File Path (Instant Mode)...")
    pyautogui.write(path_text)
    time.sleep(0.1)
    time.sleep(0.5)


def press_down(times):
    for _ in range(times):
        pyautogui.press('down')
        time.sleep(random.uniform(0.15, 0.3) * FORM_PAGE_SPEED_MULTIPLIER)
    time.sleep(random.uniform(0.4, 0.7) * FORM_PAGE_SPEED_MULTIPLIER)


def press_tab_human(count=1):
    for _ in range(count):
        pyautogui.press('tab')
        time.sleep(random.uniform(0.6, 1.0) * FORM_PAGE_SPEED_MULTIPLIER)


# --- State Management ---
class FormFillerState:
    def __init__(self): self.active = False; self.user_index = 0

    def toggle_active(self):
        self.active = not self.active
        status = "ACTIVATED" if self.active else "DEACTIVATED"
        print(f"\n--- Form Filler {status} ---")
        if self.active: print(f"Ready for User {self.user_index + 1}. Click NAME -> Press ALT+Q.")

    def reset(self): self.active = False; self.user_index = 0; print("--- RESET ---")


state = FormFillerState()


# --- Part 1 Logic (Tatkal Modes) ---
def execute_first_page_sequence():
    pyautogui.keyUp('alt');
    pyautogui.keyUp('1')

    print(f"\n[Part 1] Started. Mode: {WORK_MODE}")
    time.sleep(0.5)  # Focus delay

    if WORK_MODE == "Morning_Tatkal":
        # 2 Tabs -> Enter -> Tab -> 6 -> 2 Tabs -> 2 Enters
        for _ in range(2): keyboard.send('tab'); time.sleep(0.05)
        keyboard.send('enter');
        time.sleep(0.3)
        keyboard.send('tab');
        time.sleep(0.1)
        keyboard.write('6')
        time.sleep(0.1)
        for _ in range(2): keyboard.send('tab'); time.sleep(0.05)
        keyboard.send('enter');
        time.sleep(0.2)
        keyboard.send('enter');
        time.sleep(0.8)

    elif WORK_MODE == "Afternoon_Tatkal":
        # 3 Tabs -> Enter -> Tab -> 6 -> 2 Tabs -> 2 Enters
        for _ in range(3): keyboard.send('tab'); time.sleep(0.05)
        keyboard.send('enter');
        time.sleep(0.3)
        keyboard.send('tab');
        time.sleep(0.1)
        keyboard.write('6')
        time.sleep(0.1)
        for _ in range(2): keyboard.send('tab'); time.sleep(0.05)
        keyboard.send('enter');
        time.sleep(0.2)
        keyboard.send('enter');
        time.sleep(0.8)

    else:
        # Standard
        initial_tabs = 7 if WORK_MODE.upper() == "AFTERNOON" else 6
        for _ in range(initial_tabs): keyboard.send('tab'); time.sleep(0.05)
        keyboard.send('enter');
        time.sleep(0.3)
        keyboard.send('tab');
        time.sleep(0.1)
        keyboard.write(str(MANUAL_PAX_COUNT))
        if ARE_PAX_ONLY_INDIAN:
            time.sleep(0.1)
            for _ in range(4): keyboard.send('tab'); time.sleep(0.05)
            keyboard.send('enter');
            time.sleep(0.8)

    # --- Common End Sequence ---
    if find_and_click(BUTTON_1_IMAGE, "First Button"):
        pyautogui.scroll(SCROLL_AMOUNT);
        time.sleep(0.2)
        if find_and_click(CHECKBOX_IMAGE, "Checkbox", wait_after=0.1):
            keyboard.send('tab');
            time.sleep(0.05)
            keyboard.send('tab');
            time.sleep(0.05)
            keyboard.send('enter')
            print("[Part 1] Sequence Complete.")


# --- Part 2 Logic ---
def fill_complete_member_flow(user):
    ultra_human_type(user['name'].lower())
    press_tab_human()
    if user['gender'] == 'M':
        press_down(1)
    else:
        press_down(2)
    press_tab_human()
    type_age_safely(str(user['age']))
    press_tab_human()
    if user['nationality'] == 'I':
        press_down(1);
        press_tab_human()
        id_key = user['id_type_key']
        if id_key == 'A':
            press_down(1)
        elif id_key == 'P':
            press_down(2)
        elif id_key == 'PAN':
            press_down(3)
        elif id_key == 'V':
            press_down(4)
        elif id_key == 'S':
            press_down(5)
        press_tab_human()
        ultra_human_type(user['id'])
    else:
        press_down(2);
        press_tab_human(2);
        press_down(1);
        press_tab_human(1);
        ultra_human_type(user['id'])

    press_tab_human()
    pyautogui.press('enter')
    time.sleep(1.5)

    if 'id_file_path' in user and user['id_file_path']:
        paste_file_path_instantly(user['id_file_path'])
        time.sleep(random.uniform(0.3, 0.5))
        pyautogui.press('enter')
        time.sleep(random.uniform(1.5, 2.0))
    else:
        print(f"--> WARNING: No 'id_file_path' found for {user['name']}. Skipping.")
        pyautogui.press('esc')
        time.sleep(0.5)
    print(f"--> DONE: {user['name']}")


# --- Part 3 Logic (Continue -> Fast Payment) ---
def trigger_fill_next():
    if not state.active: return
    pyautogui.keyUp('alt');
    pyautogui.keyUp('q')

    if state.user_index >= MANUAL_PAX_COUNT:
        state.reset();
        return

    fill_complete_member_flow(USER_DATA[state.user_index])
    state.user_index += 1

    # --- THIS BLOCK EXECUTES ONCE ALL USERS ARE FILLED ---
    if state.user_index >= MANUAL_PAX_COUNT:

        # --- 1. CONTINUE BUTTON + ENTER ---
        print("\n[Sequence] All users filled. Looking for 'Continue' button...")
        if wait_and_click_indefinitely(CONTINUE_BUTTON_IMAGE, "Continue Button", wait_after=0.1):
            keyboard.send('enter')  # Fast Enter
            print("[Sequence] Clicked Continue + Pressed Enter.")

            # --- 2. PHONE NUMBER ---
            if wait_and_click_indefinitely(PHONE_BOX_IMAGE, "Phone Number Box"):
                instant_type(PHONE_NUMBER)  # Fast Type
                print("[Part 2] Finished.")

                if PERFORM_PAYMENT_PAGE:
                    print(f"\n[Part 3] Payment Page Started (Fast Mode)...")
                    print("--> Waiting for OTP verification (Active Button)...")

                    # --- 3. PAY BUTTON (STRICT WAIT) ---
                    if wait_and_click_indefinitely(PAY_BUTTON_IMAGE, "Pay Button", wait_after=0.1, grayscale=False,
                                                   confidence=0.95):

                        # --- 4. UPI BUTTON ---
                        if wait_and_click_indefinitely(UPI_IMAGE, "UPI Button", wait_after=0.1, grayscale=True,
                                                       confidence=0.8):

                            # --- 5. FINAL PAY BUTTON ---
                            if wait_and_click_indefinitely(FINAL_PAY_BUTTON_IMAGE, "Final Pay Button", wait_after=0.1,
                                                           confidence=0.8):

                                # --- 6. SCANNER ---
                                if wait_and_click_indefinitely(SCANNER_IMAGE, "Scanner", wait_after=0.1,
                                                               confidence=0.8):
                                    print("[Part 3] Payment Page Complete.")
                                else:
                                    print("[Part 3] FAILED: Could not find Scanner.")
                            else:
                                print("[Part 3] FAILED: Could not find Final Pay Button.")
                        else:
                            print("[Part 3] FAILED: Could not find UPI Button.")
                    else:
                        print("[Part 3] FAILED: Could not find Pay Button.")

                else:
                    print("\n[Part 3] Payment Page Skipped (as per config).")

        state.reset()
    else:
        print(f"\nReady for User {state.user_index + 1}. Click next NAME -> Press ALT+Q.")


# --- Main Execution Loop ---
if __name__ == "__main__":
    print("=== Automation Script Ready ===");
    print(f"| Configured for {MANUAL_PAX_COUNT} passengers.");
    print(f"| Mode: {WORK_MODE}");
    print("| ALT+1: Run First Page | ALT+2: Activate Filler | ALT+Q: Fill Next | ESC: Quit")
    keyboard.add_hotkey('alt+1', execute_first_page_sequence)
    keyboard.add_hotkey('alt+2', state.toggle_active)
    keyboard.add_hotkey('alt+q', trigger_fill_next)
    keyboard.wait('esc')
