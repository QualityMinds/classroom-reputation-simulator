import matplotlib as mpl
import matplotlib.pyplot as plt

def chart(data, groups, colors, title):
    hatch_styles = ['//', '-' , 'xx', 'oo', 'OO', '..', '**']
    plt.rcParams['hatch.linewidth'] = 0.5

    def count_members(data_set, group):
        return len([l for (_, l, _) in data_set if l == group])
    
    plt.figure()

    # draw group chart
    group_index = 0
    for g in groups:
        count = count_members(data, g)
        plt.axvspan(group_index,
                    group_index + count,
                    facecolor=colors[g],
                    alpha=.5)

        plt.axvspan(group_index,
                    group_index + count,
                    facecolor="None",
                    hatch=hatch_styles[groups.index(g) % len(hatch_styles)],
                    edgecolor = 'grey')

        group_index += count

    # draw bar chart
    for (index, (d, g, label)) in enumerate(data):
        rect = plt.bar(index,
                       d,
                       align='edge',
                       alpha=1,
                       width=1,
                       edgecolor='black',
                       color=colors[g],
                       hatch=hatch_styles[groups.index(g) % len(hatch_styles)])
        set_label(plt, rect, label)

    # chart labelling a.s.o
    plt.ylabel('Scores')
    plt.title(title)
    return plt


def set_label(plot, bars, label):
    for bar in bars:
        height = bar.get_height()
        plot.text(bar.get_x() + bar.get_width() / 2., height, label, ha='center', va='bottom')
