import time

from .adapters import (
    VoiceroidAdapterDict,
    VoiceroidAdapter,
)


class VoiceroidController:
    def __init__(self, voiceroid):
        if isinstance(voiceroid, str):
            voiceroid = VoiceroidAdapterDict.get(voiceroid)()
        if not isinstance(voiceroid, VoiceroidAdapter):
            raise TypeError('voiceroid must inherit VoiceroidAdapter')
        self.voiceroid = voiceroid

    def play(self, text):
        self.voiceroid.textbox.set_text(text)
        self.voiceroid.stop_button.click()
        self.voiceroid.play_button.click()
        warning_dialog = self.voiceroid.get_phrase_warning_dialog(self.voiceroid.main_window)
        if warning_dialog is not None:
            warning_dialog.ok()

    def save(self, text, path):
        self.voiceroid.textbox.set_text(text)
        self.voiceroid.save_button.click()
        time.sleep(1)
        save_dialog = self.voiceroid.get_save_dialog(self.voiceroid.main_window)
        save_dialog.save(path)
        return save_dialog

    def take_phrase_screenshot(self):
        image = self.voiceroid.take_phrase_screenshot(self.voiceroid.main_window)
        return image
