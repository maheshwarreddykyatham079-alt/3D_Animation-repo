# rectifier_anim_updated.py
# Updated animation: slower, 3 cycles, diode-as-switch style, load connected, synchronized plots.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches, animation
from matplotlib.patches import FancyArrowPatch
import os

# Parameters (user requested slower, 3 cycles)
f_line = 50.0
V_rms = 230.0
V_peak = V_rms * np.sqrt(2)
Vf = 1.0                   # diode forward drop (V)
electrical_cycles = 3      # animate up to 3 cycles
t_elec_total = electrical_cycles / f_line

# Make animation slower: lower fps and more frames
frames = 240               # total frames (increase for smoothness)
fps = 12                   # lower fps => slower playback
dt_elec = t_elec_total / (frames * 4)

# Circuit elements
R_load = 47.0              # ohms - load at DC bus (connected + to -)
C = 0.002                  # 2 mF bulk cap to show smoother DC (tunable)
R_source = 1.0             # small series source resistance to shape charging pulses

# Time arrays for simulation (higher resolution)
t_highres = np.arange(0, t_elec_total, dt_elec)
omega = 2 * np.pi * f_line
vin_highres = V_peak * np.sin(omega * t_highres)

# Simulate capacitor voltage and currents:
vcap = np.zeros_like(t_highres)
i_charge = np.zeros_like(t_highres)  # diode charging current pulses (sum of conducting diodes)
i_load = np.zeros_like(t_highres)
vc = 0.0
for i in range(len(t_highres)):
    vin = vin_highres[i]
    vrect = abs(vin)
    # If rectified voltage minus two diode drops exceeds capacitor, diodes conduct and charge cap
    if vrect - 2*Vf > vc:
        # charging current determined by (vrect - 2Vf - vc) / R_source
        ich = (vrect - 2*Vf - vc) / R_source
        if ich < 0:
            ich = 0.0
        vc += (ich / C) * dt_elec  # dv = i/C * dt
        i_charge[i] = ich
    else:
        # no conduction; cap discharges through load
        i_charge[i] = 0.0
        # load current = Vc / R_load
        iL = vc / R_load
        # capacitor voltage change due to load
        dv = - (iL / C) * dt_elec
        vc += dv
        i_load[i] = iL
    # update load current in case of charging (both charge and load can coexist)
    if i_charge[i] > 0:
        # while charging, load still draws current
        i_load[i] = vc / R_load
    vcap[i] = vc

# For plotting
t_plot = np.linspace(0, t_elec_total, 2000)
vin_plot = V_peak * np.sin(omega * t_plot)
vrect_plot = np.abs(vin_plot)
vcap_plot = np.interp(t_plot, t_highres, vcap)
i_charge_plot = np.interp(t_plot, t_highres, i_charge)
i_load_plot = np.interp(t_plot, t_highres, i_load)
t_frames = np.linspace(0, t_elec_total, frames)

# --- Figure setup ---
fig = plt.figure(figsize=(11,5))
ax_sch = fig.add_axes([0.02, 0.1, 0.42, 0.85])
ax_wf = fig.add_axes([0.48, 0.1, 0.50, 0.85])

# Schematic axes
ax_sch.set_xlim(-1.6, 1.6); ax_sch.set_ylim(-1.1, 1.1); ax_sch.axis('off')
ax_sch.text(-1.45, 0.9, 'Full-Bridge Rectifier (diode bridge with cap-input filter)', fontsize=9)

# Nodes
node_ac = (-1.2, 0.0)
node_ac_plus = (-0.9, 0.6); node_ac_minus = (-0.9, -0.6)
node_top = (0.5, 0.6); node_bottom = (0.5, -0.6)
node_pos = (1.1, 0.25); node_neg = (1.1, -0.25)
node_bus_right = (1.4, 0.25); node_bus_left = (1.4, -0.25)

# AC source
circle = patches.Circle(node_ac, 0.2, fill=False, linewidth=1.2); ax_sch.add_patch(circle)
ax_sch.text(node_ac[0], node_ac[1]-0.35, 'AC\n230V', ha='center', va='top', fontsize=8)

# Wires
ax_sch.plot([node_ac[0], node_ac_plus[0]], [node_ac[1], node_ac_plus[1]], 'k', linewidth=1)
ax_sch.plot([node_ac[0], node_ac_minus[0]], [node_ac[1], node_ac_minus[1]], 'k', linewidth=1)
ax_sch.plot([node_ac_plus[0], node_top[0]], [node_ac_plus[1], node_top[1]], 'k', linewidth=1)
ax_sch.plot([node_ac_minus[0], node_bottom[0]], [node_ac_minus[1], node_bottom[1]], 'k', linewidth=1)
ax_sch.plot([node_top[0], node_pos[0]], [node_top[1], node_pos[1]], 'k', linewidth=1)
ax_sch.plot([node_bottom[0], node_neg[0]], [node_bottom[1], node_neg[1]], 'k', linewidth=1)

