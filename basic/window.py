import time
from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import *

from ttkbootstrap import *
import ttkbootstrap.scrolled as scrolled

from basic.lang import *
from basic.constants import *

from PIL import Image, ImageTk
import mouse
import keyboard
import os
import ctypes

winapi = ctypes.windll.user32
trueWidth = winapi.GetSystemMetrics(0)

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ZOOM = round((winapi.GetSystemMetrics(0) / trueWidth) + (0.1 * ((winapi.GetSystemMetrics(0) / trueWidth) / 2)), 1)

IMG_CACHE = []


class MainWindow(Window):
    def __init__(self):
        Window.__init__(self, themename="sandstone")
        self.withdraw()
        if CONFIG.has_option("WINDOW", "pos"):
            pos = CONFIG["WINDOW"]["pos"]
        else:
            pos = None

        self.x = self.winfo_x()
        self.y = self.winfo_y()
        self.title_showed = BooleanVar(self)
        self.title_showed.set(True)

        win_height = winapi.GetSystemMetrics(1)
        height = round(win_height * 0.46)
        windowInit(self, int(height * 0.75 // ZOOM * 2), height // ZOOM, False, LANG["main.title"],
                   "assets\\icons\\ctrans.ico")
        self.overrideredirect(True)

        cross = ImageTk.PhotoImage(Image.open("assets\\bitmaps\\Cross_Mark.png").resize((zoom(16), zoom(16))))
        setting = ImageTk.PhotoImage(Image.open("assets\\bitmaps\\setting.png").resize((zoom(16), zoom(16))))
        icon = ImageTk.PhotoImage(Image.open("assets\\icons\\ctrans.ico").resize((zoom(16), zoom(16))))
        IMG_CACHE.append(cross)
        IMG_CACHE.append(icon)
        IMG_CACHE.append(setting)

        self.configure(background="#1b1b1b")

        self.Style = Style()

        self.Style.configure("close.info.Link.TButton", font=("FreeSans", "10"))
        # self.Style.configure("title.TLabel", font=("FreeSans", "16"))

        self.titleFrame = Frame(self)
        self.titleFrame.bind("<ButtonPress-1>", self.StartMove)
        self.titleFrame.bind("<ButtonRelease-1>", self.StopMove)
        self.titleFrame.bind("<B1-Motion>", self.OnMotion)
        self.iconLabel = Label(self.titleFrame, image=icon)
        self.titleLabel = Label(self.titleFrame, text=LANG["main.title"])
        self.closeButton = Button(self.titleFrame, image=cross, command=self.close, style="close.info.Link.TButton")
        self.configButton = Button(self.titleFrame, image=setting,
                                   command=self.setting, style="close.info.Link.TButton")
        self.console = ScrollText(self)
        self.console.text["state"] = "disabled"

        self.iconLabel.bind("<ButtonPress-1>", self.StartMove)
        self.iconLabel.bind("<ButtonRelease-1>", self.StopMove)
        self.iconLabel.bind("<B1-Motion>", self.OnMotion)
        self.titleLabel.bind("<ButtonPress-1>", self.StartMove)
        self.titleLabel.bind("<ButtonRelease-1>", self.StopMove)
        self.titleLabel.bind("<B1-Motion>", self.OnMotion)

        def detect_in():
            while True:
                m_x, m_y = mouse.get_position()
                w_x, w_y = self.winfo_width(), self.winfo_height()
                _x, _y = self.winfo_x(), self.winfo_y()

                if _x < m_x < _x+w_x and _y < m_y < _y+w_y and (not self.title_showed.get()):
                    self.show_title()

                elif not (_x < m_x < _x+w_x and _y < m_y < _y+w_y):
                    if self.title_showed.get():
                        self.forget_title()

                time.sleep(0.05)

        def topMost():
            while True:
                self.attributes('-topmost', True)
                self.lift()
                time.sleep(0.01)

        def resize_loop():
            while True:
                new_zoom = round(
                    (winapi.GetSystemMetrics(0) / trueWidth) + (0.1 * ((winapi.GetSystemMetrics(0) / trueWidth) / 2)),
                    1)

                def _zoom(integer):
                    return round(integer * new_zoom)

                self.configure(width=_zoom(600), height=_zoom(400))
                self.iconLabel.place(x=_zoom(0), y=_zoom(0), width=_zoom(25), height=_zoom(25))
                self.titleLabel.place(x=_zoom(25), y=_zoom(0), width=_zoom(200), height=_zoom(25))
                self.closeButton.place(x=_zoom(560), y=_zoom(0), width=_zoom(40), height=_zoom(25))
                self.configButton.place(x=_zoom(500), y=_zoom(0), width=_zoom(40), height=_zoom(25))
                self.console.place(x=_zoom(0), y=_zoom(25), width=_zoom(600), height=_zoom(340))
                if self.title_showed.get():
                    self.titleFrame.place(x=_zoom(0), y=_zoom(0), width=_zoom(600), height=_zoom(25))
                time.sleep(0.5)

        Thread(target=topMost).start()
        self.attributes("-transparentcolor", "#1b1b1b")

        set_appwindow(self)
        self.protocol("WM_DELETE_WINDOW", self.close)
        if pos is not None:
            x, y = pos.split(",")

            self.geometry(f"+{x}+{y}")

        else:
            middle(self, int(height * 0.75 // ZOOM), height // ZOOM)

        self.deiconify()
        Thread(target=resize_loop).start()
        Thread(target=detect_in).start()

    def setting(self):
        self.focus_set()
        view = ConfigWindow(self)
        view.mainloop()

    def show_title(self, event=None):
        self.title_showed.set(True)
        new_zoom = round(
            (winapi.GetSystemMetrics(0) / trueWidth) + (0.1 * ((winapi.GetSystemMetrics(0) / trueWidth) / 2)),
            1)

        def _zoom(integer):
            return round(integer * new_zoom)
        self.console.show_scrollbars()
        self.bind_all("<MouseWheel>", self.console.redirect_yscroll_event)
        self.titleFrame.place(x=_zoom(0), y=_zoom(0), width=_zoom(300), height=_zoom(25))

    def forget_title(self, event=None):
        self.title_showed.set(False)
        self.console.hide_scrollbars()
        self.unbind_all("<MouseWheel>")
        self.titleFrame.place_forget()

    def StartMove(self, event=None):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event=None):
        self.x = self.winfo_x()
        self.y = self.winfo_y()

    def OnMotion(self, event=None):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))

    def addtext(self, text: str, color=COLORS.NONE):
        self.console.text["state"] = "normal"
        self.console.text.insert("end", text, color.color_code)
        self.console.text["state"] = "disabled"
        self.console.cyview("end")

    def close(self):
        self.focus_set()
        pos = f"{self.winfo_x()},{self.winfo_y()}"
        if CONFIG.has_option("WINDOW", "pos"):
            CONFIG["WINDOW"]["pos"] = pos
        else:
            CONFIG.add_section("WINDOW")
            CONFIG["WINDOW"]["pos"] = pos

        with open(f"{LOCAL_PATH}\\config.ini", "w") as config_f:
            CONFIG.write(config_f)

        self.destroy()
        os._exit(0)


