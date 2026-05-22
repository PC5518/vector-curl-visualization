# Interactive Curl Visualization

An interactive 3D tool for visualizing and understanding **curl** in vector fields, built with Python and Matplotlib. It uses an animated paddlewheel metaphor to intuitively demonstrate the difference between conservative and non-conservative vector fields.
<img width="1081" height="594" alt="image" src="https://github.com/user-attachments/assets/8adee9ff-15d8-4a28-8253-3a15ce7aef66" />


---

## Overview

The curl of a vector field measures how much the field "rotates" or "circulates" around a point. This tool makes that concept tangible: a 3D paddlewheel placed in the field will spin only when curl is non-zero — just like a physical paddle wheel placed in a swirling fluid.

---

## Features

- **3D interactive vector field** rendered using Matplotlib's quiver plot
- **Animated paddlewheel** that spins in response to the field's curl
- **Switch between field types** using radio buttons:
  - *Conservative* — zero curl; the paddlewheel stays still
  - *Non-Conservative* — non-zero curl; the paddlewheel spins
- **Adjustable field strength** via a live slider
- **Mouse-rotatable 3D view** for exploring the field from any angle

---

## Requirements

- Python 3.7+
- NumPy
- Matplotlib (with `mpl_toolkits` for 3D support in Ubuntu's linux distribution.)

Install dependencies with:

```bash
pip install numpy matplotlib
```

---

## Usage

Run the script directly:

```bash
python field_visualizer.py
```

### Controls

| Control | Action |
|---|---|
| **Radio Buttons** | Switch between Conservative and Non-Conservative fields |
| **Strength Slider** | Adjust the magnitude of the field |
| **Mouse Drag** | Rotate the 3D view |

---

## Field Types

### Conservative Field
- Uniform downward field: `F = (0, 0, -strength)`
- Curl is zero everywhere
- The paddlewheel **does not spin**
- Rendered in **cyan**

### Non-Conservative Field
- Rotational field: `F = (-strength·y, strength·x, 0)`
- Curl is non-zero (points in the Z direction)
- The paddlewheel **spins**, with speed proportional to field strength
- Rendered in **magenta**

---

## Code Structure

| Class / Method | Description |
|---|---|
| `FieldVisualizer` | Main class — owns the figure, state, and animation loop |
| `setup_plot()` | Initializes axes, labels, and draws initial elements |
| `_create_paddlewheel()` | Builds 4-bladed paddle geometry using `Poly3DCollection` |
| `setup_widgets()` | Creates the radio button and slider UI |
| `update_vector_field()` | Recalculates and redraws the quiver plot |
| `_update(frame)` | Animation callback — rotates the paddlewheel each frame |

---

## How It Works

1. A 3D grid of points is created using `np.meshgrid`.
2. Vector field arrows are drawn at each grid point with `ax.quiver`.
3. The paddlewheel consists of four rectangular paddles (`Poly3DCollection`) rotated 90° apart around the Z-axis.
4. Each animation frame applies a rotation matrix to the paddle vertices. In the non-conservative field, the rotation angle increments each frame; in the conservative field, the angle stays fixed.

---

## License

This project is provided for educational purposes. Feel free to modify and extend it.
