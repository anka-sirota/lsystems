from pysvg.turtle import Turtle, Vector
import json
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
    print(f'Iterating from {axiom} with {rules}, {iterations} times')
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
    angle = lconfig.get('angle')
    angle_left = lconfig.get('angle_left')
    angle_right = lconfig.get('angle_right')
    if not angle_right and not angle_right and not angle:
        angle = DEFAULT_ANGLE
    distance = lconfig.get('distance', DEFAULT_DISTANCE)

    t = Turtle()
    t.moveTo(Vector(0, 0))
    t.penDown()
    output_file = f'./testoutput/{name}.svg'
    for cmd in commands:
        if cmd in ('F', 'G'):
            t.forward(distance)
        elif cmd == '+':
            t.left(angle_left or angle)
        elif cmd == '-':
            t.right(angle_right or angle)
    t.penDown()
    points = [[float(__) for __ in _.split(',')] for _ in t.getSVGElements()[0].get_points().split('  ') if _]
    bbox = bounding_box(points)

    dwg = svgwrite.Drawing(output_file)
    polyline = dwg.polyline(points=points, stroke='black', fill='none', stroke_width=2)
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
