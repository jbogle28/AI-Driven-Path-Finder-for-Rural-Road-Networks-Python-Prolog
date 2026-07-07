import tkinter as tk
from tkinter import ttk, messagebox


class RoadNetworkGUI:
    def __init__(self, root, network):
        self.root = root
        self.network = network
        
        self.root.title("Jamaican Road Network")
        self.root.geometry("750x600")
        self.root.configure(bg="#f8f9fa")
        
        # Simple modern style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#f8f9fa", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        style.configure("TCombobox", padding=5)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        main = tk.Frame(self.root, bg="#f8f9fa")
        main.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Title
        title = tk.Label(main, text="Road Network Pathfinder",
                        font=("Segoe UI", 18, "bold"),
                        bg="#f8f9fa", fg="#2c3e50")
        title.pack(pady=(0, 15))
        
        # Mode toggle
        mode_frame = tk.Frame(main, bg="#f8f9fa")
        mode_frame.pack(pady=(0, 15))
        
        self.mode = tk.StringVar(value="user")
        
        user_btn = tk.Radiobutton(mode_frame, text="User", variable=self.mode,
                                 value="user", command=self.switch_mode,
                                 bg="#f8f9fa", font=("Segoe UI", 10),
                                 indicatoron=False, width=12, padx=10, pady=5,
                                 selectcolor="#2c3e50", fg="black",
                                 activebackground="#34495e", relief="flat", bd=1)
        user_btn.pack(side="left", padx=5)
        
        admin_btn = tk.Radiobutton(mode_frame, text="Admin", variable=self.mode,
                                  value="admin", command=self.switch_mode,
                                  bg="#f8f9fa", font=("Segoe UI", 10),
                                  indicatoron=False, width=12, padx=10, pady=5,
                                  selectcolor="#2c3e50", fg="black",
                                  activebackground="#34495e", relief="flat", bd=1)
        admin_btn.pack(side="left", padx=5)
        
        # Content container
        self.content_frame = tk.Frame(main, bg="#f8f9fa")
        self.content_frame.pack(fill="both", expand=True)
        
        self.create_user_view()
    
    def switch_mode(self):
        """Switch between user and admin views"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if self.mode.get() == "user":
            self.create_user_view()
        else:
            self.create_admin_view()
    
    def create_user_view(self):
        """Create user pathfinding interface"""
        
        # Input form
        form = tk.Frame(self.content_frame, bg="white", relief="solid", bd=1)
        form.pack(fill="x", pady=(0, 15))
        
        # From
        tk.Label(form, text="From:", bg="white", font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky="w", padx=20, pady=12)
        
        self.from_var = tk.StringVar()
        locations = self.network.get_locations()
        
        self.from_combo = ttk.Combobox(form, textvariable=self.from_var,
                                       values=locations, width=35, state="readonly")
        self.from_combo.grid(row=0, column=1, padx=20, pady=12, sticky="ew")
        if locations:
            self.from_combo.current(0)
        
        # To
        tk.Label(form, text="To:", bg="white", font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky="w", padx=20, pady=12)
        
        self.to_var = tk.StringVar()
        self.to_combo = ttk.Combobox(form, textvariable=self.to_var,
                                     values=locations, width=35, state="readonly")
        self.to_combo.grid(row=1, column=1, padx=20, pady=12, sticky="ew")
        if len(locations) > 1:
            self.to_combo.current(1)
        
        # Criteria
        tk.Label(form, text="Criteria:", bg="white", font=("Segoe UI", 10)).grid(
            row=2, column=0, sticky="w", padx=20, pady=12)
        
        self.criteria_var = tk.StringVar(value="Shortest Distance")
        criteria = ttk.Combobox(form, textvariable=self.criteria_var,
                               values=["Shortest Distance", "Fewest Stops (BFS)",
                                      "Avoid Unpaved", "Avoid Closed", 
                                      "Avoid Broken Cistern", "Avoid Deep Pothole"],
                               width=35, state="readonly")
        criteria.grid(row=2, column=1, padx=20, pady=12, sticky="ew")
        
        form.columnconfigure(1, weight=1)
        
        # Find button
        find_btn = tk.Button(self.content_frame, text="Find Path", command=self.find_path,
                           bg="#2c3e50", fg="white",
                           font=("Segoe UI", 11, "bold"),
                           relief="flat", padx=30, pady=10,
                           cursor="hand2", bd=0,
                           activebackground="#34495e")
        find_btn.pack(pady=15)
        
        # Results
        result_frame = tk.Frame(self.content_frame, bg="white", relief="solid", bd=1)
        result_frame.pack(fill="both", expand=True)
        
        tk.Label(result_frame, text="Results", bg="white",
                font=("Segoe UI", 11, "bold"), fg="#2c3e50").pack(
                    anchor="w", padx=15, pady=10)
        
        # Text area
        text_container = tk.Frame(result_frame, bg="white")
        text_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        scrollbar = tk.Scrollbar(text_container)
        scrollbar.pack(side="right", fill="y")
        
        self.result_text = tk.Text(text_container, wrap="word",
                                   font=("Consolas", 9), height=15,
                                   yscrollcommand=scrollbar.set,
                                   relief="flat", bg="#f8f9fa",
                                   padx=10, pady=10)
        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.result_text.yview)
        
        self.result_text.insert("1.0", "Select locations and click Find Path...")
        self.result_text.config(state="disabled")
    
    def create_admin_view(self):
        """Create admin interface for road management"""
        # Add Road section
        add_frame = tk.Frame(self.content_frame, bg="white", relief="solid", bd=1)
        add_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(add_frame, text="Add New Road", bg="white",
                font=("Segoe UI", 11, "bold"), fg="#2c3e50").grid(
                    row=0, column=0, columnspan=2, pady=10, padx=20, sticky="w")
        
        tk.Label(add_frame, text="Source:", bg="white", font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky="w", padx=20, pady=8)
        self.admin_source = ttk.Entry(add_frame, width=35)
        self.admin_source.grid(row=1, column=1, padx=20, pady=8, sticky="ew")
        
        tk.Label(add_frame, text="Destination:", bg="white", font=("Segoe UI", 10)).grid(
            row=2, column=0, sticky="w", padx=20, pady=8)
        self.admin_dest = ttk.Entry(add_frame, width=35)
        self.admin_dest.grid(row=2, column=1, padx=20, pady=8, sticky="ew")
        
        tk.Label(add_frame, text="Distance (km):", bg="white", font=("Segoe UI", 10)).grid(
            row=3, column=0, sticky="w", padx=20, pady=8)
        self.admin_distance = ttk.Entry(add_frame, width=35)
        self.admin_distance.grid(row=3, column=1, padx=20, pady=8, sticky="ew")
        
        tk.Label(add_frame, text="Road Type:", bg="white", font=("Segoe UI", 10)).grid(
            row=4, column=0, sticky="w", padx=20, pady=8)
        self.admin_type = ttk.Combobox(add_frame, width=33, state="readonly",
                                       values=["paved", "unpaved", "broken_cistern", "deep_pothole"])
        self.admin_type.grid(row=4, column=1, padx=20, pady=8, sticky="ew")
        self.admin_type.current(0)
        
        tk.Label(add_frame, text="Status:", bg="white", font=("Segoe UI", 10)).grid(
            row=5, column=0, sticky="w", padx=20, pady=8)
        self.admin_status = ttk.Combobox(add_frame, width=33, state="readonly",
                                         values=["open", "closed"])
        self.admin_status.grid(row=5, column=1, padx=20, pady=8, sticky="ew")
        self.admin_status.current(0)
        
        add_frame.columnconfigure(1, weight=1)
        
        add_btn = tk.Button(add_frame, text="Add Road", command=self.add_road,
                           bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"),
                           relief="flat", padx=25, pady=8, cursor="hand2", bd=0,
                           activebackground="#229954")
        add_btn.grid(row=6, column=0, columnspan=2, pady=15)
        
        # Edit Road section
        edit_frame = tk.Frame(self.content_frame, bg="white", relief="solid", bd=1)
        edit_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(edit_frame, text="Edit Existing Road", bg="white",
                font=("Segoe UI", 11, "bold"), fg="#2c3e50").grid(
                    row=0, column=0, columnspan=2, pady=10, padx=20, sticky="w")
        
        locations = self.network.get_locations()
        
        tk.Label(edit_frame, text="From:", bg="white", font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky="w", padx=20, pady=8)
        self.edit_source = ttk.Combobox(edit_frame, width=33, state="readonly", values=locations)
        self.edit_source.grid(row=1, column=1, padx=20, pady=8, sticky="ew")
        self.edit_source.bind("<<ComboboxSelected>>", self.load_road_details)
        if locations:
            self.edit_source.current(0)
        
        tk.Label(edit_frame, text="To:", bg="white", font=("Segoe UI", 10)).grid(
            row=2, column=0, sticky="w", padx=20, pady=8)
        self.edit_dest = ttk.Combobox(edit_frame, width=33, state="readonly", values=locations)
        self.edit_dest.grid(row=2, column=1, padx=20, pady=8, sticky="ew")
        self.edit_dest.bind("<<ComboboxSelected>>", self.load_road_details)
        if len(locations) > 1:
            self.edit_dest.current(1)
        
        tk.Label(edit_frame, text="Distance (km):", bg="white", font=("Segoe UI", 10)).grid(
            row=3, column=0, sticky="w", padx=20, pady=8)
        self.edit_distance = ttk.Entry(edit_frame, width=35)
        self.edit_distance.grid(row=3, column=1, padx=20, pady=8, sticky="ew")
        
        tk.Label(edit_frame, text="Road Type:", bg="white", font=("Segoe UI", 10)).grid(
            row=4, column=0, sticky="w", padx=20, pady=8)
        self.edit_type = ttk.Combobox(edit_frame, width=33, state="readonly",
                                      values=["paved", "unpaved", "broken_cistern", "deep_pothole"])
        self.edit_type.grid(row=4, column=1, padx=20, pady=8, sticky="ew")
        
        tk.Label(edit_frame, text="Status:", bg="white", font=("Segoe UI", 10)).grid(
            row=5, column=0, sticky="w", padx=20, pady=8)
        self.edit_status = ttk.Combobox(edit_frame, width=33, state="readonly",
                                        values=["open", "closed"])
        self.edit_status.grid(row=5, column=1, padx=20, pady=8, sticky="ew")
        
        edit_frame.columnconfigure(1, weight=1)
        
        # Buttons frame
        btn_frame = tk.Frame(edit_frame, bg="white")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)
        
        load_btn = tk.Button(btn_frame, text="Load Road", command=self.load_road_details,
                            bg="#95a5a6", fg="white", font=("Segoe UI", 10, "bold"),
                            relief="flat", padx=20, pady=8, cursor="hand2", bd=0,
                            activebackground="#7f8c8d")
        load_btn.pack(side="left", padx=5)
        
        update_btn = tk.Button(btn_frame, text="Update Road", command=self.update_road,
                              bg="#3498db", fg="white", font=("Segoe UI", 10, "bold"),
                              relief="flat", padx=20, pady=8, cursor="hand2", bd=0,
                              activebackground="#2980b9")
        update_btn.pack(side="left", padx=5)
    
    def add_road(self):
        """Add new road to database"""
        try:
            source = self.admin_source.get().strip()
            dest = self.admin_dest.get().strip()
            distance = float(self.admin_distance.get())
            road_type = self.admin_type.get()
            status = self.admin_status.get()
            
            if not source or not dest:
                messagebox.showerror("Error", "Source and destination required")
                return
            
            if self.network.db.add_road(source, dest, distance, road_type, status):
                messagebox.showinfo("Success", f"Road added: {source} → {dest}")
                self.admin_source.delete(0, "end")
                self.admin_dest.delete(0, "end")
                self.admin_distance.delete(0, "end")
            else:
                messagebox.showerror("Error", "Failed to add road")
        except ValueError:
            messagebox.showerror("Error", "Distance must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def load_road_details(self, event=None):
        """Load existing road details for editing"""
        source = self.edit_source.get()
        dest = self.edit_dest.get()
        
        if source == dest:
            return
        
        road = self.network.get_road_details(source, dest)
        if road:
            self.edit_distance.delete(0, "end")
            self.edit_distance.insert(0, str(road['distance']))
            
            try:
                self.edit_type.set(road['road_type'])
            except:
                self.edit_type.current(0)
            
            try:
                self.edit_status.set(road['status'])
            except:
                self.edit_status.current(0)
        else:
            self.edit_distance.delete(0, "end")
            self.edit_type.current(0)
            self.edit_status.current(0)
    
    def update_road(self):
        """Update existing road with all new details"""
        try:
            source = self.edit_source.get()
            dest = self.edit_dest.get()
            distance = float(self.edit_distance.get())
            road_type = self.edit_type.get()
            status = self.edit_status.get()
            
            if source == dest:
                messagebox.showerror("Error", "Source and destination must be different")
                return
            
            if self.network.db.update_road(source, dest, distance, road_type, status):
                messagebox.showinfo("Success", f"Road updated: {source} → {dest}")
            else:
                messagebox.showerror("Error", "Road not found")
        except ValueError:
            messagebox.showerror("Error", "Distance must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def find_path(self):
        from_loc = self.from_var.get()
        to_loc = self.to_var.get()
        criteria_text = self.criteria_var.get()
        
        if not from_loc or not to_loc:
            messagebox.showerror("Error", "Please select both locations")
            return
        
        if from_loc == to_loc:
            messagebox.showerror("Error", "Locations must be different")
            return
        
        # Check if BFS is selected
        if criteria_text == "Fewest Stops (BFS)":
            path, stats = self.network.find_path_bfs(from_loc, to_loc)
        else:
            criteria_map = {
                "Shortest Distance": "distance",
                "Avoid Unpaved": "avoid_unpaved",
                "Avoid Closed": "avoid_closed",
                "Avoid Broken Cistern": "avoid_broken_cistern",
                "Avoid Deep Pothole": "avoid_deep_pothole"
            }
            
            criteria = criteria_map.get(criteria_text, "distance")
            path, stats = self.network.find_path(from_loc, to_loc, criteria)
        
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        
        if path and stats:
            distance = stats
            
            self.result_text.insert("end", "PATH FOUND\n", "header")
            self.result_text.insert("end", "=" * 65 + "\n\n")
            self.result_text.insert("end", f"Route: {' → '.join(path)}\n\n")
            self.result_text.insert("end", f"Total Distance: {distance} km\n")
            self.result_text.insert("end", f"Stops: {len(path)}\n\n")
            self.result_text.insert("end", "Road Details:\n", "subheader")
            self.result_text.insert("end", "-" * 65 + "\n")
            
            for i in range(len(path) - 1):
                road = self.network.get_road_details(path[i], path[i+1])
                if road:
                    self.result_text.insert("end", f"\n{i+1}. {path[i]} → {path[i+1]}\n")
                    self.result_text.insert("end", f"   {road['distance']} km, ")
                    self.result_text.insert("end", f"{road['road_type']}, ")
                    status_tag = "open" if road['status'] == "open" else "closed"
                    self.result_text.insert("end", f"{road['status']}\n", status_tag)
            
            self.result_text.tag_config("header", foreground="#27ae60", font=("Consolas", 10, "bold"))
            self.result_text.tag_config("subheader", font=("Consolas", 9, "bold"))
            self.result_text.tag_config("open", foreground="#27ae60")
            self.result_text.tag_config("closed", foreground="#e74c3c")
        else:
            self.result_text.insert("end", "NO PATH FOUND\n", "error")
            self.result_text.insert("end", "=" * 65 + "\n\n")
            self.result_text.insert("end", f"No route from {from_loc} to {to_loc}\n")
            self.result_text.insert("end", "with the selected criteria.\n")
            
            self.result_text.tag_config("error", foreground="#e74c3c", font=("Consolas", 10, "bold"))
        
        self.result_text.config(state="disabled")



if __name__ == "__main__":
    import os
    import sys
    from prolog_db import PrologDB
    from road_network import RoadNetwork
    
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    try:
        print("Loading Prolog database via gui.py...")
        db = PrologDB('roads.pl')
        network = RoadNetwork(db)
        
        root = tk.Tk()
        
        # Now Python knows exactly what RoadNetworkGUI is!
        app = RoadNetworkGUI(root, network)
        
        def on_closing():
            db.close()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")