# AI-Driven-Path-Finder-for-Rural-Road-Networks-Python-Prolog
An AI-driven road network pathfinder built with Python (Tkinter) and SWI-Prolog via pyswip. Features Dijkstra's algorithm for multi-criteria optimization (shortest path, avoiding hazards/road closures) and BFS for fewest stops. Includes a dynamic dynamic-knowledge-base Admin panel to update nodes and routes in real-time.


# 🇯🇲 Jamaican Road Network Pathfinder

An AI-driven pathfinding application that calculates optimal travel routes across Jamaican towns using classical search algorithms. Built with a **Python (Tkinter)** graphical user interface and backed by a **SWI-Prolog** logical database engine.

---

## 🚀 Project Overview

This project simulates a real-world logistics and routing problem by modeling a road network in Jamaica (featuring central hubs like Mandeville, May Pen, Porus, and Christiana). The core routing intelligence is written entirely in declarative Prolog, which handles complex network queries based on varied constraint weights, including distance, road conditions, and closures.

### 🧠 Core AI Features
* **Multi-Criteria Optimization:** Uses a custom Dijkstra's algorithm implementation to find routes based on user preferences:
  * Shortest overall distance.
  * Avoid unpaved roads.
  * Avoid severe terrain hazards (e.g., Deep Potholes, Broken Cisterns).
  * Safely reroute around closed pathways.
* **Topology Traversal:** Features a Breadth-First Search (BFS) routing option to establish paths with the absolute **fewest stops**, bypassing path distance calculations.
* **Dynamic Knowledge Base:** Includes an integrated Admin panel capable of writing new locations, structural road links, and modified hazards back to the active `.pl` Prolog database file in real-time.

---

## 🛠️ Architecture & Tech Stack

* **Frontend:** Python 3 + Tkinter (Native GUI with `ttk` stylized elements)
* **AI Logic Engine:** SWI-Prolog (Declarative knowledge base & search predicates)
* **Bridge Layer:** `pyswip` (Foreign Function Interface wrapper linking Python to the Prolog engine)

---

## 📦 Installation & Setup

### 1. System Prerequisites
Because the application leverages native Prolog reasoning, you must install the **SWI-Prolog** binary on your operating system:
* **Windows:** Download from [SWI-Prolog Official Downloads](https://www.swi-prolog.org/). *Ensure you check "Add SWI-Prolog to system PATH" during installation.*
* **macOS:** `brew install swi-prolog`
* **Linux (Ubuntu/Debian):** `sudo apt install swi-prolog`

### 2. Clone and Install Dependencies
```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/jamaican-road-network-pathfinder.git](https://github.com/YOUR_USERNAME/jamaican-road-network-pathfinder.git)
cd jamaican-road-network-pathfinder

# Install Python requirements
pip install pyswip
