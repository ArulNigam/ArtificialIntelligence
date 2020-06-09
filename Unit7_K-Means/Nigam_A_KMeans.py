# Name: Arul Nigam
# Period 3

''' Test cases:
6 https://cf.geekdo-images.com/imagepage/img/5lvEWGGTqWDFmJq_MaZvVD3sPuM=/fit-in/900x600/filters:no_upscale()/pic260745.jpg
10 cute_dog.jpg
6 turtle.jpg
'''
import math
import operator

import PIL
from PIL import Image
import urllib.request
import io, sys, os, random
import copy
############################ BELOW IS USED FOR RANDOM.CHOICES() ############################
from itertools import accumulate as _accumulate, repeat as _repeat
from bisect import bisect as _bisect


############################################################################################

def choose_random_means(k_count, img, pix):
    concat_pix = [c for x in pix for c in x]
    means = [choices([i for i in range(min(concat_pix), 1 + max(concat_pix))], k=3) for j in range(k_count)]
    return means


def choose_k_plus_plus_means(k_count, img, pix):
    concat_pix = [c for x in pix for c in x]
    for k in range(k_count):
        if k == 0:
            means = choices(pix, k=1)
        else:
            weights = [dist2(pix[i], means[k - 1]) for i in range(len(pix))]
            w = sum(weights)
            weights = [weight / w for weight in weights]
            means.append(choices(pix, weights, k=1)[0])
        # print(means)
    return means


def choices(population, weights=None, *, cum_weights=None, k=1):
    """Return a k sized list of population elements chosen with replacement.
    If the relative weights or cumulative weights are not specified,
    the selections are made with equal probability.
    """
    n = len(population)
    if cum_weights is None:
        if weights is None:
            _int = int
            n += 0.0  # convert to float for a small speed improvement
            return [population[_int(random.random() * n)] for i in _repeat(None, k)]
        cum_weights = list(_accumulate(weights))
    elif weights is not None:
        raise TypeError('Cannot specify both weights and cumulative weights')
    if len(cum_weights) != n:
        raise ValueError('The number of weights does not match the population')
    bisect = _bisect
    total = cum_weights[-1] + 0.0  # convert to float
    hi = n - 1
    return [population[bisect(cum_weights, random.random() * total, 0, hi)]
            for i in _repeat(None, k)]


# goal test: no hopping
def check_move_count(mc):
    return True


# calculate distance with the current color with each mean
# return the index of means
def dist(col, means):
    # minIndex, dist_sum = 0, 255 ** 2 + 255 ** 2 + 255 ** 2
    dist_to_clusters = {math.sqrt(sum([(c - m) ** 2 for c, m in zip(col, means[i])])): i for i in range(len(means))}
    return dist_to_clusters[min(list(dist_to_clusters.keys()))]
    # return minIndex


def dist2(col, mean):
    # minIndex, dist_sum = 0, 255 ** 2 + 255 ** 2 + 255 ** 2
    # print("c,m", col, mean)
    return math.sqrt(sum([(c - m) ** 2 for c, m in zip(col, mean)]))
    # return minIndex


def clustering(img, pix, cb, mc, means, count):
    temp_pb, temp_mc, temp_m = [[] for x in means], [], []
    temp_cb = [0 for x in means]
    pix_to_clusters = {i: 0 for i in pix}
    while sum([abs(mc[i]) for i in range(len(mc))]) != 0:
        # print("round", new_count)
        # temp_pix_to_clusters = copy.deepcopy(pix_to_clusters)
        temp_cb = copy.deepcopy(cb)
        for x in pix:
            pix_to_clusters[x] = dist(x, means)
        for cluster_num in range(len(means)):
            cluster_pixels = [x for x in pix if pix_to_clusters[x] == cluster_num]
            n = len(cluster_pixels)
            if n != 0:
                # print(n)
                means[cluster_num] = [sum([cluster_pixels[j][i] for j in range(n)]) / n for i in range(3)]
                '''if cluster_num == 0:
                    print(means[cluster_num])'''
            cb[cluster_num] = n
        mc = [cb[i] - temp_cb[i] for i in range(len(means))]
        count += 1
        '''if count == 2:
            print('first means:', means)
            print('starting sizes:', cb)'''  ###############################################
        # temp_mc = [(a - b) for a, b in zip(temp_cb, cb)]
        # print('diff', count, ':', mc)
    return cb, mc, means, pix_to_clusters


def update_picture(img, pix, means, pix_to_clusters):
    region_dict = {}
    visited = set()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # print("len vis", len(visited))
            if (i, j) not in visited:
                cluster = pix_to_clusters[pix[i, j]]
                visited = explore_region(i, j, cluster, visited, pix, pix_to_clusters, img)
                if cluster not in region_dict:
                    region_dict[cluster] = 0
                region_dict[cluster] += 1
    return pix, region_dict


def color_picture(pix, pix_to_clusters, k, img, means):
    total_cb = {i: 0 for i in range(k)}
    most_common_color = {i: {} for i in range(k)}
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            cluster = pix_to_clusters[pix[i, j]]
            total_cb[cluster] += 1
            if pix[i, j] not in most_common_color[cluster]:
                most_common_color[cluster][pix[i, j]] = 0
            most_common_color[cluster][pix[i, j]] += 1
    cluster_colors = []
    for c in range(k):
        mean_rgb = tuple([round(means[c][j]) for j in range(3)])
        cluster_colors.append(mean_rgb)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            color = cluster_colors[pix_to_clusters[pix[i, j]]]
            img.putpixel((i, j), color)
    return img, total_cb


