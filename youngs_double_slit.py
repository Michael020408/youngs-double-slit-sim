import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to convert wavelength to RGB
def wavelength_to_rgb(wavelength_nm):
    if 380 <= wavelength_nm <= 440:
        R = -(wavelength_nm - 440) / (440 - 380)
        G = 0.0
        B = 1.0
    elif 440 < wavelength_nm <= 490:
        R = 0.0
        G = (wavelength_nm - 440) / (490 - 440)
        B = 1.0
    elif 490 < wavelength_nm <= 510:
        R = 0.0
        G = 1.0
        B = -(wavelength_nm - 510) / (510 - 490)
    elif 510 < wavelength_nm <= 580:
        R = (wavelength_nm - 510) / (580 - 510)
        G = 1.0
        B = 0.0
    elif 580 < wavelength_nm <= 645:
        R = 1.0
        G = -(wavelength_nm - 645) / (645 - 580)
        B = 0.0
    elif 645 < wavelength_nm <= 780:
        R = 1.0
        G = 0.0
        B = 0.0
    else:
        R = G = B = 0.0
    return (max(0, min(R, 1)), max(0, min(G, 1)), max(0, min(B, 1)))

# Initial constants
initial_slit_gap = 200  # μm
initial_wavelength = 650  # nm
initial_screen_distance = 100  # cm
fixed_laser_distance = 5  # cm

# Sidebar sliders
st.sidebar.title("Simulation Settings")
slit_gap = st.sidebar.slider("Slit Separation (μm)", 50, 325, initial_slit_gap, step=5)
wavelength = st.sidebar.slider("Wavelength (nm)", 380, 780, initial_wavelength, step=1)
screen_distance = st.sidebar.slider("Screen Distance (cm)", 10, 150, initial_screen_distance, step=1)

# Unit conversions
d = slit_gap * 1e-6
λ = wavelength * 1e-9
L = screen_distance / 100
initial_λ = initial_wavelength * 1e-9
initial_d = initial_slit_gap * 1e-6
initial_L = initial_screen_distance / 100

initial_fringe_spacing_mm = (initial_λ * initial_L / initial_d) * 1000
current_fringe_spacing_mm = (λ * L / d) * 1000
percent_change = ((current_fringe_spacing_mm - initial_fringe_spacing_mm) / initial_fringe_spacing_mm) * 100

# Display theoretical calculation
st.title("Young’s Double Slit Interference Pattern")
st.markdown(f"""
**Theoretical Fringe Spacing:** {current_fringe_spacing_mm:.2f} mm  
**Change from Initial (650 nm, 200 µm, 100 cm):** {percent_change:+.2f}%
""")

# Setup plot
fig, ax = plt.subplots(figsize=(12, 6))
wave_color = wavelength_to_rgb(wavelength)
slit_x = fixed_laser_distance
screen_x = slit_x + screen_distance

# Slits and screen
slit_y_positions = [-slit_gap / 2 / 100, slit_gap / 2 / 100]
ax.scatter([slit_x]*2, slit_y_positions, color='blue', s=100, label='Slits')
ax.plot([slit_x, slit_x], [-15, 15], color='black', linewidth=3, label='Slit Plate')
ax.plot([screen_x, screen_x], [-15, 15], color='gray', linewidth=3, label='Screen')
ax.scatter(0, 0, color='red', s=100, label='Laser Source')

# Rays from source to slits
for slit_y in slit_y_positions:
    ax.plot([0, slit_x], [0, slit_y], color='orange', linestyle='--')

# Rays from slits to screen
screen_points_y = np.linspace(-15, 15, 200)
for y_target in screen_points_y:
    for slit_y in slit_y_positions:
        ax.plot([slit_x, screen_x], [slit_y, y_target], color=wave_color, alpha=0.2)

# Interference pattern on screen
screen_y = np.linspace(-15, 15, 300)
for y_cm in screen_y:
    y_m = y_cm / 100
    path_diff = d * y_m / L
    phase_diff = 2 * np.pi * path_diff / λ
    I = (np.cos(phase_diff / 2)) ** 2
    color_scaled = tuple(min(1.0, c * I) for c in wave_color)
    ax.plot([screen_x + 0.2, screen_x + 0.7], [y_cm, y_cm], color=color_scaled, linewidth=5)

# Final plot settings
ax.set_title("Simulation Diagram", fontsize=16)
ax.set_xlabel("X-axis (cm)")
ax.set_ylabel("Y-axis (cm)")
ax.set_xlim(0, screen_x + 10)
ax.set_ylim(-16, 16)
ax.legend()

# Show plot
st.pyplot(fig)