class ConfigWindow(Toplevel):

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.withdraw()
        windowInit(self, 400, 500, False, LANG["main.setting"],
                   "assets\\icons\\ctrans.ico")

        middle(self, zoom(400), zoom(500))
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.Style = Style()
        self.Style.configure("normal.secondary.Link.TButton", focusthickness=0, relief="flat")
        self.Style.configure("normal.TLabel", font=("arial", "10"))
        self.Style.configure("redtip.danger.TLabel", font=("arial", "6"), )
        self.Style.configure("e.info.TLabel", anchor="e", font=("arial", "15", "bold"))
        self.Style.configure("green.success.Roundtoggle.Toolbutton", font=("arial", "10"))

        self.basic_frame = LabelFrame(self, text=LANG["config.basic"])
        self.language_frame = LabelFrame(self, text=LANG["config.lang"])
        self.proxy_frame = LabelFrame(self, text=LANG["config.proxy"])
        self.shortcut_frame = LabelFrame(self, text=LANG["config.shortcut"])

        self.ui_lang_frame = Frame(self.basic_frame)
        self.ui_lang_tip = Label(self.ui_lang_frame, text=LANG["config.ui_lang"]+"*", style="normal.TLabel")
        langs = list(LANG_DICT.keys())
        self.ui_lang_box = Combobox(self.ui_lang_frame, values=langs)
        self.ui_lang_box.bind("<<ComboboxSelected>>", self.change_lang)
        self.ui_lang_box.current(langs.index(LANG["language_name"]))

        self.cs_path_frame = Frame(self.basic_frame)
        self.cs_path_tip = Label(self.cs_path_frame, text=LANG["config.game_path"]+"*", style="normal.TLabel")
        self.path = CONFIG["CONFIG"]["cs_path"]
        self.cs_path_box = Entry(self.cs_path_frame)
        self.cs_path_btn = Button(self.cs_path_frame, command=self.select_cs_path,
                                  text=LANG["config.game_path.btn"], style="normal.info.Link.TButton")
        self.cs_path_box.insert(END, self.path)
        self.cs_path_box.config(state="disabled")

        self.dst_frame = Frame(self.language_frame)
        self.dst_tip = Label(self.dst_frame, text=LANG["config.dst_lang"], style="normal.TLabel")
        self.dst_box = Entry(self.dst_frame)
        self.dst_box.insert(END, CONFIG["LANGUAGE"]["dst"])

        self.ing_frame = Frame(self.language_frame)
        self.ing_tip = Label(self.ing_frame, text=LANG["config.default_lang"], style="normal.TLabel")
        self.ing_box = Entry(self.ing_frame)
        self.ing_box.insert(END, CONFIG["LANGUAGE"]["in_game"])

        self.stran_frame = Frame(self.shortcut_frame)
        self.stran_tip = Label(self.stran_frame, text=LANG["config.shortcut.selftrans"], style="normal.TLabel")
        self.stran_box = Entry(self.stran_frame)
        self.stran_box.insert(END, CONFIG["SHORTCUT"]["strans"])

        self.tog_frame = Frame(self.shortcut_frame)
        self.tog_tip = Label(self.tog_frame, text=LANG["config.shortcut.toggle"], style="normal.TLabel")
        self.tog_box = Entry(self.tog_frame)
        self.tog_box.insert(END, CONFIG["SHORTCUT"]["toggle"])

        self.pxy_frame = Frame(self.proxy_frame)
        self.pxy_bool = BooleanVar(self)
        self.pxy_bool.set(True) if CONFIG["PROXY"]["enabled"] == "true" else self.pxy_bool.set(False)
        self.pxy_chk = Checkbutton(self.pxy_frame, style="success.Roundtoggle.Toolbutton", command=self.set_proxy,
                                   text=LANG["config.proxy.enable"]+"*", variable=self.pxy_bool)
        self.pxy_bool_auto = BooleanVar(self)
        self.pxy_bool_auto.set(True) if CONFIG["PROXY"]["mode"] == "auto" else self.pxy_bool_auto.set(False)
        self.pxy_chk_auto = Checkbutton(self.pxy_frame, style="success.Roundtoggle.Toolbutton",
                                        command=self.set_proxy_auto,
                                        text=LANG["config.proxy.auto"]+"*", variable=self.pxy_bool_auto)

        self.pxy_entry = Entry(self.pxy_frame)
        self.pxy_entry_tip = Label(self.pxy_frame, text=LANG["config.proxy.url"]+"*", style="normal.TLabel")
        self.pxy_entry.insert(END, CONFIG["PROXY"]["url"])

        self.refresh_chk()

        self.thanks_frame = Frame(self)
        thanks_tk = ImageTk.PhotoImage(Image.open("assets\\bitmaps\\07222024_1.png").resize((zoom(100), zoom(100))))
        self.thanks_tip = Label(self.thanks_frame, text="Thanks for your support", style="e.info.TLabel")
        self.thanks_tip2 = Label(self.thanks_frame, text="made by HoldWind", style="normal.TLabel")
        self.thanks_img = Label(self.thanks_frame, image=thanks_tk)
        IMG_CACHE.append(thanks_tk)

        self.gpowered_frame = Frame(self)
        gpowered_tk = ImageTk.PhotoImage(Image.open("assets\\bitmaps\\gpowered.png").resize((zoom(150), zoom(35))))
        self.gpowered_img = Label(self.gpowered_frame, image=gpowered_tk)
        IMG_CACHE.append(gpowered_tk)

        self.misc_frame = LabelFrame(self, text=LANG["config.misc"])
        self.id_frame = Frame(self.misc_frame)
        self.id_tip = Label(self.id_frame, text=LANG["config.account_name"], style="normal.TLabel")
        self.id_box = Entry(self.id_frame)
        self.id_box.insert(END, CONFIG["CONFIG"]["username"])

        self.url_frame = Frame(self.misc_frame)
        self.url_tip2 = Label(self.url_frame, text=LANG["config.custom_url.tip"], style="redtip.danger.TLabel")
        self.url_tip = Label(self.url_frame, text=LANG["config.custom_url"]+"*", style="normal.TLabel")

        self.url_box = Entry(self.url_frame)
        self.url_box.insert(END, CONFIG["CONFIG"]["url"])

        self.star_tip = Label(self, text=LANG["config.restart.tip"], style="warning.TLabel")

        self.basic_frame.place(x=zoom(25), y=zoom(5), width=zoom(345), height=zoom(75))
        self.ui_lang_frame.place(x=zoom(0), y=zoom(0), width=zoom(340), height=zoom(25))
        self.cs_path_frame.place(x=zoom(0), y=zoom(30), width=zoom(340), height=zoom(25))

        self.ui_lang_tip.place(x=zoom(0), y=zoom(0), width=zoom(150), height=zoom(25))
        self.ui_lang_box.place(x=zoom(150), y=zoom(0), width=zoom(190), height=zoom(25))

        self.cs_path_tip.place(x=zoom(0), y=zoom(0), width=zoom(140), height=zoom(25))
        self.cs_path_box.place(x=zoom(140), y=zoom(0), width=zoom(125), height=zoom(25))
        self.cs_path_btn.place(x=zoom(265), y=zoom(0), width=zoom(75), height=zoom(25))

        self.language_frame.place(x=zoom(25), y=zoom(85), width=zoom(345), height=zoom(45))
        self.dst_frame.place(x=zoom(0), y=zoom(0), width=zoom(150), height=zoom(25))
        self.ing_frame.place(x=zoom(150), y=zoom(0), width=zoom(190), height=zoom(25))

        self.dst_tip.place(x=zoom(0), y=zoom(0), width=zoom(100), height=zoom(25))
        self.dst_box.place(x=zoom(100), y=zoom(0), width=zoom(50), height=zoom(25))

        self.ing_tip.place(x=zoom(0), y=zoom(0), width=zoom(140), height=zoom(25))
        self.ing_box.place(x=zoom(140), y=zoom(0), width=zoom(50), height=zoom(25))

        self.shortcut_frame.place(x=zoom(25), y=zoom(135), width=zoom(345), height=zoom(75))
        self.stran_frame.place(x=zoom(0), y=zoom(0), width=zoom(170), height=zoom(50))
        self.tog_frame.place(x=zoom(170), y=zoom(0), width=zoom(170), height=zoom(50))

        self.stran_tip.place(x=zoom(0), y=zoom(0), width=zoom(170), height=zoom(25))
        self.stran_box.place(x=zoom(0), y=zoom(25), width=zoom(150), height=zoom(25))

        self.tog_tip.place(x=zoom(0), y=zoom(0), width=zoom(170), height=zoom(25))
        self.tog_box.place(x=zoom(0), y=zoom(25), width=zoom(150), height=zoom(25))

        self.proxy_frame.place(x=zoom(25), y=zoom(215), width=zoom(345), height=zoom(100))
        self.pxy_frame.place(x=zoom(0), y=zoom(0), width=zoom(340), height=zoom(75))
        self.pxy_chk.place(x=zoom(0), y=zoom(0), width=zoom(100), height=zoom(25))
        self.pxy_chk_auto.place(x=zoom(0), y=zoom(25), width=zoom(150), height=zoom(25))
        self.pxy_entry_tip.place(x=zoom(0), y=zoom(50), width=zoom(150), height=zoom(25))
        self.pxy_entry.place(x=zoom(150), y=zoom(50), width=zoom(190), height=zoom(25))

        self.gpowered_frame.place(x=zoom(5), y=self.winfo_height()-zoom(40), width=zoom(150), height=zoom(35))
        self.gpowered_img.place(x=zoom(0), y=zoom(0), width=zoom(150), height=zoom(35))

        self.thanks_frame.place(x=self.winfo_width() - zoom(255),
                                y=self.winfo_height() - zoom(155), width=zoom(250), height=zoom(175))
        self.thanks_img.place(x=zoom(150), y=zoom(25), width=zoom(100), height=zoom(100))
        self.thanks_tip.place(x=zoom(0), y=zoom(125), width=zoom(250), height=zoom(25))
        self.thanks_tip2.place(x=zoom(140), y=zoom(0), width=zoom(125), height=zoom(25))

        self.misc_frame.place(x=zoom(25), y=zoom(320), width=zoom(250), height=zoom(120))
        self.id_frame.place(x=zoom(0), y=zoom(0), width=zoom(240), height=zoom(25))
        self.url_frame.place(x=zoom(0), y=zoom(25), width=zoom(240), height=zoom(75))

        self.id_tip.place(x=zoom(0), y=zoom(0), width=zoom(100), height=zoom(25))
        self.id_box.place(x=zoom(100), y=zoom(0), width=zoom(135), height=zoom(25))

        self.url_tip.place(x=zoom(0), y=zoom(0), width=zoom(200), height=zoom(25))
        self.url_tip2.place(x=zoom(0), y=zoom(20), width=zoom(240), height=zoom(30))
        self.url_box.place(x=zoom(0), y=zoom(50), width=zoom(200), height=zoom(25))

        self.star_tip.place(x=zoom(25), y=zoom(440), width=zoom(250), height=zoom(25))

        self.deiconify()
        self.focus_set()

    def change_lang(self, event=None):
        language = self.ui_lang_box.get()
        CONFIG["CONFIG"]["lang"] = LANG_DICT[language]
        with open(f"{LOCAL_PATH}\\config.ini", "w") as config_f:
            CONFIG.write(config_f)

    def close(self, event=None):
        dst = self.dst_box.get()
        in_game = self.ing_box.get()
        strans = self.stran_box.get()
        toggle = self.tog_box.get()
        proxy = self.pxy_entry.get()
        username = self.id_box.get()
        url = self.url_box.get()
        if dst.lower() in LANGUAGE_CODES:
            dst = LANGUAGE_CODES[dst.lower()]

        if in_game.lower() in LANGUAGE_CODES:
            in_game = LANGUAGE_CODES[in_game.lower()]

        if keyboard.key_to_scan_codes(strans, False) != ():
            CONFIG["SHORTCUT"]["strans"] = strans
        if keyboard.key_to_scan_codes(toggle, False) != ():
            CONFIG["SHORTCUT"]["toggle"] = toggle

        CONFIG["LANGUAGE"]["dst"] = dst
        CONFIG["LANGUAGE"]["in_game"] = in_game
        CONFIG["PROXY"]["url"] = proxy
        CONFIG["CONFIG"]["username"] = username
        CONFIG["CONFIG"]["url"] = url

        with open(f"{LOCAL_PATH}\\config.ini", "w") as config_f:
            CONFIG.write(config_f)
        self.destroy()

    def set_proxy(self, event=None):
        print('px')
        print(self.pxy_bool.get())
        p_state = self.pxy_bool.get()
        if p_state:
            self.pxy_chk.update()
            CONFIG["PROXY"]["enabled"] = "true"
        else:
            self.pxy_chk.update()
            CONFIG["PROXY"]["enabled"] = "false"

        with open(f"{LOCAL_PATH}\\config.ini", "w") as config_f:
            CONFIG.write(config_f)
        self.refresh_chk()

    def set_proxy_auto(self, event=None):
        print("at")
        print(self.pxy_bool_auto.get())
        p_state = self.pxy_bool_auto.get()
        if p_state:
            self.pxy_chk_auto.update()
            CONFIG["PROXY"]["mode"] = "auto"
        else:
            self.pxy_chk_auto.update()
            CONFIG["PROXY"]["mode"] = "manual"

        with open(f"{LOCAL_PATH}\\config.ini", "w") as config_f:
            CONFIG.write(config_f)

        self.refresh_chk()

    def refresh_chk(self, event=None):
        if self.pxy_bool_auto.get() or not self.pxy_bool.get():
            self.pxy_entry.configure(state="disabled")
        else:
            self.pxy_entry.configure(state="normal")

        if not self.pxy_bool.get():
            self.pxy_chk_auto.configure(state="disabled")
        else:
            self.pxy_chk_auto.configure(state="normal")

    def select_cs_path(self, event=None):
        path = askdirectory()
        self.path = path
        self.cs_path_box.config(state="normal")
        self.cs_path_box.delete(0, END)
        self.cs_path_box.insert(0, self.path)
        self.cs_path_box.config(state="disabled")

        CONFIG["CONFIG"]["cs_path"] = path
        with open(f"{LOCAL_PATH}\\config.ini", "w") as config_f:
            CONFIG.write(config_f)


