import os
import shutil
import multiprocessing
import time
import pyautogui
import pygetwindow
import threading
from mutagen import File

def organize_music(source_dirs, destination_dir):
    for source_dir in source_dirs:
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith(".mp3"):
                    file_path = os.path.join(root, file)
                    try:
                        audio = File(file_path, easy=True)
                        if audio.tags:
                            album = audio.tags.get("album", ["Unknown Album"])[0]
                            year = audio.tags.get("date", ["Unknown Year"])[0]
                            print(f"Found {file} from {file_path}")
                            print(f"{file} metadata Album: {album} Year: {year}")
                            destination_subdir = os.path.join(destination_dir, year, album)
                            try:
                                os.makedirs(destination_subdir, exist_ok=True)
                                if os.path.exists(destination_subdir):
                                    print(f"Directory created: {destination_subdir}")
                                else:
                                    print(f"Failed to create directory: {destination_subdir}")
                            except OSError as e:
                                print(f"Error creating directory")
                            destination_file = os.path.join(destination_subdir, file)
                            shutil.copy2(file_path, destination_file)
                            print(f"Copied {file} from {file_path} to {destination_file}")
                            print("")
                        else:
                            print(f"No tags found for {file_path}")
                            print("")
                    except Exception as e:
                        print(f"Error processing {file}: {e}")
                        print("")

def take_screenshot(interval, destination_dir, stop_event, x, y, width, height):
    screenshot_count = 0

    while not stop_event.is_set():
        screenshot_name = f"screenshot_{screenshot_count}.png"
        screenshot_path = os.path.join(destination_dir, screenshot_name)
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot.save(screenshot_path)
        print(f"Captured screenshot: {screenshot_path}")
        screenshot_count += 1
        time.sleep(interval)


if __name__ == "__main__":
    source_dirs = ["C:/Users/kevin/Desktop", "C:/Users/kevin/Documents"]
    destination_dir = "C:/Users/kevin/Music/Organized" 
    screenshot_dir = "C:/Users/kevin/Pictures/Evidencia"
    
    cmd_window = pygetwindow.getWindowsWithTitle('Command Prompt')[0]
    cmd_window.activate()
    x, y, width, height = cmd_window.left, cmd_window.top, cmd_window.width, cmd_window.height

    start_time = time.time()

    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)
    pool.apply_async(organize_music, (source_dirs, destination_dir))
    
    stop_event = threading.Event()
    interval = 0.2
    screenshot_thread = threading.Thread(target=take_screenshot, args=(interval, screenshot_dir, stop_event, x, y, width, height))
    screenshot_thread.start()

    pool.close()
    pool.join()
    end_time = time.time()
    total_time = end_time - start_time

    stop_event.set()
    screenshot_thread.join()

    print(f"Organizing music files complete.")
    print(f"Total run time: {total_time} seconds.")