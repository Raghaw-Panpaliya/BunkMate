from tkinter import Label, Menu
from PIL import Image, ImageTk
from tkinter import messagebox
from bs4 import BeautifulSoup
from customtkinter import *
from datetime import datetime
from math import ceil
import webbrowser
import requests
import json
import os


APP_NAME = "BunkBuddy"
WEBSITE  = "https://bunkmate.netlify.app/"
CREATOR = "https://coderstation.netlify.app/"
DATA_FOLDER = f"{os.getenv('APPDATA')}\\{APP_NAME}"
DISCLAIMER = "Disclaimer: I do not promote or support bunking, This is just a calculator to ease attendance prediction. Also the calculations are approximate and might not be perfect, so use at your own risk."
VERSION = 1.0
ABOUT = '27 April, 2023: Thursday\n\nHello,\nThis is just a tool to ease attendance calculations. This is made using python and due to, well, boredom.\n\nCreated By: Raghaw Panpaliya\n"Efforts": Garv Thakral, Niharika Joshi(forced)'
SHORTCUTS = "Calculate: Ctrl + c\nReset: Ctrl + r\nQuit: Ctrl + q"
HISTORY = 1
date = datetime.now()
HISTORY_DATA = {
    f"{date.day}-{date.month}-{date.year}": {
        "Conducted": 0,
        "Attended": 0,
        "Yellow Form Hours": 0,
        "Situation": {
            "Can Bunk": 0,
            "Need to Attend": 0
        }
    }
}

# history
# blue form
# calculation redo
# library hours


