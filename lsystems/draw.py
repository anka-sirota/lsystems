from pysvg.turtle import Turtle, Vector
import json
import random
import svgwrite
DEFAULT_ANGLE = 90
DEFAULT_DISTANCE = 30
DEFAULT_ITERATIONS = 2


def bounding_box(points):
    x_coordinates, y_coordinates = zip(*points)
    return [(min(x_coordinates), min(y_coordinates)),
            (max(x_coordinates), max(y_coordinates))]


def iterate_lsystem(lconfig):
    iterations = lconfig.get('iterations', DEFAULT_ITERATIONS)
    axiom = lconfig['axiom']
    rules = lconfig['rules']

    commands = axiom
    while iterations:
        chunks = []
        for symbol in commands:
            replacement = rules.get(symbol, symbol)
            chunks.append(replacement)
        commands = ''.join(chunks)
        iterations -= 1
    # print(f'Iteration {iterations}: {commands}')
    return commands


def draw_lsystem(name, commands):
    angle = lconfig.get('angle')
    angle_left = lconfig.get('angle_left')
    angle_right = lconfig.get('angle_right')
    if not angle_right and not angle_right and not angle:
        angle = DEFAULT_ANGLE
    angle_chaos = lconfig.get('angle_chaos')
    distance = lconfig.get('distance', DEFAULT_DISTANCE)
    draw_symbols = lconfig.get('draw', 'FG')

    t = Turtle()
    t.moveTo(Vector(0, 0))
    t.penDown()
    output_file = f'./testoutput/{name}.svg'
    stack = []
    for cmd in commands:
        if cmd in draw_symbols:
            t.forward(distance)
        elif cmd == '[':
            stack.append((t._position, t.getOrientation()))
        elif cmd == ']':
            position, orientation = stack.pop()
            t.moveTo(position)
            t.setOrientation(orientation)
        elif cmd == '+':
            chaos = 1
            if angle_chaos:
                chaos = random.uniform(1, 1 + angle_chaos)
            t.left((angle_left or angle) * chaos)
        elif cmd == '-':
            chaos = 1
            if angle_chaos:
                chaos = random.uniform(1, 1 + angle_chaos)
            t.right((angle_left or angle) * chaos)
    t.finish()
    points = [[float(__) for __ in _.split(',')] for _ in t.getSVGElements()[0].get_points().split('  ') if _]
    bbox = bounding_box(points)

    dwg = svgwrite.Drawing(output_file)
    polyline = dwg.polyline(points=points, stroke='black', fill='none', stroke_width=6)
    dwg.add(polyline)
    polyline.translate(-bbox[0][0], -bbox[0][1])
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