class ScrollText(scrolled.ScrolledText):

    def __init__(self, master):
        self.Style = Style()
        self.Style.configure("info.TFrame", background="#1b1b1b", relief="flat")
        scrolled.ScrolledText.__init__(self, master=master, padding=0, border=0, relief="flat")
        self.text = self._text
        self.configure(style="info.TFrame")
        self._text.configure(wrap=WORD, background="#1b1b1b", borderwidth=0,
                             inactiveselectbackground="#1b1b1b",
                             foreground="#ffffff", highlightthickness=0,
                             selectbackground="#909090", selectforeground="#303030",
                             insertbackground="#ffffff",
                             highlightcolor="#ffffff", relief="flat", font=("Arial", 12, "bold"))
        # self.vbar = Scrollbar(self.outframe, command=self.cyview, orient=VERTICAL)
        # self.hbar = Scrollbar(self.outframe, command=self.cxview, orient=HORIZONTAL)
        # self['yscrollcommand'] = self.redirect_yscroll_event
        # self['xscrollcommand'] = self.hbar.set
        # # self.vbar.pack(side=RIGHT, fill=Y)
        # # self.hbar.pack(side=BOTTOM, fill=X)
        # self.pack(side=LEFT, fill=BOTH, expand=True)
        # self.vbar['command'] = self.cyview
        # self.hbar['command'] = self.cxview
        # text_meths = vars(Text).keys()
        # methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        # methods = methods.difference(text_meths)
        # for m in methods:
        #     if m[0] != '_' and m != 'config' and m != 'configure':
        #         setattr(self, m, getattr(self.outframe, m))
        # self._text.pack_forget()
        for i in COLORS.colors:
            self._text.tag_config(i.color_code, foreground=i.color_code)

    def cyview(self, *event):
        self._text.yview(*event)

    def cxview(self, *event):
        self._text.xview(*event)

    def redirect_mousewheel_event(self, event):
        self.event_generate('<MouseWheel>',
                            x=0, y=event.y, delta=event.delta)
        return "break"

    def redirect_yscroll_event(self, event):
        if self.winfo_viewable():
            delta = (event.delta / 120) if os.name == "nt" else event.delta
            self.text.yview_scroll(int(-1 * delta), "units")


def windowInit(master, width: int, height: int, canResize: bool, title: str, icon: str):
    master.config(width=zoom(width), height=zoom(height))
    if not canResize:
        master.resizable(width=False, height=False)
    master.title(title)
    master.iconbitmap(icon)


def set_appwindow(root):
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    _style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    _style = _style & ~WS_EX_TOOLWINDOW
    _style = _style | WS_EX_APPWINDOW
    res = ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, _style)
    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())


def middle(master, width=None, height=None):
    winX = width
    winY = height
    maxX = winapi.GetSystemMetrics(0)
    maxY = winapi.GetSystemMetrics(1)
    if winX is None:
        winX = master.winfo_width()
        winY = master.winfo_height()
    x = maxX // 2 - winX // 2
    y = maxY // 2 - winY // 2
    master.geometry(f"+{int(x)}+{int(y)}")


def zoom(data):
    return round(data*ZOOM)
