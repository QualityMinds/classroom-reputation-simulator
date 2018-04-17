import matplotlib.pyplot as plt
import numpy as np


def chart(data, groups, colors, title):
    hatchStyles = ['//', '-' , 'xx' , 'oo' , 'OO' , '..' , '**']
    plt.rcParams['hatch.linewidth'] = 0.5

    def count_members(data, group):
        return len([l for (_, l, _) in data if l == group])
    
    values = [a for (a, _, _) in data]
    y_range = np.arange(min(values), max(values) + 1)
    plt.figure()
    # draw group chart
    group_index = 0
    for g in groups:
        count = count_members(data, g)
        plt.axvspan(group_index, group_index + count, facecolor=colors[g], alpha=.5)
        plt.axvspan(group_index, group_index + count, facecolor="None", hatch=hatchStyles[groups.index(g) % len(hatchStyles)], edgecolor = 'grey')
        group_index += count
    # draw bar chart
    for (index, (d, g, label)) in enumerate(data):
        rect = plt.bar(index, d, align='edge', alpha=1, width=1, edgecolor='black', color=colors[g], hatch=hatchStyles[groups.index(g) % len(hatchStyles)])
        setLabel(plt, rect, label)
    # chart labelling a.s.o
    plt.ylabel('Scores')
    plt.title(title)
    return plt


def setLabel(plot, rects, label):
    for rect in rects:
        height = rect.get_height()
        plot.text(rect.get_x() + rect.get_width()/2., height, label, ha='center', va='bottom')
