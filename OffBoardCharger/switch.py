import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(config={'background': 'white'}) as d:
    # Voltage source: + on top, - on bottom
    v = d.add(elm.SourceV().up().label('5V'))

    # Positive terminal path: → Resistor → Node Vout
    d += elm.Line().right()
    r = d.add(elm.Resistor().right().label('10kΩ'))
    d += elm.Line().right()
    dot = d.add(elm.Dot(open=True).label('Vout', loc='top'))

    # Capacitor from Vout down to ground
    d += elm.Capacitor().down().label('1µF')
    g = d.add(elm.Ground())  # ground symbol

    # Negative terminal connection: horizontal line to ground (parallel to resistor)
    d += elm.Line().right().at(v.start).to(g.start)

    d.save('rc_circuit_vout_horizontal_ground.png', transparent=False, facecolor='white')

plt.close('all')