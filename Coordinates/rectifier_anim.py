# rectifier_anim.py
# Animation of a full-bridge diode rectifier with capacitor smoothing.
# Produces full_bridge_rectifier.gif (and mp4 if ffmpeg is available).

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches, animation
from matplotlib.patches import FancyArrowPatch
import os

# Parameters
f_line = 50.0                 # mains frequency (Hz)
V_rms = 230.0                 # mains (for annotation)
V_peak = V_rms * np.sqrt(2)
Vf = 1.0                      # diode forward drop (V) — simple model
electrical_cycles = 5         # how many electrical cycles to simulate
t_elec_total = electrical_cycles / f_line
frames = 240                  # animation frames
fps = 30                      # frames-per-second for saving
dt_elec = t_elec_total / (frames * 4)

# Simple RC load to show capacitor smoothing behavior
R_load = 50.0      # ohms (arbitrary to make discharge visible)
C = 0.0005         # farads (0.5 mF) — adjust to see more/less smoothing

# High-resolution simulation of capacitor voltage
t_highres = np.arange(0, t_elec_total, dt_elec)
omega = 2 * np.pi * f_line
vin_highres = V_peak * np.sin(omega * t_highres)
vcap = np.zeros_like(t_highres)
vc = 0.0
for i in range(len(t_highres)):
    vin = vin_highres[i]
    vrect = abs(vin)
    # ideal diode conduction: if rectified voltage (minus diode drops) > Vc, capacitor charges
    if vrect - 2*Vf > vc:
        vc = vrect - 2*Vf
    else:
        # discharge through load (simple Euler step)
        dv = - (vc / (R_load * C)) * dt_elec
        vc = vc + dv
        if vc < 0:
            vc = 0.0
    vcap[i] = vc

# plotting-time arrays
t_plot = np.linspace(0, t_elec_total, 2000)
vin_plot = V_peak * np.sin(omega * t_plot)
vrect_plot = np.abs(vin_plot)
vcap_plot = np.interp(t_plot, t_highres, vcap)
t_frames = np.linspace(0, t_elec_total, frames)

# Setup figure (left: schematic, right: waveforms)
fig = plt.figure(figsize=(10,4))
ax_sch = fig.add_axes([0.03, 0.1, 0.45, 0.85])
ax_wf = fig.add_axes([0.53, 0.12, 0.44, 0.8])

ax_sch.set_xlim(-1.5, 1.5); ax_sch.set_ylim(-1.0, 1.0); ax_sch.axis('off')
circle = patches.Circle((-1.2, 0.0), 0.2, fill=False, linewidth=1.2); ax_sch.add_patch(circle)
ax_sch.text(-1.2, -0.35, 'AC\n230V', ha='center', va='top', fontsize=8)

# Node positions (for schematic drawing)
node_ac_plus = (-0.9, 0.6); node_ac_minus = (-0.9, -0.6)
node_top = (0.6, 0.6); node_bottom = (0.6, -0.6)
node_pos = (1.2, 0.18); node_neg = (1.2, -0.18)

# draw four diodes (simple triangular symbol + line)
diode_patches = []
def draw_diode(center):
    cx, cy = center
    tri = patches.Polygon([[cx-0.12, cy-0.08], [cx-0.12, cy+0.08], [cx+0.12, cy]], closed=True, linewidth=1)
    line = patches.FancyBboxPatch((cx+0.12, cy-0.02), 0.06, 0.04, boxstyle="square,pad=0")
    ax_sch.add_patch(tri); ax_sch.add_patch(line)
    diode_patches.append((tri, line))

draw_diode(((node_ac_plus[0]+node_top[0])/2, node_ac_plus[1]*0.55))       # top-left
draw_diode(((node_bottom[0]+node_ac_minus[0])/2, node_ac_minus[1]*0.55)) # bottom-right (visual)
draw_diode(((node_top[0]+node_pos[0])/2, node_top[1]*0.55))              # top-right
draw_diode(((node_neg[0]+node_bottom[0])/2, node_bottom[1]*0.55))        # bottom-left

# wires and DC bus / capacitor / load
ax_sch.plot([-1.2, node_ac_plus[0]], [0.0, node_ac_plus[1]], 'k', linewidth=1)
ax_sch.plot([-1.2, node_ac_minus[0]], [0.0, node_ac_minus[1]], 'k', linewidth=1)
ax_sch.plot([node_ac_plus[0], node_top[0]], [node_ac_plus[1], node_top[1]], 'k', linewidth=1)
ax_sch.plot([node_ac_minus[0], node_bottom[0]], [node_ac_minus[1], node_bottom[1]], 'k', linewidth=1)
ax_sch.plot([node_top[0], node_pos[0]], [node_top[1], node_pos[1]], 'k', linewidth=1)
ax_sch.plot([node_bottom[0], node_neg[0]], [node_bottom[1], node_neg[1]], 'k', linewidth=1)
ax_sch.plot([node_pos[0], node_pos[0]+0.15], [node_pos[1], node_pos[1]], 'k', linewidth=1)
ax_sch.plot([node_neg[0], node_neg[0]+0.15], [node_neg[1], node_neg[1]], 'k', linewidth=1)
ax_sch.plot([node_pos[0]+0.15, node_pos[0]+0.30], [node_pos[1], node_pos[1]], 'k', linewidth=1)
ax_sch.plot([node_pos[0]+0.30, node_pos[0]+0.30], [node_pos[1]-0.08, node_pos[1]+0.08], 'k', linewidth=2)
ax_sch.plot([node_pos[0]+0.35, node_pos[0]+0.35], [node_pos[1]-0.08, node_pos[1]+0.08], 'k', linewidth=2)
ax_sch.text(node_pos[0]+0.35, node_pos[1]+0.12, 'C', ha='center', fontsize=8)
ax_sch.plot([node_pos[0]+0.35, node_pos[0]+0.70], [node_pos[1], node_pos[1]], 'k', linewidth=1)
ax_sch.plot([node_pos[0]+0.70, node_pos[0]+0.70], [node_pos[1], node_neg[1]], 'k', linewidth=1)
ax_sch.plot([node_pos[0]+0.70, node_neg[0]+0.35], [node_neg[1], node_neg[1]], 'k', linewidth=1)
ax_sch.text(node_pos[0]+0.85, (node_pos[1]+node_neg[1])/2, 'Load\nR', ha='left', fontsize=8)
ax_sch.text(node_pos[0]+0.05, node_pos[1]+0.12, '+Vdc', ha='center', fontsize=8)
ax_sch.text(node_neg[0]+0.05, node_neg[1]-0.12, '-Vdc', ha='center', fontsize=8)
ax_sch.text(-1.25, 0.8, 'Full-Bridge Schematic\n(idealized)', fontsize=9, ha='left')

