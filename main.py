from basic.tengine import *
from basic.window import *


def view_toggle_fast(root: MainWindow):
    while True:
        if keyboard.is_pressed(CONFIG["SHORTCUT"]["toggle"]):
            while keyboard.is_pressed(CONFIG["SHORTCUT"]["toggle"]):
                time.sleep(0.02)
            root.withdraw()
            while not keyboard.is_pressed(CONFIG["SHORTCUT"]["toggle"]):
                time.sleep(0.02)
            while keyboard.is_pressed(CONFIG["SHORTCUT"]["toggle"]):
                time.sleep(0.02)
            root.deiconify()
        time.sleep(0.02)


def main():
    threading.Thread(target=self_translation).start()
    root = MainWindow()
    threading.Thread(target=core, args=(root, )).start()
    threading.Thread(target=view_toggle_fast, args=(root, )).start()
    root.mainloop()


if __name__ == "__main__":
    main()
