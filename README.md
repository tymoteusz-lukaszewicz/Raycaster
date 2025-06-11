# Raycasting-Grid-Editor

# Grid-Based Map Editor with Real-Time 2D Raycasting Visualization

## Purpose

This project is a two-part interactive system that includes:
1. A **grid-based map editor** for manually creating and modifying 2D line-based maps.
2. A **real-time raycasting visualizer** that simulates light rays or line-of-sight calculations based on the created map.

The primary use case is educational visualization of raycasting principles, 2D simulations, and custom map-based scenarios such as visibility, shadows, or AI perception.


## Key Features

### 🧱 Map Editor (`map_editor.py`)
* **Grid-Snapped Drawing:** Mouse clicks snap to a fixed-size grid for precise placement.
* **Line Pairing Logic:** Lines are drawn between pairs of clicked points.
* **Duplicate Line Deletion:** Clicking on an existing line removes it.
* **Edit or Create Mode:** Load existing `.txt` maps or create new ones.
* **Simple Map Format:** Saved as plain text with coordinate pairs.

### 💡 Raycasting Visualizer (`raycaster.py`)
* **Real-Time Raycasting:** Simulates rays emitted from the mouse position.
* **Ray-Wall Intersections:** Uses precise geometric checks for intersection detection.
* **Efficient with Numba:** Core raycasting logic is accelerated using Numba.
* **Dynamic Visualization:** Intersections are rendered live with colored lines.

## Technologies Used

* **Python**
* **Libraries:**
  * `pygame` – Visualization and input handling.
  * `numpy` – Numerical operations and vector math.
  * `numba` – JIT compilation for performance boost.

## File Format

Maps are saved as `.txt` files where each line represents a line segment in the form:

```
x1 y1,x2 y2
```

Example:

```
100 200,300 200
300 200,300 400
```

## Setup Instructions

1. Make sure Python 3.x is installed.
2. Install required libraries:

    ```bash
    pip install pygame numpy numba
    ```

3. Place both `map_editor.py` and `raycaster.py` in your working directory.

## Running the Code

### Run the map editor:

```bash
python map_editor.py
```

- Choose `N` to create a new map (saved to `map1.txt`).
- Or input an existing filename (e.g. `map1.txt`) to edit a map.
- Use **left-click** to add or remove lines.
- Exit the window to save the map.

### Run the raycaster:

```bash
python raycaster.py
```

- Make sure a map file like `map1.txt` exists.
- Move the mouse to emit rays from the current cursor position.
- Walls and intersections will be rendered dynamically.

## Example Use Cases

* Educational tool for teaching raycasting or vector math.
* Prototype for visibility and lighting in 2D games.
* Line-of-sight simulation for AI or robot sensors.

---

Enjoy experimenting with your own 2D maps and raycasting scenarios!