class App:
    
    def __init__(self) -> None:
        if os.path.exists(DATA_FOLDER):
            if os.path.exists(DATA_FOLDER + "\\history.json", 'r'):
                with open(DATA_FOLDER + "\\history.json") as f:
                    HISTORY_DATA = json.loads(f)

            else:
                with open(DATA_FOLDER + "\\history.json", 'w'):
                    json.dumps({}, f, indent=4)

        
    
    def check_update(self, by_user=0):
        try:
            soup = BeautifulSoup(requests.get(WEBSITE).text, "lxml")
            latest_version = float(soup.find("span", attrs={'class': 'latest'}).text)
            
            if VERSION != latest_version:
                if messagebox.askyesno("New Update!", "Seems like you are using an older version of the app!\nDo you want to install the better version now?"):
                    webbrowser.open(WEBSITE)
            
            if by_user and VERSION == latest_version:
                messagebox.showinfo("Latest Version!", f"You are already using the latest version of {APP_NAME}! Version {VERSION}")
            
        except Exception:
            latest_version = VERSION #check if reference before declare error in exe
            if by_user:
                messagebox.showerror("Update Error!", "Could not get the update at this time! Please check internet connection!")
                return 0


    def calculate(self, yellow_hours=0, blue_hours=0):
        y_hours = self.form_field.get()
        b_hours = self.blue_field.get()

        if y_hours == "":
            yellow_hours = 0
            # self.form_field.insert(0, 0)

        try:
            yellow_hours = int(y_hours)

        except Exception:
            # messagebox.showerror("TypeError", "Please check yellow form hours!")
            # self.form_field.insert(0, 0)
            yellow_hours = 0

        if b_hours == "":
            blue_hours = 0
            # self.form_field.insert(0, 0)

        try:
            blue_hours = int(b_hours)

        except Exception:
            # messagebox.showerror("TypeError", "Please check yellow form hours!")
            # self.form_field.insert(0, 0)
            blue_hours = 0

        
        self.result_box.configure(state=NORMAL)
        self.result_box.delete("1.0", END)
        self.result_box.configure(state=DISABLED)

        try:
            conducted = int(self.conducted.get())
            attended = int(self.attended.get()) + yellow_hours
        except Exception:
            messagebox.showerror("Type Error", "Please check the entries made!")
            return 0
    
        if attended > conducted:
            go_on = messagebox.askyesno("Potential corrupt entry!", "Classes attended is more than classes conducted! Are you sure?")
            if not go_on:
                return 0
        
        current_percentage = (attended/conducted) * 100
        
        required = self.required_var.get()

        required = int(required[:-1])
        new_attended = (required*conducted)/100
        new_percentage = (new_attended/conducted) * 100
        bunk = 0

        if current_percentage < required:
            margin = ((required * conducted)-(100*attended))/(100-required)
        
        elif current_percentage == required:
            margin = 0
            
        else:
            margin = attended - new_attended
            bunk = 1

        margin = ceil(margin)

        truth = "Can Bunk" if bunk else "Need to Attend"
        phrase = "DOBBY IS FREEEE!" if bunk else "Sed lyf, No Bunk."

        if margin == 0:
            truth = "Balanced BOI"
            phrase = "TAKE RISKS, LOL"

        result_text = f"Conducted: {conducted}\nAttended: {attended} (Yellow Forms: {yellow_hours})\n\nCurrent Percentage: {round(current_percentage, 2)}%\nRequired Percentage: {required}%\n\n{truth}: {margin} Classes ({round(new_percentage,2)}%)\n\n" + phrase
        
        self.result_box.configure(state=NORMAL)
        self.result_box.insert("1.0", result_text)
        self.result_box.configure(state=DISABLED)

 
    def reset(self):
        self.root.update()
        self.conducted.delete(0, END)
        self.conducted.configure(placeholder_text='Total Conducted...')
        self.attended.delete(0, END)
        self.attended.configure(placeholder_text='Attended...')
        self.form_field.delete(0, END)
        self.form_field.configure(placeholder_text='Yellow form hours')

        self.result_box.configure(state=NORMAL)
        self.result_box.delete("1.0", END)
        self.result_box.configure(state=DISABLED)

        self.required.set("85%")
        self.root.focus()
        

    def run(self):
        # set_appearance_mode("system")
        set_appearance_mode("dark")
        set_default_color_theme("green")
        
        self.root = CTk()
        # self.root.geometry("530x300")
        self.root.resizable(0, 0)
        self.root.title(f"{APP_NAME}")
        self.root.configure(pady=10)
    
        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)

        options_menu = Menu(main_menu, tearoff=OFF)
        main_menu.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Disclaimer", command=lambda :messagebox.showwarning("Disclaimer", DISCLAIMER))
        options_menu.add_command(label="Shortcuts", command=lambda: messagebox.showinfo("Shortcuts", SHORTCUTS))
        options_menu.add_command(label="About", command=lambda: messagebox.showinfo(f"About {APP_NAME}", ABOUT))
        options_menu.add_separator()
        options_menu.add_command(label="Check for updates", command=lambda :self.check_update(1))
        options_menu.add_command(label="Report Errors/Glitches", command=lambda :webbrowser.open("https://forms.gle/rVJ6raEqnCx8Pphg9"))

        theme_menu = Menu(main_menu, tearoff=OFF)
        main_menu.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="System", command=lambda :set_appearance_mode('system'))
        theme_menu.add_separator()
        theme_menu.add_command(label="Dark", command=lambda :set_appearance_mode('dark'))
        theme_menu.add_command(label="Light", command=lambda :set_appearance_mode('light'))

        theme_menu = Menu(main_menu, tearoff=OFF)
        main_menu.add_cascade(label="KnowledgePro", menu=theme_menu)
        theme_menu.add_command(label="Open Locally", command=lambda: webbrowser.open("https://kp.christuniversity.in/KnowledgePro/StudentLogin.do"))
        theme_menu.add_command(label="Link KP", command=lambda: webbrowser.open("https://kp.christuniversity.in/KnowledgePro/StudentLogin.do"))
        theme_menu.add_command(label="Time table", command=lambda :set_appearance_mode('system'))
        theme_menu.add_separator()

        left = CTkFrame(self.root, fg_color=self.root._fg_color)
        left.grid(row=0, column=0, padx=10)

        right = CTkFrame(self.root, fg_color=self.root._fg_color)
        right.grid(row=0, column=1, padx=10)
        
        self.result_box = CTkTextbox(right, height=235, width=260, font=("Calibre", 18))
        self.result_box.pack(pady=5, expand=1, fill=X)

        # self.result_box.insert("1.0", DISCLAIMER)
        self.result_box.configure(state=DISABLED)

        form_area = CTkFrame(right, fg_color=self.root._fg_color)
        form_area.pack()

        self.form_field = CTkEntry(form_area, placeholder_text="Yellow form hours")
        self.form_field.grid(row=0, column=0)

        self.blue_field = CTkEntry(form_area, placeholder_text="Blue form hours")
        self.blue_field.grid(row=0, column=1, pady=10)

        # self.form_field.insert(0, 0)

        # form_add = CTkButton(form_area, text="Add Hours", fg_color="yellow", text_color='black', cursor="hand2", command=self.yellow_form)
        # form_add.grid(row=0, column=1, pady=10)

        image=Image.open('bunk_transparent.png')
        img=image.resize((252, 150))

        my_img=ImageTk.PhotoImage(img)
        Label(left, image=my_img).pack(fill=X)
        
        
        self.attended = CTkEntry(left, placeholder_text="Attended...", width=209, font=("Calibre", 16))
        self.attended.pack(pady=10, fill=X)
        
        self.conducted = CTkEntry(left, placeholder_text="Total Conducted...", width=209, font=("Calibre", 16))
        self.conducted.pack(fill=X)


        self.required_var = StringVar(value="85%")
        
        self.required = CTkOptionMenu(left, values=[f"{i}%" for i in range(60, 96, 5)], width=209, font=("Calibre", 16), variable=self.required_var)
        self.required.set("85%")
        self.required.pack(pady=10, fill=X)

        buttons = CTkFrame(left, fg_color=self.root._fg_color)
        buttons.pack(fill=X)

        calculate = CTkButton(buttons, text="Calculate", cursor="hand2", font=("Calibre", 16), command=self.calculate)
        calculate.grid(row=0, column=0)
        CTkLabel(buttons, text="   ").grid(row=0, column=1)
        reset = CTkButton(buttons, text="Reset", cursor="hand2", font=("Calibre", 16), command=self.reset)
        reset.grid(row=0, column=2)

        self.root.bind("<Control_L><q>", lambda x: self.quit())
        self.root.bind("<Control_L><r>", lambda x: self.reset())
        self.root.bind("<Control_L><c>", lambda x: self.calculate())

        self.check_update()
        self.root.mainloop()

    
    def quit(self):
        if messagebox.askyesno("Confirm exit", "Are you sure you want to exit?"):
            self.root.destroy()


if __name__ == "__main__":
    bunkmate = App()
    bunkmate.run()

    