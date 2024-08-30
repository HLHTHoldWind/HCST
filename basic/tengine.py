import googletrans as tran
import keyboard
from httpcore import SyncHTTPProxy
import time
import pyperclip
import os
import urllib
import threading
import basic.window as window
from basic.constants import *
from basic.lang import LANG

BASE_PATH = CONFIG["CONFIG"]["cs_path"] + "\\game\\csgo"

LOG_PATH = f"{BASE_PATH}\\csdm\\console.log"
if not os.path.exists(f"{BASE_PATH}\\csdm"):
    print("INGAME MODE")
    LOG_PATH = f"{BASE_PATH}\\console.log"
else:
    print("DEMO MODE")

KEY_W = ["[ALL]", "[CT]", "[T]"]

proxies = urllib.request.getproxies()

if CONFIG["PROXY"]["enabled"] == "true":
    if CONFIG["PROXY"]["mode"] == "auto":
        h_address = proxies["http"]
    else:
        h_address = CONFIG["PROXY"]["url"]

    head = h_address.split("//")[0].rstrip(":")
    a_p = h_address.split("//")[1]
    address = a_p.split(":")[0]
    port = a_p.split(":")[1]

    http_proxy = SyncHTTPProxy((head.encode(), address.encode(), int(port), b''))
    proxies = {'http': http_proxy, 'https': http_proxy}
    trans = tran.Translator(service_urls=[CONFIG["CONFIG"]["url"]], proxies=proxies)
else:
    trans = tran.Translator(service_urls=[CONFIG["CONFIG"]["url"]])

t_dsc = CONFIG["LANGUAGE"]["dst"]
t_dsc2 = "zh-tw"
in_game = CONFIG["LANGUAGE"]["in_game"]


def convert_en(string: str):
    translated = trans.translate(string, dest=t_dsc)
    # translated2 = trans.translate(string, dest=t_dsc2)
    translated2 = translated
    if translated2.src != in_game:
        translated3 = trans.translate(string, src=in_game, dest=t_dsc)
    else:
        translated3 = translated2

    return translated, translated2, translated3


def translate(string):
    try:
        translated = trans.translate(string, dest=in_game)

        text = translated.text
        return text
    except ValueError:
        return ""


def self_translation():
    while True:
        if keyboard.is_pressed(CONFIG["SHORTCUT"]["strans"]):
            keyboard.press_and_release("Ctrl+a")
            keyboard.press_and_release("Ctrl+c")
            time.sleep(0.05)
            text = pyperclip.paste()
            content = translate(text)
            pyperclip.copy(content)
            keyboard.press_and_release("Ctrl+v")

        time.sleep(0.1)


def core(root: window.MainWindow):
    global in_game, t_dsc
    content = ["awa"]
    tran_lines = []
    if not os.path.exists(BASE_PATH):
        root.addtext(LANG["error.game_root"], COLORS.RED)
    if not os.path.exists(LOG_PATH):
        root.addtext(LANG["error.game_log"], COLORS.RED)
    while True:
        with open(LOG_PATH, "rb") as file:
            f_content = file.readlines()
            try:
                if content[-1] != f_content[-1]:
                    new_lines = f_content[len(content):]
                    content = f_content

                    for i in new_lines:
                        for x in KEY_W:
                            side = ""+x
                            try:
                                texts = i.decode()
                                if x in texts:
                                    text = ""
                                    for a in texts.split(": ")[1:]:
                                        text += a
                                    title = texts.split(": ")[0]
                                    text = text.rstrip()
                                    t_dsc = CONFIG["LANGUAGE"]["dst"]
                                    in_game = CONFIG["LANGUAGE"]["in_game"]

                                    if CONFIG["CONFIG"]["username"] in title:
                                        if "/cmd" in text:
                                            command = text.split(" ")[1]
                                            if command == "set_lang":
                                                lang = text.split(" ")[2].strip().lower()
                                                if lang in LANGUAGE_CODES.keys():
                                                    lang = LANGUAGE_CODES[lang]
                                                in_game = lang
                                                CONFIG["LANGUAGE"]["in_game"] = lang
                                                with open(f"{LOCAL_PATH}\\config.ini", "w") as config_f:
                                                    CONFIG.write(config_f)
                                        t_content = translate(text)
                                        pyperclip.copy(t_content)
                                        tran_text = title + ": " + text + "\n" + t_content
                                        print(tran_text)
                                        if side == "[CT]":
                                            color = COLORS.LIGHT_BLUE
                                        elif side == "[T]":
                                            color = COLORS.LIGHT_YELLOW
                                        else:
                                            color = COLORS.LIGHT_GREEN
                                        _title = "[" + title.split("[")[1]
                                        if "﹫" in _title and side != "[ALL]":
                                            t1 = "".join(_title.split("﹫")[:-1])
                                            t2 = "﹫"+_title.split("﹫")[-1]
                                            root.addtext(t1, color)
                                            root.addtext(t2, COLORS.LIGHT_GREEN)
                                        else:
                                            root.addtext(_title, color)
                                        root.addtext(": "+text+"\n", COLORS.NONE)
                                        root.addtext(f"({t_content})\n", COLORS.LIGHT_GRAY)

                                    else:

                                        tran1, tran2, tran3 = convert_en(text)
                                        tran_text = f"{title} (From {tran1.src}): {tran1.text}\n{tran2.text}\n{tran3.text}"

                                        tran_lines.append(tran_text)
                                        print(tran_text)
                                        if side == "[CT]":
                                            color = COLORS.LIGHT_BLUE
                                        elif side == "[T]":
                                            color = COLORS.LIGHT_YELLOW
                                        else:
                                            color = COLORS.LIGHT_GREEN

                                        _title = "[" + title.split("[")[1]
                                        if "﹫" in _title and side != "[ALL]":
                                            t1 = "".join(_title.split("﹫")[:-1])
                                            t2 = "﹫" + _title.split("﹫")[-1]
                                            root.addtext(t1, color)
                                            root.addtext(t2, COLORS.LIGHT_GREEN)
                                            root.addtext(f"(Probably from {tran1.src})", color)
                                        else:
                                            root.addtext(f"{_title}(Probably from {tran1.src})", color)
                                        root.addtext(f": {text}\n", COLORS.NONE)
                                        root.addtext(f"({tran1.text})\n", COLORS.LIGHT_GRAY)
                                        root.addtext(f"{in_game}->({tran3.text})\n", COLORS.LIGHT_GRAY)
                            except:
                                continue
            except IndexError:
                content = ["awa"]
                tran_lines = []
                continue

        time.sleep(1)


"""if __name__ == '__main__':
    threading.Thread(target=self_translation).start()
    test("HoldWind")"""
