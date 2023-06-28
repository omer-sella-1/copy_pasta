from tkinter import *
import pyperclip
from pynput import keyboard
import os


class CopyPastaUI:
    """Class representing the user interface of the CopyPasta application."""

    def __init__(self, functionality):
        """
        Initialize the CopyPastaUI.

        Args:
            functionality (CopyPastaFunctionality): The functionality object to interact with.
        """
        self.functionality = functionality
        self.window = Tk()
        self.window.title("CopyPasta")
        self.window.config(padx=50, pady=50, height=220, width=220)
        self.list_box = Listbox(self.window, height=20)
        self.remove_button = Button(self.window, text="Remove", command=self.functionality.remove)
        self.copy_button = Button(self.window, text="Copy", command=self.functionality.copy_selected_text)
        self.clear_button = Button(self.window, text="Clear", command=self.functionality.clear)
        self.save_template_button = Button(self.window, text="Save to Templates", command=self.functionality.save_template)
        self.view_templates_button = Button(self.window, text="View Templates", command=self.functionality.view_templates)

    def start(self):
        """Start the CopyPasta user interface."""
        self.window.after(1000, self.functionality.check_clipboard)
        self.list_box.grid(column=0, row=0)
        self.remove_button.grid(column=0, row=2)
        self.copy_button.grid(column=0, row=1)
        self.clear_button.grid(column=0, row=3)
        self.save_template_button.grid(column=0, row=4)
        self.view_templates_button.grid(column=0, row=5)
        self.functionality.load_data_from_file()
        self.register_hotkey()
        self.window.mainloop()

    def register_hotkey(self):
        """Register a global hotkey to bring the window to the front."""
        listener = keyboard.GlobalHotKeys({'<cmd>+b+<shift>': self.functionality.on_activate_wrapper})
        listener.start()


class CopyPastaFunctionality:
    """Class representing the functionality of the CopyPasta application."""

    def __init__(self):
        """Initialize the CopyPastaFunctionality."""
        self.ui = None
        self.previous_clipboard = pyperclip.paste()

    def check_clipboard(self):
        """Check the clipboard for changes and save the content if it has changed."""
        current_clipboard = pyperclip.paste()
        if current_clipboard != self.previous_clipboard:
            self.save()
            self.previous_clipboard = current_clipboard
        self.ui.window.after(1000, self.check_clipboard)

    def load_data_from_file(self):
        """Load data from the file and populate the list box."""
        if not os.path.exists("data.txt"):
            open("data.txt", "a").close()
        with open("data.txt", "r") as f:
            data_list = f.read().split(sep=",")
        for item in data_list:
            self.ui.list_box.insert(0, item)

    def save(self):
        """Save the clipboard content to the file and insert it into the list box."""
        copy = pyperclip.paste()
        if copy in self.ui.list_box.get(0, END):
            self.ui.list_box.delete(self.ui.list_box.get(0, END).index(copy))
        self.ui.list_box.insert(0, copy)
        with open("data.txt", "a") as f:
            f.writelines(f"{copy},\n")

    def copy_selected_text(self):
        """Copy the selected text from the list box."""
        selected_text = self.ui.list_box.get(ANCHOR)
        pyperclip.copy(selected_text)

    def remove(self):
        """Remove the highlighted entry from the list box and the file."""
        selected_index = self.ui.list_box.curselection()
        if selected_index:
            selected_text = self.ui.list_box.get(selected_index)
            self.ui.list_box.delete(selected_index)
            with open("data.txt", "r") as f:
                lines = f.readlines()
            with open("data.txt", "w") as f:
                for line in lines:
                    if line.strip(",\n") != selected_text:
                        f.write(line)

    def clear(self):
        """Clear all entries in the list box and the file."""
        with open("data.txt", "w") as f:
            pass
        self.ui.list_box.delete(0, END)

    def save_template(self):
        """Save the selected text as a template."""
        selected_text = self.ui.list_box.get(ANCHOR)
        with open("templates.txt", "a") as f:
            f.writelines(f"{selected_text},\n")

    def view_templates(self):
        """View the saved templates."""
        # Placeholder for the view templates functionality
        pass

    def on_activate_wrapper(self):
        """Wrapper function to activate the window when the hotkey is pressed."""
        self.ui.window.after(0, self.on_activate)

    def on_activate(self):
        """Activate the window and bring it to the front."""
        self.ui.window.deiconify()
        self.ui.window.lift()
        self.ui.window.focus_force()

    def start(self):
        """Start the CopyPasta functionality."""
        self.ui = CopyPastaUI(self)
        self.ui.start()


if __name__ == "__main__":
    app = CopyPastaFunctionality()
    app.start()

