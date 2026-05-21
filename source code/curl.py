import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation
# Attention to the users and readers: this code has been gone through several bug reduction system like claude etc. However, I have not maded optimizing of memory as the primary goal of the project.
# If the AIM is to focus on memory optimization then native c or c++ is the best way to resolve it.
# In this case the whole code should be rewritten in CPP or C. I am always open for any issues or pull request. 
class FieldVisualizer:
    def __init__(self):
        # --- Basic Setup ---
        self.fig = plt.figure(figsize=(12, 9))
        self.ax = self.fig.add_subplot(111, projection='3d')
        plt.subplots_adjust(left=0.0, right=0.85, top=1, bottom=0) # Make room for widgets

        # --- Simulation Parameters ---
        self.field_type = 'Conservative'
        self.strength = 1.0
        self.angle = 0  # Current angle of the paddlewheel
        
        # --- Create the 3D Grid ---
        grid_range = np.arange(-1.5, 2, 1)
        self.x, self.y, self.z = np.meshgrid(grid_range, grid_range, grid_range)
        
        # --- Initial Plotting ---
        self.setup_plot()
        self.setup_widgets()
        
        # --- Animation ---
        self.anim = animation.FuncAnimation(
            self.fig, self._update, frames=200, interval=50, blit=False)

    def setup_plot(self):
        """Initializes the 3D plot elements."""
        self.ax.set_title("Interactive Curl Visualization", fontsize=16)
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([-2, 2])
        
        self.update_vector_field() # Draw the initial vector field
        self.paddles = self._create_paddlewheel() # Create the paddle geometry
        for p in self.paddles:
            self.ax.add_collection3d(p) # Add paddles to the plot

    def _create_paddlewheel(self):
        """Creates the geometric objects for a 3D paddlewheel."""
        # Paddle dimensions
        paddle_len = 0.8
        paddle_width = 0.4
        
        # Vertices for one paddle aligned with the y-axis
        v = np.array([
            [0, -paddle_len/2, -paddle_width/2],
            [0,  paddle_len/2, -paddle_width/2],
            [0,  paddle_len/2,  paddle_width/2],
            [0, -paddle_len/2,  paddle_width/2],
        ])

        paddles = []
        # Initialize self.original_vertices as an empty list
        self.original_vertices = [] 
        
        # Create 4 paddles by rotating the base vertices
        for angle in np.deg2rad([0, 90, 180, 270]):
            Rz = np.array([
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle),  np.cos(angle), 0],
                [0, 0, 1]
            ])
            rotated_v = v @ Rz.T
            
            # Store the raw vertices before creating the plot object
            self.original_vertices.append(rotated_v)
            
            paddle = Poly3DCollection([rotated_v], alpha=0.8)
            paddle.set_facecolor('purple')
            paddles.append(paddle)
        
        return paddles

    def setup_widgets(self):
        """Sets up the interactive sliders and buttons."""
        ax_radio = plt.axes([0.87, 0.7, 0.12, 0.15])
        self.radio_buttons = RadioButtons(ax_radio, ('Conservative', 'Non-Conservative'))
        self.radio_buttons.on_clicked(self._update_field_type)

        ax_slider = plt.axes([0.87, 0.5, 0.1, 0.15])
        self.slider = Slider(
            ax=ax_slider,
            label='Strength',
            valmin=0.1,
            valmax=3.0,
            valinit=self.strength,
            orientation="vertical"
        )
        self.slider.on_changed(self._update_strength)

    def update_vector_field(self):
        """Calculates and redraws the vector field based on current settings."""
        if hasattr(self, 'quiver'):
            self.quiver.remove()

        if self.field_type == 'Conservative':
            u, v, w = 0, 0, -1 * self.strength
            color = 'c'
        else: # Non-Conservative
            u, v, w = -self.strength * self.y, self.strength * self.x, 0
            color = 'm'
            
        self.quiver = self.ax.quiver(self.x, self.y, self.z, u, v, w, length=0.5, normalize=True, color=color)

    def _update_field_type(self, label):
        """Callback for the radio buttons."""
        self.field_type = label
        self.angle = 0 # Reset angle on field change
        self.update_vector_field()
        self.fig.canvas.draw_idle()

    def _update_strength(self, val):
        """Callback for the slider."""
        self.strength = val
        self.update_vector_field()
        self.fig.canvas.draw_idle()

    def _update(self, frame):
        """The main animation function, called for each frame."""
        if self.field_type == 'Non-Conservative':
            rotation_speed = self.strength * 0.1 
            self.angle += rotation_speed

        Rz = np.array([
            [np.cos(self.angle), -np.sin(self.angle), 0],
            [np.sin(self.angle),  np.cos(self.angle), 0],
            [0, 0, 1]
        ])

        for i, p in enumerate(self.paddles):
            new_verts = self.original_vertices[i] @ Rz.T
            p.set_verts([new_verts])

        return self.paddles

    def show(self):
        plt.show()

# --- Run the Simulation ---
if __name__ == "__main__":
    vis = FieldVisualizer()
    print("--------------------------------------------------")
    print("Interactive Curl Simulation:")
    print("- Use your mouse to rotate the 3D view.")
    print("- Use the radio buttons to switch field types.")
    print("- Use the slider to change the field strength.")
    print("Observe how the paddlewheel only spins in the Non-Conservative field!")
    print("--------------------------------------------------")
    vis.show()
