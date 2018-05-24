import numpy as np


def print_metrics(name, centrality_vector, groups):
    d, c, i = get_metrics(centrality_vector, groups)
    print("")
    print("######## Final Metrics: " + name + " ########")
    print("Distinction: " + str(d))
    print("Correctness: " + str(c))
    print("Inversion Quality: " + str(i))


def print_stddev_metrics(name, intermediate_results, groups):
    mean_dis, std_dis, mean_cor, std_cor, mean_inv_q, std_inv_q = get_metrics_stddev(intermediate_results, groups)
    print("")
    print("######## Mean & Std. Dev.: " + name + " ########")
    print("Distinction:       {} ({})".format(mean_dis, std_dis))
    print("Correctness:       {} ({})".format(mean_cor, std_cor))
    print("Inversion Quality: {} ({})".format(mean_inv_q, std_inv_q))


def get_metrics_stddev(intermediate_results, groups):
    dis_list = list()
    cor_list = list()
    inv_q_list = list()

    for result in intermediate_results:
        dis, cor, inv_q = get_metrics(result, groups)
        dis_list.append(dis)
        cor_list.append(cor)
        inv_q_list.append(inv_q)

    mean_dis = np.mean(dis_list)
    std_dis = np.std(dis_list)

    mean_cor = np.mean(cor_list)
    std_cor = np.std(cor_list)

    mean_inv_q = np.mean(inv_q_list)
    std_inv_q = np.std(inv_q_list)

    return mean_dis, std_dis, mean_cor, std_cor, mean_inv_q, std_inv_q


def count_members(data, group):
    return len([l for (_, l, _) in data if l == group])


def in_correct_zone(groups, centrality_vector, label, index):
    minimum = 0
    maximum = 0
    for i in range(0, len(groups)):
        if groups[i] == label:
            maximum = minimum + count_members(centrality_vector, label)
            break
        else:
            minimum += count_members(centrality_vector, groups[i])

    return minimum <= index < maximum


def convert_to_ranking_array(groups, centrality_vector):
    result = list()
    for i in range(0, len(centrality_vector)):
        for j in range(0, len(groups)):
            if centrality_vector[i][1] == groups[j]:
                result.append(j)
    return result


def correctness(centrality_vector, groups):
    count = max(1, len(centrality_vector))
    metric = 0
    for i in range(0, count):
        if in_correct_zone(groups, centrality_vector, centrality_vector[i][1], i):
            metric += 1
        metric /= count
    return metric


def distinction(centrality_vector, groups):
    count = max(1, len(centrality_vector))
    metric = 0
    average_diff = 0

    for i in range(0, count - 1):
        average_diff += centrality_vector[i + 1][0] - centrality_vector[i][0]

    average_diff = average_diff / count

    curr_idx = 0
    for i in range(0, len(groups) - 1):
        curr_idx += count_members(centrality_vector, groups[i])
        metric += (centrality_vector[curr_idx][0] - centrality_vector[curr_idx - 1][0]) / average_diff

    if len(groups) > 1:
        metric /= (len(groups) - 1)

    return metric


def inversion_quality(centrality_vector, groups):
    inversions = 0
    count = len(centrality_vector)
    ranked_arr = convert_to_ranking_array(groups, centrality_vector)
    for i in range(0, count):
        for j in range(0, i):
            if ranked_arr[j] > ranked_arr[i]:
                inversions += 1

    max_inversions = (count * (count - 1)) / 2

    for group in groups:
        group_size = count_members(centrality_vector, group)
        max_inversions -= (group_size * (group_size - 1)) / 2

    metric = 1 - (inversions / max_inversions)
    return metric


def get_metrics(centrality_vector, groups):
    d = distinction(centrality_vector, groups)
    c = correctness(centrality_vector, groups)
    i = inversion_quality(centrality_vector, groups)
    return d, c, i
