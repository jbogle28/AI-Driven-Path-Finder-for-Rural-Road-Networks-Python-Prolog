
import tkinter as tk
from tkinter import messagebox
from prolog_db import PrologDB
from road_network import RoadNetwork
from gui import RoadNetworkGUI
import ctypes

def main():
    try:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
        print("Loading Prolog database...")
        db = PrologDB('roads.pl')
        network = RoadNetwork(db)
        root = tk.Tk()
        app = RoadNetworkGUI(root, network)
        
        def on_closing():
            db.close()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Error", f"Failed to start application:\n{e}")

if __name__ == "__main__":
    main()
