from datetime import datetime
import os
import webbrowser

import PySimpleGUI as sg

from PatternMatching import PatternMatching as PM


class Matching:
    def __init__(self):
        self.matching = PM()

    def match(self, seq, pat):
        no_error = True
        try:
            with open(seq) as sequence, open(pat) as patterns:
                out_file_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
                with open(out_file_name, "w") as res:
                    self.matching.text = sequence.readline().strip()
                    for line in patterns:
                        self.matching.pattern = line.strip()
                        print(f"for pattern {self.matching.pattern}:\n")
                        res.write(f"for pattern {self.matching.pattern}:\n")
                        print(f"match indices: {self.matching.proposed_match()}\n\n")
                        res.write(
                            f"match indices: {self.matching.proposed_match()}\n\n"
                        )

        except (IOError, OSError) as e:
            no_error = False
            print(e)

        return no_error, out_file_name


class Gui:
    def __init__(self):
        self.layout = [
            [
                sg.Text("Enter Sequence Location:", size=(20, 1)),
                sg.Input(size=(45, 1), key="sequence_location"),
                sg.FileBrowse("Browse"),
            ],
            [
                sg.Text("Enter Pattern Location:", size=(20, 1)),
                sg.Input(size=(45, 1), key="pattern_location"),
                sg.FileBrowse("Browse"),
            ],
            [
                sg.Button("Submit", size=(10, 1), bind_return_key=True, key="-SUBMIT-"),
                sg.Button("Clear", size=(10, 1), key="_CLEAR_"),
                sg.Button(
                    "Open Output File", size=(20, 1), visible=False, key="-OPENOUT-"
                ),
            ],
            [sg.Output(size=(400, 380), key="-OUTPUT-")],
        ]
        self.window = sg.Window("Pattern Matcher", self.layout, size=(600, 400))


def main():
    m = Matching()
    g = Gui()
    while True:
        event, values = g.window.Read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "-SUBMIT-":
            ret = m.match(values["sequence_location"], values["pattern_location"])
            if ret[0]:
                g.window["-OPENOUT-"].update(visible=True)
                print(
                    f">> Results saved to '{os.path.join(os.getcwd(), ret[1])}'"
                )
                print(">> Click on 'Open Output File' Button to open it.")

        if event == "_CLEAR_":
            g.window["-OPENOUT-"].update(visible=False)
            g.window["-OUTPUT-"].Update("")
            g.window["sequence_location"].Update("")
            g.window["pattern_location"].Update("")

        if event == "-OPENOUT-":
            webbrowser.open(ret[1])


main()
