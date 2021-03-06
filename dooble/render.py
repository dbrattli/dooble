from math import pi
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from dooble.marble import Operator, Observable, Item

area = pi * 100
end_area = pi * 50


def render_to_file(marble, filename, theme):
    height = len(marble.layers) * 0.7
    fig, ax = plt.subplots(figsize=(6.4, height), dpi=100)

    def plt_y(y):
        return len(marble.layers) - y - 1

    # higher observable links    
    for link in marble.higher_order_links:
        ax.plot(
            [link.from_x, link.to_x],
            [plt_y(link.from_y), plt_y(link.to_y)],
            color=theme.timeline_color, linestyle='-',
            linewidth='2', zorder=0)

    # item links
    for link in marble.item_links:
        ax.plot(
            [link.from_x, link.to_x],
            [plt_y(link.from_y), plt_y(link.to_y)],
            color=theme.item_link_color, linestyle=':',
            linewidth='1', zorder=0)
        ax.scatter(
            [link.to_x], [plt_y(link.to_y) + 0.3],
            color=theme.item_link_color, marker='v', linewidth='1')

    # label links
    for link in marble.label_links:
        ax.plot(
            [link.from_x, link.to_x],
            [plt_y(link.from_y), plt_y(link.to_y)],
            color=theme.label_link_color, linestyle='--',
            linewidth='1', zorder=0)
        ax.scatter(
            [link.to_x], [plt_y(link.to_y) + 0.3],
            color=theme.label_link_color, marker='v', linewidth='1')

    for layer_index, layer in enumerate(marble.layers):
        if type(layer) is Observable:
            observable = layer
            # time line
            ax.plot(
                [observable.start, observable.end],
                [plt_y(layer_index), plt_y(layer_index)],
                color=theme.timeline_color, linestyle='-',
                linewidth='2',
                zorder=0)

            # end marker
            if observable.completed is not None:
                ax.scatter(
                    [observable.completed], [plt_y(layer_index)],
                    s=end_area, color=theme.timeline_color, marker='|', linewidth='2')
            elif observable.error is not None:
                ax.scatter(
                    [observable.error], [plt_y(layer_index)], 
                    s=end_area, color=theme.timeline_color, marker='x', linewidth='2')
            else:
                ax.scatter(
                    [observable.end], [plt_y(layer_index)],
                    s=end_area, color=theme.timeline_color, marker='>')

            # items
            x = []
            y = []
            for item in observable.items:
                x.append(item.at)
                y.append(plt_y(layer_index))
            ax.scatter(x, y, s=area, c=None, edgecolors=theme.timeline_color, color=theme.item_color, alpha=1.0, linewidth='2')

            # label
            if observable.label is not None:
                ax.scatter(
                    [observable.start], [plt_y(layer_index)], s=area, c=None, 
                    edgecolors=theme.operator_edge_color, 
                    color=theme.label_color, 
                    alpha=1.0, linewidth='2')
                ax.text(observable.start, plt_y(layer_index), observable.label, horizontalalignment='center', verticalalignment='center')

            # items text
            for item in observable.items:
                text = str(item.item) if type(item) is Item else ''
                ax.text(item.at, plt_y(layer_index), text, horizontalalignment='center', verticalalignment='center')

        elif type(layer) is Operator:
            operator = layer
            y = plt_y(layer_index) - 0.15
            ax.add_patch(Rectangle(
                (operator.start, y), operator.end-operator.start, 0.35,
                alpha=1, edgecolor=theme.operator_edge_color,
                facecolor=theme.operator_color,
                linewidth='2'))
            ax.text(
                operator.start + (operator.end-operator.start)/2, y + 0.15,
                operator.text,
                horizontalalignment='center', verticalalignment='center')

    ax.set_axis_off()
    plt.savefig(filename, dpi=fig.dpi)
    plt.close()
