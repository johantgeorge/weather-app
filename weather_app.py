import tkinter as tk
from tkinter import ttk
import requests
#import random 

class App(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Weather App")
    self.geometry("500x500") # WxH
    #self.configure(bg = "black")

    container = tk.Frame(self)
    container.pack(fill = "both", expand = True)

    self.frames = {}
    for f in (MenuPage, TypeCity, DisplayResults): # loop all the frame names n add to frames
      frame = f(parent=container, controller=self)
      self.frames[f] = frame
      frame.place(relwidth = 1, relheight = 1)
    
    self.show_frame(MenuPage) # first frame you want to show

  def show_frame(self, page):
    frame = self.frames[page]
    frame.tkraise()
  
class MenuPage(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller

    tk.Label(self, text="Menu Screen", font=("Arial", 18)).pack(pady=50)
    tk.Label(self, text="welcome to the weather app", font=("Arial", 18)).pack(pady=70)
    tk.Button(self, text="ENTER", command=lambda: controller.show_frame(TypeCity)).pack()
    tk.Button(self, text="second button", command=lambda: controller.show_frame(TypeCity)).pack()
      
class TypeCity(tk.Frame):
  def __init__(self,parent,controller):
    super().__init__(parent)
    self.controller = controller

    tk.Label(self, text="Type City Name", font=("Helvetica",16)).pack(pady=30)

    self.city_entry = tk.Entry(self) # creates entry point
    self.city_entry.pack()
    self.city_entry.bind("<Return>", self.save_city) # when u press return it will send 
    tk.Button(self, text="Save and Print City", command=self.save_city).pack(pady=10) #will also send if u press button

  def save_city(self, event=None):
    city = self.city_entry.get()
    print(f"City entered: {city}")
    self.controller.city_name = city
    self.controller.show_frame(DisplayResults)

class DisplayResults(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller

    self.label = tk.Label(self, text="", font=("Arial", 18))
    self.label.pack(pady=50)

    tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(MenuPage)).pack()

  def tkraise(self, *args, **kwargs):
    # Override tkraise to update label before showing
    city = getattr(self.controller, 'city_name', 'Unknown')
    weather_info = get_weather_data(city)
    self.label.config(text=weather_info)
    super().tkraise(*args, **kwargs)

def get_weather_data(city_name, api_key="30d4741c779ba94c470ca1f63045390a"):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "imperial"  # or "imperial" for Fahrenheit
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"{city_name.title()}: {temp}°F, {desc}"
        else:
            return f"Error: {data.get('message', 'Failed to get weather')}"
    except Exception as e:
        return f"Exception occurred: {e}"


if __name__ == "__main__":
    app = App()
    app.mainloop()






"""


# window = tk.Tk()
# window.title("Weather App")
# window.geometry("500x500") # WxH
# window.configure(bg="red")

# -- prints out the coords of where you clicked ---
def click_location(event):
    print(f"Clicked at x={event.x}, y={event.y}")
window.bind("<Button-1>", click_location) 
# -------------------------------------------------



def change_color():
  rand_col = "#%06x" % random.randint(0, 0xFFFFFF)
  print(f"Changing color to: {rand_col}")  # Debug output
  window['bg'] = rand_col
  window.update()

# style = ttk.Style()
# style.configure("My.TButton",
#     font=("Arial", 12, "bold"),
#     foreground="green",
#     background="black",   # May still not show on macOS
#     padding=10
# )
# btn = ttk.Button(window, text="Change Color!", style="My.TButton", command=change_color)
# btn.pack(pady=50)

col_btn = tk.Button(
  window, 
  text = "Change Color! ", 
  font = ("Arial", 10, "bold"),
  bg = "black",
  fg = "green",
  activebackground= "white",
  activeforeground= "red",
  width =10,
  height = 2,
  relief = "sunken",
  bd = 3,
  command=change_color
)
#col_btn.pack(pady = 50)
col_btn.place(x=200, y=200)
#col_btn.grid(row=5, column=0, padx=50, pady=30)


window.mainloop() #actually runs the window 
"""