# arrow showing current flow when charging occurs
current_arrow = FancyArrowPatch((0,0),(0,0), arrowstyle='->', mutation_scale=15, linewidth=2, color='tab:orange')
current_arrow.set_visible(False)
ax_sch.add_patch(current_arrow)

# Waveform plot (right)
ax_wf.set_title('Waveforms (milliseconds)')
ax_wf.set_xlabel('Time (ms)')
ax_wf.set_ylabel('Voltage (V)')
ax_wf.set_xlim(0, t_elec_total*1000)
ax_wf.set_ylim(-V_peak*1.1, V_peak*1.1)
ax_wf.plot(t_plot*1000, vin_plot, linewidth=1, label='AC input (sin)')
ax_wf.plot(t_plot*1000, vrect_plot, linewidth=1, label='Rectified (|sin|)')
ax_wf.plot(t_plot*1000, vcap_plot, linewidth=2, label='Capacitor voltage (Vcap)')
marker_vin, = ax_wf.plot([0], [0], marker='o', markersize=6)
marker_vrect, = ax_wf.plot([0], [0], marker='s', markersize=6)
marker_vcap, = ax_wf.plot([0], [0], marker='D', markersize=6)
ax_wf.legend(loc='upper right', fontsize=8)
ax_wf.grid(alpha=0.25)
text_info = ax_wf.text(0.02, 0.92, '', transform=ax_wf.transAxes, fontsize=9, va='top')

# Update function for animation
def update(frame):
    t_frame = t_frames[frame]
    idx = int(t_frame / dt_elec)
    if idx >= len(t_highres):
        idx = len(t_highres) - 1
    vin = vin_highres[idx]
    vrect = abs(vin)
    vc_val = vcap[idx]

    marker_vin.set_data([t_frame*1000], [vin])
    marker_vrect.set_data([t_frame*1000], [vrect])
    marker_vcap.set_data([t_frame*1000], [vc_val])
    info = f"Time: {t_frame*1000:5.1f} ms\nVin: {vin:6.1f} V\nRectified: {vrect:6.1f} V\nVcap: {vc_val:6.1f} V\n(230 Vrms → {V_peak:.1f} Vpk)"
    text_info.set_text(info)

    # determine which diode pair conducts (visual)
    conducting = [False, False, False, False]  # mapping of the four drawn diodes
    if vin >= 0:
        if (vrect - 2*Vf) > vc_val:
            conducting[0] = True; conducting[1] = True
            start = (node_ac_plus[0], node_ac_plus[1]*0.55); end = (node_pos[0]+0.30, node_pos[1])
            current_arrow.set_positions(start, end); current_arrow.set_visible(True)
        else:
            current_arrow.set_visible(False)
    else:
        if (vrect - 2*Vf) > vc_val:
            conducting[2] = True; conducting[3] = True
            start = (node_ac_minus[0], node_ac_minus[1]*0.55); end = (node_pos[0]+0.30, node_pos[1])
            current_arrow.set_positions(start, end); current_arrow.set_visible(True)
        else:
            current_arrow.set_visible(False)

    for i, (tri, line) in enumerate(diode_patches):
        if conducting[i]:
            tri.set_facecolor((1.0, 0.55, 0.0)); tri.set_edgecolor('k'); line.set_facecolor((1.0,0.55,0.0))
        else:
            tri.set_facecolor('none'); tri.set_edgecolor('k'); line.set_facecolor('none')

    return marker_vin, marker_vrect, marker_vcap, text_info, current_arrow

anim = animation.FuncAnimation(fig, update, frames=frames, interval=1000/fps, blit=False)

out_gif = "full_bridge_rectifier.gif"
out_mp4 = "full_bridge_rectifier.mp4"
anim.save(out_gif, writer='pillow', fps=fps)
# try mp4 if ffmpeg is installed
try:
    anim.save(out_mp4, writer='ffmpeg', fps=fps, extra_args=['-vcodec', 'libx264'])
except Exception:
    print("ffmpeg not available; mp4 not created. GIF was created.")

print("Saved:", out_gif)
if os.path.exists(out_mp4):
    print("Also saved:", out_mp4)
