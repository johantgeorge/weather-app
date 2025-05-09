import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import json
import time
#import random 

CACHE_DUR = 600
cache_file = "cache.json"
cache = {}

try:
  with open(cache_file, "r") as f:
    cache = json.load(f)
    print(f"Loading cache from 'cache.json")

except FileNotFoundError:
   
   cache = {}


class App(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Weather App")
    self.geometry("500x500") # WxH
    #self.configure(bg = "red")

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
    tk.Label(self, text="Welcome to My Weather App!", font=("Arial", 18)).pack(pady=70)
    self.enter_button = tk.Button(self, text="ENTER", command=lambda: controller.show_frame(TypeCity))
    self.enter_button.pack()

    # Bind Return to press the ENTER button
    #self.bind_all("<Return>", lambda event: controller.show_frame(TypeCity))

  def tkraise(self, *args, **kwargs):
     super().tkraise(*args, **kwargs)
     self.bind_all("<Return>", self.goto_typecity)

  def goto_typecity(self, event=None):
    self.unbind_all("<Return>")
    self.controller.show_frame(TypeCity)
     

      
class TypeCity(tk.Frame):
  def __init__(self,parent,controller):
    super().__init__(parent)
    self.controller = controller

    tk.Label(self, text="Type City Name", font=("Helvetica",16)).pack(pady=30)

    self.city_entry = tk.Entry(self) # creates entry point
    self.city_entry.pack()
    self.city_entry.bind("<Return>", self.save_city) # when u press return it will send 
    tk.Button(self, text="Save and Print City", command=self.save_city).pack(pady=10) #will also send if u press button

    self.error_label = tk.Label(self, text="", fg="red", font=("Helvetica", 12))
    self.error_label.pack(pady=5)

  def save_city(self, event=None):
    city = self.city_entry.get()
    if not city:
        #self.error_label.config(text="Please enter a city name.")
        return
    print(f"City entered: {city}")

    weather_info = get_weather_data(city)

    if weather_info.startswith("Error") or weather_info.startswith("Exception"):
        self.error_label.config(text=weather_info)  # Show error message
    else:
        self.error_label.config(text="")  # Clear previous errors
        self.controller.city_name = city
        self.city_entry.delete(0, tk.END)
        self.controller.show_frame(DisplayResults)

class DisplayResults(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller

    self.label = tk.Label(self, text="", font=("Arial", 18))
    self.label.pack(pady=50)

    back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(TypeCity))
    back_button.pack()

    self.bind("<Return>", lambda event: controller.show_frame(TypeCity))

  def tkraise(self, *args, **kwargs):
    # Override tkraise to update label before showing
    city = getattr(self.controller, 'city_name', 'Unknown')
    weather_info = get_weather_data(city)
    self.label.config(text=weather_info)
    super().tkraise(*args, **kwargs)

    self.bind_all("<Return>", self.go_back)

  def go_back(self, event=None):
     self.unbind_all("<Return>")
     self.controller.show_frame(TypeCity)
     self.controller.frames[TypeCity].focus_set()


def get_weather_data(city_name, api_key="30d4741c779ba94c470ca1f63045390a"):
    current_time = time.time()
    if city_name in cache:
      data, timestamp = cache[city_name]
      if (current_time - timestamp <= CACHE_DUR):
        print(f"Using Cached Data")
        return data
      print(f"Cached Data Expired...") 

    
    print(f"Fetching Data from  WeatherAPI")
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "imperial"  # or "metric" for celcius
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            result = f"{city_name.title()}: {temp}°F, {desc}"
            cache[city_name] = [result, current_time]
            with open(cache_file, "w") as f:
              print(f"Loading data into 'cache.json")
              json.dump(cache, f)
            #print(f{data})
            return result
        else:
            return f"Error: {data.get('message', 'Failed to get weather')}"
    except Exception as e:
        return f"Exception occurred: {e}"


if __name__ == "__main__":
    app = App()
    app.mainloop()

