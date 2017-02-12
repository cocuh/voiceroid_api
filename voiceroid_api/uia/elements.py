import ctypes
import win32gui
import win32con

class TextBox:
    def __init__(self, handle):
        assert handle is not None
        self.handle = handle

    def set_text(self, text):
        message = ctypes.create_unicode_buffer(text)
        message_ref = ctypes.addressof(ctypes.byref(message)._obj)
        win32gui.SendMessage(self.handle, win32con.WM_SETTEXT, 0, message_ref)


class Button:
    def __init__(self, handle):
        assert handle is not None
        self.handle = handle

    def click(self):
        win32gui.PostMessage(self.handle, win32con.BM_CLICK, 0, None)


class SaveDialog:
    def __init__(self, handle, filename_textbox, save_button):
        assert handle is not None
        self.handle = handle
        self.filename_textbox = filename_textbox
        self.save_button = save_button

    def save(self, path):
        self.filename_textbox.set_text(path)
        self.save_button.click()


class WarningDialog:
    def __init__(self, handle, ok_button, cancel_button):
        assert handle is not None
        self.handle = handle
        self.ok_button = ok_button
        self.cancel_button = cancel_button

    def ok(self):
        self.ok_button.click()

    def cancel(self):
        self.cancel_button.click()

