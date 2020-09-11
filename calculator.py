import os
import pygubu
import tkinter as tk

PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "simple.ui")
ANSWER_UI = os.path.join(PROJECT_PATH, "answer.ui")

class SimpleApp:
    # Construct the user interface. There are two inputs for Volts and Ohms, and two buttons.
    # One button clears the inputs and the other button calculates Amps and Watts based on
    # Volts and Ohms.
    def __init__(self, root):
        builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('top_frame')
        builder.connect_callbacks(self)

        self.volts_entry = builder.get_object('volts_entry')
        self.ohms_entry = builder.get_object('ohms_entry')
        self.builder = builder
        # Hack so that we can keep references to all the builders we create. Everytime we create a new builder
        # for a new window, we'll add the builder to this list so that Python knows it's still alive.
        self.builders = []

    # Results are shown in a separate window.
    # The answer window just has a label at the top and a multiline blob of text under the label.
    # We use this window for both error messages and for the results of the calculation.
    def open_answer_frame(self, parent, text):
        answer_builder = pygubu.Builder()
        answer_builder.add_from_file(ANSWER_UI)
        answer_builder.get_object('answer_frame', parent)
        answer_builder.connect_callbacks(self)
        stringvar = answer_builder.get_variable('answer_stringvar')
        stringvar.set(text)
        # This is a hack because we need to make sure that answer_builder doesn't get garbage collected.
        # If it does, it might clear some of the UI elements when it goes. If we add it to a list of builders
        # on our main app object, it won't get garbage collected.
        self.builders.append(answer_builder)

    # Calculate Amps and Watts based on Volts and Ohms
    def calculate(self):
        print("Calculating.")
        # self.mainwindow = self.builder.get_object('output_frame')
        # self.builder.connect_callbacks(self)
        try:
            # Fetch the values from the entry boxes and use them to calculate the results.
            # If there was an error anywhere, tell the user that the inputs were invalid.
            volts = float(self.volts_entry.get())
            ohms = float(self.ohms_entry.get())
            amps = volts / ohms
            watts = volts * amps
        except:
            top2 = tk.Toplevel(self.mainwindow)
            self.open_answer_frame(top2, "There was an error processing your inputs.\n"
                                         + "Please make sure that volts and ohms are both numbers\n"
                                         + "and that ohms is greater than 0." )
            return

        # The calculation worked, so let's show the results to the user.
        result_text = (str(volts) + " volts running through " + str(ohms) + " Ohms would be:\n\n"
                             + "{:.2f} Amps\n".format(amps)
                             + "{:.2f} Watts".format(watts))
        top2 = tk.Toplevel(self.mainwindow)
        self.open_answer_frame(top2, result_text)

    # Clear the entry boxes
    def clear(self):
        self.volts_entry.delete(0, tk.END)
        self.ohms_entry.delete(0, tk.END)

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Ohm's Law Calculator")
    app = SimpleApp(root)
    app.run()

