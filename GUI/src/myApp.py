import customtkinter
from actions.download_OHLCV import download_data_func

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("700x780")
app.title("CustomTkinter simple_example.py")

def download_data():
    # Fetch the user's input from the entry widget
    ticker_list_input = ticker_input.get()
    start_date = start_date_input.get()
    end_date = end_date_input.get()
    
    # You might want to do some error checking on the inputs here
    
    # Call your function with the inputs
    download_data_func(ticker_list_input, start_date, end_date)


def button_callback():
    selected_action = optionmenu_1.get()
    print("Button clicked", selected_action)
    if selected_action == "Download OHLCV":
        download_data()
        print("Download OHLCV action performed")
    elif selected_action == "Prepare Data":
        # perform Prepare Data action
        print("Prepare Data action performed")
    elif selected_action == "Run BackTest":
        # perform Run BackTest action
        print("Run BackTest action performed")
    elif selected_action == "Summaroize Results":
        # perform Summaroize Results action
        print("Summaroize Results action performed")



def slider_callback(value):
    progressbar_1.set(value)


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT)
label_1.pack(pady=10, padx=10)

download_button = customtkinter.CTkButton(master=frame_1, text="Download Data", command=download_data)
download_button.pack(pady=10, padx=10)


progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
progressbar_1.pack(pady=10, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback, text="Perform action")
button_1.pack(pady=10, padx=10)


slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_callback, from_=0, to=1)
slider_1.pack(pady=10, padx=10)
slider_1.set(0.5)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="CTkEntry")
entry_1.pack(pady=10, padx=10)

optionmenu_1 = customtkinter.CTkOptionMenu(frame_1, values=["Download OHLCV", "Prepare Data", "Run BackTest", 'Summaroize Results'])
optionmenu_1.pack(pady=10, padx=10)
optionmenu_1.set("Actions")

# Create ticker input field
ticker_input = customtkinter.CTkEntry(master=frame_1, placeholder_text="Enter tickers (comma separated)")
ticker_input.pack(pady=10, padx=10)

# Create start date input field
start_date_input = customtkinter.CTkEntry(master=frame_1, placeholder_text="Enter start date (YYYY-MM-DD)")
start_date_input.pack(pady=10, padx=10)

# Create end date input field
end_date_input = customtkinter.CTkEntry(master=frame_1, placeholder_text="Enter end date (YYYY-MM-DD)")
end_date_input.pack(pady=10, padx=10)

# combobox_1 = customtkinter.CTkComboBox(frame_1, values=["Option 1", "Option 2", "Option 42 long long long..."])
# combobox_1.pack(pady=10, padx=10)
# combobox_1.set("CTkComboBox")

# checkbox_1 = customtkinter.CTkCheckBox(master=frame_1)
# checkbox_1.pack(pady=10, padx=10)

# radiobutton_var = customtkinter.IntVar(value=1)

# radiobutton_1 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=1)
# radiobutton_1.pack(pady=10, padx=10)

# radiobutton_2 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=2)
# radiobutton_2.pack(pady=10, padx=10)

switch_1 = customtkinter.CTkSwitch(master=frame_1)
switch_1.pack(pady=10, padx=10)

text_1 = customtkinter.CTkTextbox(master=frame_1, width=200, height=70)
text_1.pack(pady=10, padx=10)
text_1.insert("0.0", "CTkTextbox\n\n\n\n")

segmented_button_1 = customtkinter.CTkSegmentedButton(master=frame_1, values=["CTkSegmentedButton", "Value 2"])
segmented_button_1.pack(pady=10, padx=10)

tabview_1 = customtkinter.CTkTabview(master=frame_1, width=200, height=70)
tabview_1.pack(pady=10, padx=10)
tabview_1.add("CTkTabview")
tabview_1.add("Tab 2")

app.mainloop()