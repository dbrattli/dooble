from dooble.marble import Marble, Observable, Operator


def create_observable(layer):
    part = 0
    step = len(layer[part])

    part += 1
    is_child = False
    if layer[part] == '+':
        is_child = True
        part += 1
        step += 1

    start = step if is_child is False else step - 1
    observable = Observable(start, is_child=is_child)
    for ts in layer[part]:
        if 'ts' in ts and ts['ts'] is not None:
            step += 1
        else:
            item = ts['item']
            if item == '+':
                observable.on_observable_at(step)
            else:
                observable.on_next_at(item, step)
            step += len(item)

    part += 1
    completion = layer[part]

    if completion == '|':
        observable.on_completed_at(step)
    elif completion == '*':
        observable.on_error_at(step)
    else:
        observable.on_continued_at(step)

    return observable


def create_operator(layer):
    step = 0
    start = step

    content = layer[1]
    text = content.strip()

    step += 1
    operator = Operator(start, step + len(content) , text)

    return operator


def create_marble_from_ast(ast):
    marble = Marble()

    for layer in ast:
        if 'obs' in layer and layer['obs'] is not None:
            marble.add_observable(create_observable(layer['obs']))
        elif 'op' in layer and layer['op'] is not None:
            marble.add_operator(create_operator(layer['op']))

    marble.build()
    return marble