# DC bus rails to right
ax_sch.plot([node_pos[0], node_bus_right[0]], [node_pos[1], node_bus_right[1]], 'k', linewidth=1)
ax_sch.plot([node_neg[0], node_bus_left[0]], [node_neg[1], node_bus_left[1]], 'k', linewidth=1)

# Capacitor symbol between rails
ax_sch.plot([node_bus_right[0], node_bus_right[0]+0.15], [node_bus_right[1], node_bus_right[1]], 'k', linewidth=1)
ax_sch.plot([node_bus_left[0], node_bus_left[0]+0.15], [node_bus_left[1], node_bus_left[1]], 'k', linewidth=1)
ax_sch.plot([node_bus_right[0]+0.15, node_bus_right[0]+0.15], [node_bus_right[1]-0.08, node_bus_right[1]+0.08], 'k', linewidth=2)
ax_sch.plot([node_bus_left[0]+0.15, node_bus_left[0]+0.15], [node_bus_left[1]-0.08, node_bus_left[1]+0.08], 'k', linewidth=2)
ax_sch.text(node_bus_right[0]+0.22, node_bus_right[1]+0.12, 'C', fontsize=8)

# Load resistor between +Vdc and -Vdc (as a rectangle-ish symbol)
res_x = node_bus_right[0]+0.15; res_y_top = node_bus_right[1]
res_y_bot = node_bus_left[1]
ax_sch.plot([res_x, res_x+0.45], [res_y_top, res_y_top], 'k', linewidth=1)
ax_sch.plot([res_x+0.45, res_x+0.45], [res_y_top, res_y_bot], 'k', linewidth=1)
ax_sch.plot([res_x+0.45, res_x+0.15], [res_y_bot, res_y_bot], 'k', linewidth=1)
ax_sch.text(res_x+0.48, (res_y_top+res_y_bot)/2, 'Load\nR', ha='left', fontsize=8)

# Labels for rails
ax_sch.text(node_bus_right[0]+0.05, node_bus_right[1]+0.14, '+Vdc', fontsize=8)
ax_sch.text(node_bus_left[0]+0.05, node_bus_left[1]-0.14, '-Vdc', fontsize=8)

# Diode switches coords and drawing (open appearance)
diode_coords = {
    'D1': {'p1': (node_ac_plus[0], node_ac_plus[1]), 'p2': (node_top[0], node_top[1])},
    'D2': {'p1': (node_top[0], node_top[1]), 'p2': (node_pos[0], node_pos[1])},
    'D3': {'p1': (node_neg[0], node_neg[1]), 'p2': (node_bottom[0], node_bottom[1])},
    'D4': {'p1': (node_bottom[0], node_bottom[1]), 'p2': (node_ac_minus[0], node_ac_minus[1])}
}
diode_lines = {}
switch_gaps = 0.06
for name, cd in diode_coords.items():
    x1,y1 = cd['p1']; x2,y2 = cd['p2']
    mx = (x1+x2)/2; my = (y1+y2)/2
    vx = (x1 - mx); vy = (y1 - my)
    norm = np.hypot(vx, vy)
    if norm == 0: norm = 1
    ux, uy = vx/norm, vy/norm
    seg1_end = (mx + ux*switch_gaps, my + uy*switch_gaps)
    seg1_start = (x1, y1)
    seg2_start = (mx - ux*switch_gaps, my - uy*switch_gaps)
    seg2_end = (x2, y2)
    line1, = ax_sch.plot([seg1_start[0], seg1_end[0]], [seg1_start[1], seg1_end[1]], 'k', linewidth=2)
    line2, = ax_sch.plot([seg2_start[0], seg2_end[0]], [seg2_start[1], seg2_end[1]], 'k', linewidth=2)
    diode_lines[name] = (line1, line2)

# Current arrow when charging
current_arrow = FancyArrowPatch((0,0),(0,0), arrowstyle='->', mutation_scale=18, linewidth=2, color='tab:orange')
current_arrow.set_visible(False)
ax_sch.add_patch(current_arrow)

# Waveform axes: Vin, rectified, Vcap; twin axis for currents
ax_wf.set_title('Synchronized waveforms (3 cycles)')
ax_wf.set_xlabel('Time (ms)')
ax_wf.set_ylabel('Voltage (V)')
ax_wf.set_xlim(0, t_elec_total*1000)
ax_wf.set_ylim(-V_peak*1.1, V_peak*1.1*0.6)

