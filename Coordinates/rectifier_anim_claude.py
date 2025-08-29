import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle, Polygon
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

class BridgeRectifierAnimation:
    def __init__(self):
        # Create figure and subplots
        self.fig = plt.figure(figsize=(16, 10))
        self.fig.suptitle('Full Bridge Rectifier - Current Flow Animation', fontsize=16, fontweight='bold')
        
        # Circuit diagram subplot
        self.ax_circuit = plt.subplot2grid((3, 2), (0, 0), rowspan=3)
        self.ax_circuit.set_xlim(-1, 11)
        self.ax_circuit.set_ylim(-1, 8)
        self.ax_circuit.set_aspect('equal')
        self.ax_circuit.axis('off')
        self.ax_circuit.set_title('Circuit Diagram', fontsize=14, pad=20)
        
        # Input waveform subplot
        self.ax_input = plt.subplot2grid((3, 2), (0, 1))
        self.ax_input.set_title('AC Input Voltage', fontsize=12)
        self.ax_input.set_ylabel('Voltage (V)')
        self.ax_input.grid(True, alpha=0.3)
        
        # Output waveform subplot
        self.ax_output = plt.subplot2grid((3, 2), (1, 1))
        self.ax_output.set_title('DC Output Voltage', fontsize=12)
        self.ax_output.set_ylabel('Voltage (V)')
        self.ax_output.grid(True, alpha=0.3)
        
        # Info subplot
        self.ax_info = plt.subplot2grid((3, 2), (2, 1))
        self.ax_info.axis('off')
        
        # Animation parameters
        self.time = 0
        self.frequency = 50  # Hz
        self.dt = 0.01
        self.time_window = 0.1  # seconds to display
        
        # Data storage
        self.time_data = []
        self.input_data = []
        self.output_data = []
        
        # Initialize circuit elements
        self.setup_circuit()
        self.setup_graphs()
        
    def setup_circuit(self):
        """Draw the static circuit elements"""
        # AC Source (transformer)
        ac_source = Circle((1, 4), 0.5, fill=False, edgecolor='black', linewidth=2)
        self.ax_circuit.add_patch(ac_source)
        self.ax_circuit.text(1, 4, 'AC', ha='center', va='center', fontweight='bold')
        
        # Transformer windings
        self.ax_circuit.plot([0.7, 0.7], [3.2, 4.8], 'k-', linewidth=3)
        self.ax_circuit.plot([1.3, 1.3], [3.2, 4.8], 'k-', linewidth=3)
        
        # Bridge diodes (as triangles with bars)
        # D1 (top-left)
        d1_triangle = Polygon([(2.5, 5.8), (3.5, 5.8), (3, 6.8)], facecolor='red', edgecolor='black', linewidth=2)
        self.ax_circuit.add_patch(d1_triangle)
        self.ax_circuit.plot([3.5, 3.5], [5.5, 6.1], 'k-', linewidth=3)
        self.ax_circuit.text(3, 5.3, 'D1', ha='center', va='center', fontweight='bold')
        
        # D2 (top-right)
        d2_triangle = Polygon([(6.5, 6.8), (7.5, 6.8), (7, 5.8)], facecolor='red', edgecolor='black', linewidth=2)
        self.ax_circuit.add_patch(d2_triangle)
        self.ax_circuit.plot([6.5, 6.5], [6.1, 7.1], 'k-', linewidth=3)
        self.ax_circuit.text(7, 7.4, 'D2', ha='center', va='center', fontweight='bold')
        
        # D3 (bottom-left)
        d3_triangle = Polygon([(2.5, 2.2), (3.5, 2.2), (3, 1.2)], facecolor='red', edgecolor='black', linewidth=2)
        self.ax_circuit.add_patch(d3_triangle)
        self.ax_circuit.plot([3.5, 3.5], [1.9, 2.5], 'k-', linewidth=3)
        self.ax_circuit.text(3, 2.8, 'D3', ha='center', va='center', fontweight='bold')
        
        # D4 (bottom-right)
        d4_triangle = Polygon([(6.5, 1.2), (7.5, 1.2), (7, 2.2)], facecolor='red', edgecolor='black', linewidth=2)
        self.ax_circuit.add_patch(d4_triangle)
        self.ax_circuit.plot([6.5, 6.5], [1.5, 2.1], 'k-', linewidth=3)
        self.ax_circuit.text(7, 0.8, 'D4', ha='center', va='center', fontweight='bold')
        
        # Load resistor
        load_rect = FancyBboxPatch((8.5, 3.5), 1, 1, boxstyle="round,pad=0.1", 
                                   facecolor='white', edgecolor='black', linewidth=2)
        self.ax_circuit.add_patch(load_rect)
        # Zigzag pattern for resistor
        x_zag = np.linspace(8.7, 9.3, 7)
        y_zag = [3.8, 4.2, 3.8, 4.2, 3.8, 4.2, 4.2]
        self.ax_circuit.plot(x_zag, y_zag, 'k-', linewidth=2)
        self.ax_circuit.text(9, 3, 'Load\nResistor', ha='center', va='center', fontweight='bold')
        
        # Circuit connections (static wires)
        # AC input connections
        self.ax_circuit.plot([1.5, 2.5], [4.5, 5.8], 'k-', linewidth=2)
        self.ax_circuit.plot([1.5, 2.5], [3.5, 2.2], 'k-', linewidth=2)
        
        # Bridge top connections
        self.ax_circuit.plot([3.5, 5], [6.3, 6.3], 'k-', linewidth=2)
        self.ax_circuit.plot([5, 6.5], [6.3, 6.3], 'k-', linewidth=2)
        self.ax_circuit.plot([7.5, 8.5], [6.3, 4.5], 'k-', linewidth=2)
        
        # Bridge bottom connections
        self.ax_circuit.plot([3.5, 5], [1.7, 1.7], 'k-', linewidth=2)
        self.ax_circuit.plot([5, 6.5], [1.7, 1.7], 'k-', linewidth=2)
        self.ax_circuit.plot([7.5, 8.5], [1.7, 3.5], 'k-', linewidth=2)
        
        # Center connections
        self.ax_circuit.plot([3, 5], [4, 4], 'k-', linewidth=2)
        self.ax_circuit.plot([5, 7], [4, 4], 'k-', linewidth=2)
        
        # Store diode patches for color changes
        self.diode_patches = {
            'D1': d1_triangle,
            'D2': d2_triangle,
            'D3': d3_triangle,
            'D4': d4_triangle
        }
        
        # Current flow paths (initially invisible)
        self.current_paths = {}
        
        # Path 1: Positive half cycle (D1 and D4 conducting)
        x1 = [1.5, 2.5, 3, 3.5, 5, 6.5, 7, 7.5, 8.5, 9, 9, 8.5, 7.5, 7, 6.5, 5, 3.5, 3, 2.5, 1.5]
        y1 = [4.5, 5.8, 6.3, 6.3, 6.3, 6.3, 6.3, 6.3, 4.5, 4, 4, 3.5, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 3.5, 4.5]
        self.current_paths['path1'] = self.ax_circuit.plot(x1, y1, 'r-', linewidth=4, alpha=0.8, visible=False)[0]
        
        # Path 2: Negative half cycle (D2 and D3 conducting)
        x2 = [1.5, 2.5, 3, 3.5, 5, 7, 7.5, 8.5, 9, 9, 8.5, 7.5, 7, 5, 3.5, 3, 2.5, 1.5]
        y2 = [3.5, 2.2, 1.7, 1.7, 1.7, 1.7, 1.7, 3.5, 4, 4, 4.5, 6.3, 6.3, 4, 4, 4, 4, 3.5]
        self.current_paths['path2'] = self.ax_circuit.plot(x2, y2, 'r-', linewidth=4, alpha=0.8, visible=False)[0]
        
        # Voltage polarity indicators
        self.ax_circuit.text(0.3, 4.7, '+', fontsize=16, fontweight='bold', color='red')
        self.ax_circuit.text(0.3, 3.3, '-', fontsize=16, fontweight='bold', color='blue')
        self.ax_circuit.text(9.8, 4.7, '+', fontsize=16, fontweight='bold', color='red')
        self.ax_circuit.text(9.8, 3.3, '-', fontsize=16, fontweight='bold', color='blue')
        
    def setup_graphs(self):
        """Setup the graph axes"""
        # Input graph setup
        self.input_line, = self.ax_input.plot([], [], 'b-', linewidth=2, label='AC Input')
        self.ax_input.set_xlim(0, self.time_window)
        self.ax_input.set_ylim(-1.5, 1.5)
        self.ax_input.legend()
        
        # Output graph setup
        self.output_line, = self.ax_output.plot([], [], 'r-', linewidth=2, label='DC Output')
        self.ax_output.set_xlim(0, self.time_window)
        self.ax_output.set_ylim(-0.2, 1.5)
        self.ax_output.legend()
        self.ax_output.set_xlabel('Time (s)')
        
        # Info text
        self.info_text = self.ax_info.text(0.1, 0.8, '', fontsize=12, transform=self.ax_info.transAxes,
                                          verticalalignment='top', 
                                          bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
    def update_diode_states(self, input_voltage):
        """Update diode colors based on conduction state"""
        conducting_color = 'green'
        blocking_color = 'red'
        
        if input_voltage > 0.1:
            # Positive half cycle: D1 and D4 conduct
            self.diode_patches['D1'].set_facecolor(conducting_color)
            self.diode_patches['D2'].set_facecolor(blocking_color)
            self.diode_patches['D3'].set_facecolor(blocking_color)
            self.diode_patches['D4'].set_facecolor(conducting_color)
            
            # Show current path 1
            self.current_paths['path1'].set_visible(True)
            self.current_paths['path2'].set_visible(False)
            
            phase = "Positive Half Cycle"
            conducting = "D1, D4"
            
        elif input_voltage < -0.1:
            # Negative half cycle: D2 and D3 conduct
            self.diode_patches['D1'].set_facecolor(blocking_color)
            self.diode_patches['D2'].set_facecolor(conducting_color)
            self.diode_patches['D3'].set_facecolor(conducting_color)
            self.diode_patches['D4'].set_facecolor(blocking_color)
            
            # Show current path 2
            self.current_paths['path1'].set_visible(False)
            self.current_paths['path2'].set_visible(True)
            
            phase = "Negative Half Cycle"
            conducting = "D2, D3"
            
        else:
            # Zero crossing
            for diode in self.diode_patches.values():
                diode.set_facecolor(blocking_color)
            
            self.current_paths['path1'].set_visible(False)
            self.current_paths['path2'].set_visible(False)
            
            phase = "Zero Crossing"
            conducting = "None"
        
        # Update info text
        info_str = f"""Current Phase: {phase}
Conducting Diodes: {conducting}
Current Direction: {'Top to Bottom through Load' if abs(input_voltage) > 0.1 else 'No Current'}
Input Voltage: {input_voltage:.2f}V
Output Voltage: {abs(input_voltage):.2f}V"""
        
        self.info_text.set_text(info_str)
    
    def animate(self, frame):
        """Animation function called for each frame"""
        current_time = frame * self.dt
        
        # Generate AC input voltage
        input_voltage = np.sin(2 * np.pi * self.frequency * current_time)
        output_voltage = abs(input_voltage)
        
        # Store data
        self.time_data.append(current_time)
        self.input_data.append(input_voltage)
        self.output_data.append(output_voltage)
        
        # Keep only recent data for display
        if len(self.time_data) > int(self.time_window / self.dt):
            self.time_data = self.time_data[-int(self.time_window / self.dt):]
            self.input_data = self.input_data[-int(self.time_window / self.dt):]
            self.output_data = self.output_data[-int(self.time_window / self.dt):]
        
        # Update graphs
        self.input_line.set_data(self.time_data, self.input_data)
        self.output_line.set_data(self.time_data, self.output_data)
        
        # Update x-axis limits to show moving window
        if current_time > self.time_window:
            self.ax_input.set_xlim(current_time - self.time_window, current_time)
            self.ax_output.set_xlim(current_time - self.time_window, current_time)
        
        # Update diode states and current flow
        self.update_diode_states(input_voltage)
        
        return [self.input_line, self.output_line] + list(self.diode_patches.values()) + list(self.current_paths.values()) + [self.info_text]
    
    def start_animation(self):
        """Start the animation"""
        self.ani = animation.FuncAnimation(
            self.fig, self.animate, frames=None, interval=50, blit=False, repeat=True
        )
        
        # Add legend for diode states
        legend_elements = [
            mpatches.Patch(color='green', label='Conducting Diode'),
            mpatches.Patch(color='red', label='Blocking Diode'),
            Line2D([0], [0], color='red', linewidth=4, label='Current Flow')
        ]
        self.ax_circuit.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
        
        plt.tight_layout()
        plt.show()

def main():
    """Main function to run the animation"""
    print("Full Bridge Rectifier Animation")
    print("=" * 50)
    print("This animation shows:")
    print("1. AC input voltage (blue sine wave)")
    print("2. DC output voltage (red rectified wave)")
    print("3. Diode switching states (green = conducting, red = blocking)")
    print("4. Current flow paths (red lines)")
    print("\nStarting animation...")
    
    # Create and start animation
    rectifier = BridgeRectifierAnimation()
    rectifier.start_animation()

if __name__ == "__main__":
    # Required libraries check
    try:
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        import numpy as np
        main()
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("\nTo install required libraries, run:")
        print("pip install matplotlib numpy")

# Additional utility functions for educational purposes

def analyze_rectifier_performance():
    """Analyze the performance characteristics of the bridge rectifier"""
    t = np.linspace(0, 0.1, 1000)  # 100ms time span
    input_voltage = np.sin(2 * np.pi * 50 * t)  # 50Hz AC
    output_voltage = np.abs(input_voltage)
    
    # Calculate ripple factor
    dc_component = np.mean(output_voltage)
    ac_component = np.sqrt(np.mean((output_voltage - dc_component)**2))
    ripple_factor = ac_component / dc_component
    
    # Calculate efficiency (ideal case)
    rms_output = np.sqrt(np.mean(output_voltage**2))
    rms_input = np.sqrt(np.mean(input_voltage**2))
    efficiency = (rms_output / rms_input) * 100
    
    print(f"\nBridge Rectifier Performance Analysis:")
    print(f"DC Component: {dc_component:.3f}V")
    print(f"Ripple Factor: {ripple_factor:.3f}")
    print(f"Efficiency: {efficiency:.1f}%")
    print(f"Peak Inverse Voltage (per diode): {1.0:.1f}V")
    
    return {
        'dc_component': dc_component,
        'ripple_factor': ripple_factor,
        'efficiency': efficiency
    }

def compare_rectifier_types():
    """Compare different rectifier configurations"""
    print("\nRectifier Comparison:")
    print("=" * 40)
    print("Half Wave Rectifier:")
    print("  - Efficiency: ~40.6%")
    print("  - Ripple Factor: 1.21")
    print("  - PIV: Vm")
    print("  - Transformer Utilization: Poor")
    
    print("\nCenter-Tap Rectifier:")
    print("  - Efficiency: ~81.2%")
    print("  - Ripple Factor: 0.48")
    print("  - PIV: 2Vm")
    print("  - Transformer Utilization: Better")
    
    print("\nFull Bridge Rectifier:")
    print("  - Efficiency: ~81.2%")
    print("  - Ripple Factor: 0.48")
    print("  - PIV: Vm")
    print("  - Transformer Utilization: Excellent")
    print("  - No center-tap required")

# Run analysis if script is executed directly
if __name__ == "__main__":
    main()
    
    # Uncomment below lines to see performance analysis
    # analyze_rectifier_performance()
    # compare_rectifier_types()