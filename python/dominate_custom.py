#!/usr/bin/env python3

from dominate import tags, document, util


def item(*args, flow='row', **kwargs):
    kwargs['style'] = f"""
    display: flex;
    flex-direction: {flow};
    image-rendering: crisp-edges;
    """ + kwargs.get('style', "")
    return tags.div(*args, **kwargs)


def grid(items, *args, flow='row', **kwargs):

    if flow == 'row':
        grid_template = f'grid-template-columns: {"min-content " * len(items)}'
    else:
        grid_template = f'grid-template-rows: {"min-content " * len(items[0])}'

    kwargs['style'] = f"""
        display: grid;
        {grid_template};
        grid-auto-flow: {flow};
    """ + kwargs.get('style', "")

    return tags.div(items, *args, **kwargs)


cols = []
for a in range(3):
    row = []
    for b in range(4):
        # row.append(item(f"{a} {b}", style="foo", flow='column'))
        row.append(item(
            tags.p(a),
            tags.p(b),
            flow='row',
            style='width: 100px;'
        ))
    cols.append(row)

with document('helloooo world') as d:
    grid(cols, flow='column')
    tags.p("end")

open('/tmp/out.html', 'w').write(d.render())