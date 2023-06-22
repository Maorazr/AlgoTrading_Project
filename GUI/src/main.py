import tkinter as tk
from tkinter import ttk

def main():
    # Create a new window
    root = tk.Tk()
    root.geometry("500x500")
    root.colormapwindows()
    # Set the window title
    root.title("My GUI App")
    label = tk.Label(root, text="Select a script:")
    label.pack()
    scripts = ["Script 1", "Script 2", "Script 3"]
    selected_script = tk.StringVar()
    dropdown = ttk.Combobox(root, textvariable=selected_script)
    dropdown['values'] = scripts
    dropdown.pack()

    # Create a text field
    input_text = tk.StringVar()
    text_field = tk.Entry(root, textvariable=input_text, width=50, font=("Arial", 24), justify=tk.CENTER)
    text_field.pack()

    # Create a button
    button = tk.Button(root, text="Run Script", command=lambda: run_script(selected_script.get(), input_text.get()))
    button.pack()

    # Run the event loop
    root.mainloop()

def run_script(script, input):
    print(f"Running {script} with input {input}...")

if __name__ == "__main__":
    main()
