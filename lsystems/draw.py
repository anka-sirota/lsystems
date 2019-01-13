from pysvg.turtle import Turtle, Vector
import json
import svgwrite
DEFAULT_ANGLE = 90
DEFAULT_DISTANCE = 30
DEFAULT_ITERATIONS = 2


def iterate_lsystem(lconfig):
    iterations = lconfig.get('iterations', DEFAULT_ITERATIONS)
    start = lconfig['start']
    rules = lconfig['rules']

    commands = start
    print(f'Iterating from {start} with {rules}, {iterations} times')
    while iterations:
        chunks = []
        for symbol in commands:
            replacement = rules.get(symbol)
            if not replacement:
                chunks.append(symbol)
            else:
                chunks.append(replacement)
        commands = ''.join(chunks)
        # print(f'Iteration {iterations}: {commands}')
        iterations -= 1
    return commands


def draw_lsystem(name, commands):
    angle = lconfig.get('angle', DEFAULT_ANGLE)
    distance = lconfig.get('distance', DEFAULT_DISTANCE)

    t = Turtle()
    t.moveTo(Vector(0, 0))
    t.penDown()
    output_file = f'./testoutput/{name}.svg'
    for cmd in commands:
        if cmd in ('F', 'G'):
            t.forward(distance)
        elif cmd == '+':
            t.left(angle)
        elif cmd == '-':
            t.right(angle)
    t.penDown()
    points = [_.split(',') for _ in t.getSVGElements()[0].get_points().split('  ') if _]

    dwg = svgwrite.Drawing(output_file)
    polyline = dwg.polyline(points=points, stroke='black', fill='none', stroke_width=2)
    dwg.add(polyline)
    dwg.fit(horiz='left', vert='middle', scale='meet')
    dwg.save()
    print(f'Saved to {output_file}')


if __name__ == '__main__':
    with open('lsystems.json') as f:
        config = json.load(f)

    settings = config.get('settings', {})
    systems = config.get('systems', {})

    if not systems:
        print('Nothing to draw, alas.')

    for name, lconfig in systems.items():
        draw_lsystem(name, iterate_lsystem(lconfig))
