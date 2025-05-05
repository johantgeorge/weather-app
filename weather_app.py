import tkinter as tk
from tkinter import ttk
import random 

class App(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Weather App")
    self.geometry("500x500") # WxH
    #self.configure(bg = "black")

    container = tk.Frame(self)
    container.pack(fill = "both", expand = True)

    self.frames = {}
    for f in (): # loop all the frame names n add to frames
      frame = f(parent= container, controller = self)
      self.frames[f] = frame
      frame.place(relwidth = 1, relheight = 1)
    
    self.show_frame("") # first frame you want to show

  def show_frame(self, page):
    frame = self.frames(page)
    frame.tkraise()
  


class MenuPage(tk.Frame):
  def __init__(self, parent, controller):
    super.__init__(parent)
    self.controller = controller

    tk.Label(self, text="Menu Screen", font=("Arial", 18)).pack(pady=50)
    tk.Button(self, text="Enter Weather App", command=lambda: controller.show_frame(MainAppPage)).pack()
      
class TypeCity(tk.Frame):
  def __init__(self,parent,controller):
    super.init(parent)
    self.controller = controller
         


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