# Plot voltages
v_in_line, = ax_wf.plot(t_plot*1000, vin_plot, linewidth=1, label='Vin (sin)')
v_rect_line, = ax_wf.plot(t_plot*1000, vrect_plot, linewidth=1, label='|Vin| (rectified)')
v_cap_line, = ax_wf.plot(t_plot*1000, vcap_plot, linewidth=2, label='Vcap (DC bus)')

# Currents (right axis)
ax_i = ax_wf.twinx()
ax_i.set_ylabel('Current (A)')
ax_i.set_ylim(0, max(np.max(i_charge_plot)*1.6, 1.0))
i_charge_line, = ax_i.plot(t_plot*1000, i_charge_plot, linewidth=1, linestyle='-', label='I_charge')
i_load_line, = ax_i.plot(t_plot*1000, i_load_plot, linewidth=1, linestyle='--', label='I_load')

# Markers synchronized
marker_vin, = ax_wf.plot([0], [0], marker='o', markersize=6)
marker_vrect, = ax_wf.plot([0], [0], marker='s', markersize=6)
marker_vcap, = ax_wf.plot([0], [0], marker='D', markersize=6)
marker_icharge, = ax_i.plot([0], [0], marker='o', markersize=6, color='tab:orange')
marker_iload, = ax_i.plot([0], [0], marker='x', markersize=6, color='tab:green')

# Legends
lines_labels = [v_in_line, v_rect_line, v_cap_line, i_charge_line, i_load_line]
labels = [l.get_label() for l in lines_labels]
ax_wf.legend(lines_labels, labels, loc='upper right', fontsize=8)

# Info text
info_text = ax_wf.text(0.02, 0.92, '', transform=ax_wf.transAxes, fontsize=9, va='top')

# Update function for animation
def update(frame):
    t_frame = t_frames[frame]
    idx = int(t_frame / dt_elec)
    if idx >= len(t_highres):
        idx = len(t_highres) - 1
    vin = vin_highres[idx]
    vrect = abs(vin)
    vc_val = vcap[idx]
    ich = i_charge[idx]
    il = i_load[idx]

    # Update waveform markers
    marker_vin.set_data([t_frame*1000], [vin])
    marker_vrect.set_data([t_frame*1000], [vrect])
    marker_vcap.set_data([t_frame*1000], [vc_val])
    marker_icharge.set_data([t_frame*1000], [ich])
    marker_iload.set_data([t_frame*1000], [il])

    info_text.set_text(f"t={t_frame*1000:5.1f} ms\nVin={vin:6.1f} V\nVrect={vrect:6.1f} V\nVcap={vc_val:6.2f} V\nI_charge={ich:5.2f} A\nI_load={il:5.2f} A")

    # Determine conduction pairs
    conducting = {'D1': False, 'D2': False, 'D3': False, 'D4': False}
    if vrect - 2*Vf > vc_val:
        if vin >= 0:
            conducting['D1'] = True
            conducting['D3'] = True
            start = (node_ac_plus[0], node_ac_plus[1]*0.55); end = (node_bus_right[0]+0.07, node_bus_right[1])
            current_arrow.set_positions(start, end); current_arrow.set_visible(True)
        else:
            conducting['D2'] = True
            conducting['D4'] = True
            start = (node_ac_minus[0], node_ac_minus[1]*0.55); end = (node_bus_right[0]+0.07, node_bus_right[1])
            current_arrow.set_positions(start, end); current_arrow.set_visible(True)
    else:
        current_arrow.set_visible(False)

    # Visual: closed (orange thick) when conducting, open (thin black) when not
    for name, (line1, line2) in diode_lines.items():
        if conducting[name]:
            line1.set_color('tab:orange'); line1.set_linewidth(3)
            line2.set_color('tab:orange'); line2.set_linewidth(3)
        else:
            line1.set_color('k'); line1.set_linewidth(2)
            line2.set_color('k'); line2.set_linewidth(2)

    return marker_vin, marker_vrect, marker_vcap, marker_icharge, marker_iload, info_text, current_arrow

anim = animation.FuncAnimation(fig, update, frames=frames, interval=1000/fps, blit=False)

out_gif = "full_bridge_rectifier_updated.gif"
out_mp4 = "full_bridge_rectifier_updated.mp4"
anim.save(out_gif, writer='pillow', fps=fps)
try:
    anim.save(out_mp4, writer='ffmpeg', fps=fps, extra_args=['-vcodec', 'libx264'])
except Exception:
    print("ffmpeg not available; mp4 not created. GIF was created.")

print("Saved:", out_gif)
if os.path.exists(out_mp4):
    print("Also saved:", out_mp4)
