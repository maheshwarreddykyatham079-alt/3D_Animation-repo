import json
import numpy as np
from manim import *

# -------------------------------
# Load JSON Spec
# -------------------------------
json_spec = """
{
  "animation_title": "Power Factor Correction - Stage 1: Full Bridge Rectifier",
  "goal": "Visualize how AC input is rectified to pulsating DC using a full bridge rectifier.",
  "circuit_elements": [
    {
      "type": "source",
      "name": "AC Input",
      "waveform": "sine",
      "voltage": "230Vrms"
    },
    {
      "type": "rectifier",
      "name": "Full Bridge Rectifier",
      "components": ["D1", "D2", "D3", "D4"]
    },
    {
      "type": "load",
      "name": "Resistive Load",
      "value": "10 Ohm"
    }
  ],
  "animation_steps": [
    {
      "step": 1,
      "description": "Show AC source feeding the rectifier."
    },
    {
      "step": 2,
      "description": "Highlight conducting diodes during positive half cycle (D1 & D2)."
    },
    {
      "step": 3,
      "description": "Highlight conducting diodes during negative half cycle (D3 & D4)."
    },
    {
      "step": 4,
      "description": "Plot and animate the output waveform (pulsating DC)."
    }
  ],
  "visual_elements": {
    "show_current_flow": true,
    "highlight_active_components": true,
    "show_waveforms": ["input_voltage", "output_voltage"],
    "colors": {
      "positive_cycle": "red",
      "negative_cycle": "blue",
      "output": "green"
    }
  },
  "output_format": {
    "type": "animation",
    "duration": "10s",
    "style": "educational",
    "export": "mp4"
  }
}
"""

spec = json.loads(json_spec)

# -------------------------------
# Manim Scene
# -------------------------------
class FullBridgeRectifier(Scene):
    def construct(self):
        title = Text(spec["animation_title"], font_size=36).to_edge(UP)
        self.play(Write(title))

        # Step 1: Show AC source feeding rectifier
        ac_label = Text("AC Input", font_size=28).shift(LEFT*4)
        load_label = Text("Resistive Load", font_size=28).shift(RIGHT*4)
        self.play(FadeIn(ac_label), FadeIn(load_label))
        
        # Wires (simplified representation of full bridge)
        rectifier_box = Rectangle(color=WHITE, width=4, height=2).shift(RIGHT*0)
        rectifier_text = Text("Bridge Rectifier", font_size=24).move_to(rectifier_box.get_center())
        self.play(Create(rectifier_box), Write(rectifier_text))

        # Step 2: Highlight D1, D2 conduction (positive half cycle)
        d12_text = Text("D1 & D2 conducting", color=spec["visual_elements"]["colors"]["positive_cycle"]).shift(DOWN*2)
        self.play(Write(d12_text))
        self.wait(1)
        self.play(FadeOut(d12_text))

        # Step 3: Highlight D3, D4 conduction (negative half cycle)
        d34_text = Text("D3 & D4 conducting", color=spec["visual_elements"]["colors"]["negative_cycle"]).shift(DOWN*2)
        self.play(Write(d34_text))
        self.wait(1)
        self.play(FadeOut(d34_text))

        # Step 4: Show input & output waveforms
        axes = Axes(x_range=[0, 2*np.pi, np.pi/2], y_range=[-1.2, 1.2, 0.5],
                    x_length=6, y_length=3, axis_config={"color": WHITE}).shift(DOWN*2.5)
        labels = axes.get_axis_labels(x_label="t", y_label="V")
        self.play(Create(axes), Write(labels))

        # Input sine
        sine_graph = axes.plot(lambda x: np.sin(x), color=spec["visual_elements"]["colors"]["positive_cycle"])
        self.play(Create(sine_graph), run_time=2)

        # Output rectified
        rectified_graph = axes.plot(lambda x: np.abs(np.sin(x)), color=spec["visual_elements"]["colors"]["output"])
        self.play(Create(rectified_graph), run_time=2)

        self.wait(2)