def color_picture2(pix, pix_to_clusters, k, img):
    total_cb = {i: 0 for i in range(k)}
    most_common_color = {i: {} for i in range(k)}
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            cluster = pix_to_clusters[pix[i, j]]
            total_cb[cluster] += 1
            if pix[i, j] not in most_common_color[cluster]:
                most_common_color[cluster][pix[i, j]] = 0
            most_common_color[cluster][pix[i, j]] += 1
    cluster_colors = []
    for c in range(k):
        rgb = max(most_common_color[c].items(), key=operator.itemgetter(1))[0]
        print("RGB = ", rgb)
        cluster_colors.append(rgb)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            color = cluster_colors[pix_to_clusters[pix[i, j]]]
            img.putpixel((i, j), color)
    return img, total_cb


def explore_region2(i, j, cluster, visited, pix, pix_to_clusters, img):
    print("i,j", i, j)
    visited.add((i, j))
    neighbors = [[i - 1, j - 1], [i - 1, j], [i - 1, j + 1], [i, j - 1], [i, j + 1], [i + 1, j - 1], [i + 1, j],
                 [i + 1, j + 1]]
    for neighbor in neighbors:
        m = neighbor[0]
        n = neighbor[1]
        if (0 <= m < img.size[0]) and (0 <= n < img.size[1]) and (m, n) not in visited and int(
                pix_to_clusters[pix[m, n]]) == int(cluster):
            print("b", len(visited))
            to_add = explore_region2(m, n, cluster, visited, pix, pix_to_clusters, img)
            print("a", len(to_add) + len(visited))
            visited.update(to_add)
    return visited


def explore_region(i, j, cluster, visited, pix, pix_to_clusters, img):
    q = [(i, j)]
    visited.add((i, j))
    while len(q) != 0:
        # print("q", len(q))
        coordinate = q.pop()
        x = coordinate[0]
        y = coordinate[1]
        # visited.add((x, y))
        neighbors = [[x - 1, y - 1], [x - 1, y], [x - 1, y + 1], [x, y - 1], [x, y + 1], [x + 1, y - 1], [x + 1, y],
                     [x + 1, y + 1]]
        for neighbor in neighbors:
            m = neighbor[0]
            n = neighbor[1]
            if (0 <= m < img.size[0]) and (0 <= n < img.size[1]) and (m, n) not in visited and int(
                    pix_to_clusters[pix[m, n]]) == int(cluster):  # if valid
                q.insert(0, (m, n))
                visited.add((m, n))
    return visited


def distinct_pix_count(img, pix):
    cols = {}
    distinct_pixels = list(set([pix[i, j] for i in range(img.size[0]) for j in range(img.size[1])]))
    max_col, max_count = pix[0, 0], 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            col = pix[i, j]
            if col not in cols:  # new color
                cols[col] = [[i, j]]
            else:
                cols[col].append([i, j])
            if len(cols[col]) > max_count:
                max_count = len(cols[col])
                max_col = col
                # print(max_col)
    return len(cols.keys()), max_col, max_count, distinct_pixels


def count_regions(img, region_dict, pix, means, k):
    region_count = [region_dict[x] for x in range(k)]
    return region_count


def main():
    k = int(sys.argv[1])
    file = sys.argv[2]
    if not os.path.isfile(file):
        file = io.BytesIO(urllib.request.urlopen(file).read())
    img = Image.open(file)
    pix = img.load()  # pix[0, 0] : (r, g, b)
    print('Size:', img.size[0], 'x', img.size[1])
    print('Pixels:', img.size[0] * img.size[1])
    d_count, m_col, m_count, distinct_pixels = distinct_pix_count(img, pix)
    print('Distinct pixel count:', d_count)
    print('Most common pixel:', m_col, '=>', m_count)
    # print('Most common pixel:', (0, 0, 0), '=>', m_count)

    count_buckets = [0 for x in range(k)]
    move_count = [10 for x in range(k)]
    # means = choose_random_means(k, img, distinct_pixels)
    means = choose_k_plus_plus_means(k, img, distinct_pixels)
    ##############################################################print('random means:', means)
    count = 1
    '''while not check_move_count(move_count):
        count += 1'''
    # print(means)
    count_buckets, move_count, means, pix_to_clusters = clustering(img, distinct_pixels, count_buckets, move_count,
                                                                   means, count)
    # print(means)
    #    if count == 2:
    #       ####################33 print('first means:', means)
    #   #######################################################33     print('starting sizes:', count_buckets)
    pix, region_dict = update_picture(img, pix, means, pix_to_clusters)
    img, total_cb = color_picture(pix, pix_to_clusters, k, img, means)
    print('Final sizes:', list(total_cb.values()))
    print('Final means:')
    for i in range(len(means)):
        print('{}:'.format(i + 1), tuple(means[i]), '=>', total_cb[i])
        # print('{}:'.format(i + 1), (0, 0, 0), '=>', total_cb[i])
    # regions = count_regions(img, region_dict, pix, means, k)  # num of area fills
    print('Region counts:', ', '.join(map(str, list(region_dict.values()))))
    '''if not os.path.exists('kmeans'):
        os.mkdir('kmeans')'''
    img.save("kmeans/{}.png".format("2021anigam"), "PNG")
    '''
    Distinct regions:
       1: # of regions of means[0]
    Final regions:
       1: # of final regions of means[0] after taking care of step 3
    Save your file in the subdirectory, kmeans/userid.png
    '''
    img.show()


if __name__ == '__main__':
    sys.setrecursionlimit(2147483647)
    '''x = 4096 * (10 ** 4)
    threading.stack_size(x)
    thread = threading.Thread(target=main())
    thread.start()'''
    main()
