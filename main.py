import pyautogui
import time
import keyboard
import threading


def get_delay_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_clicks_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive integer.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


class AutoClicker:
    def __init__(self):
        self.delay = get_delay_input("Enter delay before starting (in seconds): ")
        self.num_clicks = get_clicks_input("Enter number of clicks to perform: ")
        self.click_delay = 0.5
        self.pause_key = 'shift'
        self.is_paused = False
        self.click_count = 0
        self.start_time = None
        self.elapsed_time = 0.0
        self.original_x, self.original_y = pyautogui.position()

    def start(self):
        print("Auto Clicker")
        print("--------------")

        print("Auto Clicker will start in {} seconds. Position your cursor accordingly.".format(self.delay))
        time.sleep(self.delay)

        # Moved the cursor position retrieval here
        self.original_x, self.original_y = pyautogui.position()
        print("Chosen mouse position: ({}, {})".format(self.original_x, self.original_y))

        print("Auto Clicker is running. Press '{}' to pause.".format(self.pause_key))

        self.start_time = time.time()

        keyboard.on_press_key(self.pause_key, self.toggle_pause)

        auto_clicker_thread = threading.Thread(target=self.auto_click)
        auto_clicker_thread.start()

        auto_clicker_thread.join()

        print("Auto Clicker Summary:")
        print("  Clicks performed: {}".format(self.click_count))
        print("  Elapsed time: {:.2f} seconds".format(self.elapsed_time))
        print("  Clicks per second: {:.2f}".format(self.click_count / self.elapsed_time))

    def auto_click(self):
        while self.click_count < self.num_clicks:
            if self.is_paused:
                time.sleep(0.1)
            else:
                pyautogui.moveTo(self.original_x, self.original_y)
                pyautogui.click()
                self.click_count += 1
                time.sleep(self.click_delay)
        self.elapsed_time = time.time() - self.start_time
        print("Auto Clicker completed.")

    def toggle_pause(self, _):
        self.is_paused = not self.is_paused
        if self.is_paused:
            print("Auto Clicker paused.")
        else:
            print("Auto Clicker resumed.")


if __name__ == "__main__":
    auto_clicker = AutoClicker()
    auto_clicker.start()
