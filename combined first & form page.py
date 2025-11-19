import pyautogui
import time
import os
import keyboard

# --- SETTINGS ---
# Image Names
PAY_BUTTON_IMAGE_NAME = 'pay_button2'  # MUST BE THE CLEAR IMAGE
UPI_IMAGE_NAME = 'upi'
FINAL_PAY_BUTTON_IMAGE_NAME = 'final_pay_button'
SCANNER_IMAGE_NAME = 'scanner'

# --- SETUP ---
script_dir = os.path.dirname(os.path.abspath(__file__))


def get_image_path(filename):
    """Robust path finder for .png or .PNG"""
    base = os.path.join(script_dir, filename)
    if os.path.exists(base): return base
    if filename.lower().endswith('.png'):
        alt = base[:-4] + ".PNG"
        if os.path.exists(alt): return alt
    # Fallback for just the name without extension
    if os.path.exists(base + ".png"): return base + ".png"
    if os.path.exists(base + ".PNG"): return base + ".PNG"
    return None


PAY_BUTTON_IMAGE = get_image_path(PAY_BUTTON_IMAGE_NAME)
UPI_IMAGE = get_image_path(UPI_IMAGE_NAME)
FINAL_PAY_BUTTON_IMAGE = get_image_path(FINAL_PAY_BUTTON_IMAGE_NAME)
SCANNER_IMAGE = get_image_path(SCANNER_IMAGE_NAME)


# --- LOGIC ---
def wait_and_click_indefinitely(image_path, description, wait_after=0.5, grayscale=False, confidence=0.9):
    if image_path is None:
        print(f"[ERROR] Could not find image file for {description}")
        return False

    print(f"[{description}] Searching...", end="\r")

    while not keyboard.is_pressed('esc'):
        try:
            # Locate center
            location = pyautogui.locateCenterOnScreen(
                image_path,
                confidence=confidence,
                grayscale=grayscale
            )

            if location:
                print(f"\n[SUCCESS] Match Found! Clicking {description}...")
                pyautogui.click(location)
                time.sleep(wait_after)
                return True

            # Optional: Slow down loop slightly to save CPU
            time.sleep(0.1)

        except Exception:
            time.sleep(0.1)

    print("\n[STOPPED] ESC pressed.")
    return False


# --- MAIN EXECUTION ---
print("\n--- PAYMENT ISOLATION TEST (STRICT MODE) ---")
print("1. Open your app to the payment page.")
print("2. Enter the OTP manually.")
print("3. The script should WAIT while the button is blurry.")
print("4. The script should CLICK immediately when the button becomes clear.")
print("------------------------------------------------")
print("Starting in 3 seconds...")
time.sleep(3)

# --- STEP 1: PAY BUTTON (Strict Color & Shape) ---
# grayscale=False : Forces the script to check the EXACT Green color.
# confidence=0.95 : Forces the script to check for SHARP edges (not blurry).
if wait_and_click_indefinitely(PAY_BUTTON_IMAGE, "Pay Button", wait_after=1.0, grayscale=False, confidence=0.95):

    # --- STEP 2: UPI BUTTON (Standard) ---
    # We relax the rules here because these buttons usually don't blur.
    if wait_and_click_indefinitely(UPI_IMAGE, "UPI Button", wait_after=1.0, grayscale=True, confidence=0.8):

        # --- STEP 3: FINAL PAY BUTTON ---
        if wait_and_click_indefinitely(FINAL_PAY_BUTTON_IMAGE, "Final Pay Button", wait_after=0.5, confidence=0.8):

            # --- STEP 4: SCANNER ---
            if wait_and_click_indefinitely(SCANNER_IMAGE, "Scanner", wait_after=0.1, confidence=0.8):
                print("\n--- TEST PASSED PERFECTLY ---")
            else:
                print("\n[FAILED] Could not find Scanner.")
        else:
            print("\n[FAILED] Could not find Final Pay Button.")
    else:
        print("\n[FAILED] Could not find UPI Button.")
else:
    print(f"\n[FAILED] Could not find Pay Button (Active State).")

print("\nPress ESC to exit.")
keyboard.wait('esc')