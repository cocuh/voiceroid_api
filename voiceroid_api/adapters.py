import win32gui

from .uia import (
    search_window,
    find_child,
)
from .uia.elements import (
    TextBox,
    Button,
    SaveDialog,
    WarningDialog,
)
from .exception import (
    VoiceroidError,
)

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None


class VoiceroidAdapter:
    def __init__(self):
        self.main_window = self.get_main_window()
        self.textbox = self.get_textbox(self.main_window)
        # type: TextBox
        self.play_button = self.get_play_button(self.main_window)
        # type: Button
        self.stop_button = self.get_stop_button(self.main_window)
        # type: Button
        self.save_button = self.get_save_button(self.main_window)
        # type: Button

    def get_main_window(self):
        raise NotImplementedError

    def get_save_dialog(self, parent):
        raise NotImplementedError

    def get_phrase_warning_dialog(self, parent):
        raise NotImplementedError

    def get_textbox(self, win):
        raise NotImplementedError

    def get_play_button(self, win):
        raise NotImplementedError

    def get_stop_button(self, win):
        raise NotImplementedError

    def get_save_button(self, win):
        raise NotImplementedError

    def take_phrase_screenshot(self, win):
        raise NotImplementedError


class KiritanAdapter(VoiceroidAdapter):
    MAIN_WINDOW_TITLE = u"VOICEROID＋ 東北きりたん EX"
    EXE_PATH = "C:\Program Files (x86)\AHS\VOICEROID+\KiritanEX\VOICEROID.exe"
    SAVE_DIALOG_TITLE = u"音声ファイルの保存"
    PHRASE_WARNING_DIALOG_TITLE = u"注意"

    def get_main_window(self):
        win = search_window(self.MAIN_WINDOW_TITLE)
        if win is None:
            win = search_window(self.MAIN_WINDOW_TITLE + '*')
        if win is None:
            raise VoiceroidError('not found voiceroid window name: {}'.format(self.MAIN_WINDOW_TITLE))
        return win

    def get_save_dialog(self, parent):
        win = search_window(self.SAVE_DIALOG_TITLE, parent)
        dialog = SaveDialog(
            win,
            filename_textbox=TextBox(find_child(win, '1001', 'Edit').CurrentNativeWindowHandle),
            save_button=Button(find_child(win, '1', 'Button').CurrentNativeWindowHandle),
        )
        return dialog

    def get_phrase_warning_dialog(self, parent):
        win = search_window(self.PHRASE_WARNING_DIALOG_TITLE, parent)
        if not win:
            return None

        dialog = WarningDialog(
            win,
            ok_button=Button(find_child(win, '6', 'Button').CurrentNativeWindowHandle),
            cancel_button=Button(find_child(win, '7', 'Button').CurrentNativeWindowHandle),
        )
        return dialog

    def get_textbox(self, win):
        txt_form = find_child(win, "txtMain")
        handle = win32gui.FindWindowEx(txt_form.CurrentNativeWindowHandle, 0, None, None)
        textbox = TextBox(handle)
        return textbox

    def get_play_button(self, win):
        handle = find_child(win, "btnPlay").CurrentNativeWindowHandle
        button = Button(handle)
        return button

    def get_stop_button(self, win):
        handle = find_child(win, "btnStop").CurrentNativeWindowHandle
        button = Button(handle)
        return button

    def get_save_button(self, win):
        handle = find_child(win, "btnSaveWave").CurrentNativeWindowHandle
        button = Button(handle)
        return button

    def take_phrase_screenshot(self, win):
        bounding_box = find_child(win, "phraseEdit").CurrentBoundingRectangle
        bbox = (
            bounding_box.left,
            bounding_box.top,
            bounding_box.right,
            bounding_box.bottom,
        )
        if ImageGrab is None:
            image = None
        else:
            image = ImageGrab.grab(bbox)
        return image


VoiceroidAdapterDict = {
    'kiritan': KiritanAdapter,
}
