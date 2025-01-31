import tkinter as tk
from PIL import Image, ImageTk
import os

# Setup main window in fullscreen mode
root = tk.Tk()
root.title("Dark Mansion Adventure")
root.attributes("-fullscreen", True)  # Enable fullscreen mode

# Get screen dimensions dynamically
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Inventory and Game Variables
inventory = []
trapped = False  
mirror_world = False  

# Load Images with Fullscreen Size
def load_image(filename):
    path = os.path.join("assets", filename)  # Ensure 'assets' folder contains images
    img = Image.open(path).resize((screen_width, screen_height))
    return ImageTk.PhotoImage(img)

# Load backgrounds
backgrounds = {
    "dark_room": load_image("dark_room.jpg"),
    "left_room": load_image("left_room.jpg"),
    "right_room": load_image("mirror_hall.jpg"),
    "secret_passage": load_image("secret_passage.jpg"),
    "mirror_world": load_image("mirror_world.jpg"),
}

# UI Elements
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)

story_text = tk.Label(root, text="", wraplength=700, bg="black", fg="white", font=("Courier", 14), justify="center")
story_text.place(relx=0.5, rely=0.1, anchor="center")  # Centered at the top

button_frame = tk.Frame(root, bg="black")
button_frame.place(relx=0.5, rely=0.8, anchor="center")  # Placed at the bottom

inventory_label = tk.Label(root, text="Inventory: None", bg="black", fg="white", font=("Courier", 12))
inventory_label.place(relx=0.5, rely=0.9, anchor="center")  # Below buttons

# Function to update the background image
def update_background(bg):
    canvas.delete("bg")  # Remove previous background
    canvas.create_image(0, 0, image=backgrounds[bg], anchor="nw", tags="bg")

# Function to update the story text
def update_story(text, bg=None):
    story_text.config(text=text)
    if bg:
        update_background(bg)

# Function to update inventory
def update_inventory():
    inventory_label.config(text="Inventory: " + (", ".join(inventory) if inventory else "None"))

# Function to create buttons dynamically
def create_buttons(options):
    for widget in button_frame.winfo_children():
        widget.destroy()

    for text, command in options.items():
        button = tk.Button(button_frame, text=text, command=command, bg="gray", fg="black", font=("Courier", 12))
        button.pack(pady=5, fill="x")

# Game Functions
def welcome():
    update_story("\n🌑 Welcome to the Dark Mansion Adventure!\nYou are trapped in a decaying mansion filled with whispers.", "dark_room")
    create_buttons({"Enter the dark room": first_choice})

def first_choice():
    update_story("\nYou see two doors: Left (a dimly lit passage) and Right (a mirror-covered hallway).\nWhich door do you choose?", "dark_room")
    create_buttons({"Left Door": left_door, "Right Door": right_door})

### **LEFT DOOR PATH** ###
def left_door():
    update_story("\nYou enter a dusty study. There's a candle on a table and a locked chest.\nWhat would you like to do?", "left_room")
    create_buttons({"Take the Candle": take_candle, "Try to Open the Chest": try_chest})

def take_candle():
    inventory.append("Candle")
    update_inventory()
    update_story("\nYou take the candle and light it. Strange symbols glow on the walls.", "left_room")
    create_buttons({"Enter the Secret Passage": secret_passage})

def try_chest():
    if "Iron Key" in inventory:
        open_mystery_chest()
    else:
        update_story("\nThe chest is locked. You need a key.", "left_room")
        create_buttons({"Back": left_door})

def open_mystery_chest():
    update_story("\n🔓 You use the Iron Key to unlock the chest. Inside, you find:\n- A cryptic note with strange markings.\n- A black gemstone that pulses with energy.", "left_room")
    inventory.append("Cryptic Note")
    inventory.append("Black Gemstone")
    update_inventory()
    create_buttons({"Read the Note": read_cryptic_note, "Ignore and Enter Passage": secret_passage})

def read_cryptic_note():
    update_story("\nYou read the note:\n'**The black stone binds the curse… Break it to be free.**'\nThe gemstone grows warm.", "left_room")
    create_buttons({"Smash the Gemstone": smash_gemstone, "Keep and Continue": secret_passage})

def smash_gemstone():
    update_story("\nAs you shatter the gemstone, the mansion shakes violently!\nA hidden door opens, revealing an exit!\n🏆 **You have broken the curse and escaped!**", "left_room")
    create_buttons({"Play Again": welcome})

def secret_passage():
    update_story("\nA hidden passage appears. A chilling wind brushes past you.", "secret_passage")
    create_buttons({"Continue": passage_deeper})

def passage_deeper():
    update_story("\nA whispering voice murmurs a name you do not recognize.\nThe passage narrows, and darkness thickens.", "secret_passage")
    create_buttons({"Move Deeper": passage_end})

def passage_end():
    update_story("\nAhead, you see two paths:\n1) A door covered in glowing symbols.\n2) A staircase stained dark red.", "secret_passage")
    create_buttons({"Enter the Symbolic Door": symbol_door, "Take the Staircase": staircase_escape})

def symbol_door():
    update_story("\nAs you push open the door, shadows engulf you.\n❌ **Game Over.**", "secret_passage")
    create_buttons({"Play Again": welcome})

def staircase_escape():
    update_story("\nYou step onto the staircase. It leads to a hidden exit!\n🏆 **You have escaped!**", "secret_passage")
    create_buttons({"Play Again": welcome})

### **RIGHT DOOR PATH** ###
def right_door():
    update_story("\nYou enter a hallway of mirrors. The reflections feel… wrong.", "right_room")
    create_buttons({"Touch a Mirror": touch_mirror, "Search the Room": search_mirror_room})

def touch_mirror():
    update_story("\nThe mirror ripples like water and pulls you inside!", "mirror_world")
    create_buttons({"Mimic the Reflection": mimic_reflection, "Smash the Mirror": smash_mirror})

def mimic_reflection():
    update_story("\nYour reflection tilts its head at an unnatural angle and whispers:\n'Welcome home.'\n❌ **You are trapped forever.**", "mirror_world")
    create_buttons({"Play Again": welcome})

def smash_mirror():
    update_story("\nThe mirror shatters! A portal back to the real world appears!", "right_room")
    create_buttons({"Continue": first_choice})

def search_mirror_room():
    inventory.append("Iron Key")
    update_inventory()
    update_story("\nYou find an **Iron Key** hidden behind a broken mirror.", "right_room")
    create_buttons({"Return to Dark Room": first_choice})

# Exit Fullscreen with ESC key
def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)

# Start the game
welcome()
root.mainloop()
