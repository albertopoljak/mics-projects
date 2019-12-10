import win32gui
# Source http://timgolden.me.uk/python/win32_how_do_i/find-the-window-for-my-subprocess.html
# https://stackoverflow.com/questions/2598404/how-to-get-firefox-address-bar-url-for-python-pywin32


def print_hwnd_size(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print(f"Window {win32gui.GetWindowText(hwnd)}:")
    print(f"\tLocation: ({x}, {y})")
    print(f"\tSize: ({w}, {h})")


def enumeration_callaback(hwnd, results):
    text = win32gui.GetWindowText(hwnd)
    if text.find("Mozilla Firefox") >= 0:
        results.append(hwnd)


if __name__ == "__main__":
    my_windows = []
    win32gui.EnumWindows(enumeration_callaback, my_windows)
    for hwnd in my_windows:
        print_hwnd_size(hwnd)
