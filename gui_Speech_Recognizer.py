# Author: Timothy Duong
# Date: December 2020
# Basic Speech Recognition Application. Uses Google API speech recognizer in a GUI to prompt the user to speak into their microphone. The translated
# audio file is displayed in a text window

# import libraries
from tkinter import *
import speech_recognition as sr

class Window(Frame):
    """ Class to handle window"""
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # Initialize Recognizer and microphone
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.master = master
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Speech Recognizer")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a buttons, entry, textbox instance
        # Todo: Add more API options
        self.option = ["Google"] #ibm, bing, azure

        self.drop_down = StringVar(self)
        self.drop_down.set(self.option[0])

        self.w = OptionMenu(self, self.drop_down, *self.option)
        self.w.pack()

        # start recording button
        self.start_speech = Button(self, text="start", command=self.recognize_speech_from_mic)

        self.quitButton = Button(self, text="Exit", command=self.client_exit)

        self.t = Text(self, width=40, height=15)

        # placing the button on my window
        self.quitButton.place(x=340, y=260)
        self.start_speech.place(x=340, y=20)
        # self.entry_url.place(x=5, y=20)
        self.t.place(x=5, y=40)

    def client_exit(self):
        """Exit function"""
        self.master.destroy()

    def recognize_speech_from_mic(self):
        """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                   successful
        "error":   `None` if no error occured, otherwise a string containing
                   an error message if the API could not be reached or
                   speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                   otherwise a string containing the transcribed text
        """
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:

            response["transcription"] = self.recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        if ["transcription"]:
            self.t.insert("end", 'You said : {}\n'.format(response["transcription"]))
        if not response["success"]:
            self.t.insert("end", "I didn't catch that. What did you say? API may be unavailable\n")

def main():
    root = Tk()

    # size of the window
    root.geometry("400x300")

    app = Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()