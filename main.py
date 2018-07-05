import matplotlib
import matplotlib.pyplot as plt
import mplcursors

from collections import namedtuple, Counter, defaultdict
from lxml import etree


# Handle matplotlib fonts
font_name = 'Source Han Sans TW'
matplotlib.rcParams['font.family'] = font_name
matplotlib.rcParams['axes.unicode_minus'] = False


# MATPLOTLIB
NORTH = 1
SOUTH = 0.8


# CMS INFORMATION
CMS_FILENAME = 'cms_value.xml'
CMSID = namedtuple('cmsid', ['id', 'way', 'km'])


# TARGET
TARGET = ['速']


def parse_cmsid(cmsid):
    id_, way, km = cmsid.split('-')[1:4]
    return CMSID(id_, way, float(km))


def read_cms():
    return etree.parse(CMS_FILENAME)


def get_cms_message(root, which):
    return [e.get('message') for e in root.xpath(f'//Info[contains(@cmsid, "{which}")]')]


def get_cms_info(root, which):
    return root.xpath(f'//Info[contains(@cmsid, "{which}")]')


def draw(root, which):
    cms = get_cms_info(root, which)
    msg = get_cms_message(root, which)

    c = Counter(msg)
    mc = c.most_common(15)
    for k, v in c.items():
        if '距離' in k or '車距' in k:
            if k not in set([i[0] for i in mc]):
                mc.append((k, v))

    mc_msg = [i[0] for i in mc]
    d = defaultdict(list)

    print(mc)
    for i in mc:
        print(i)
    for v in cms:
        msg = v.get('message')
        if msg in mc_msg:
            cmsid = parse_cmsid(v.get('cmsid'))
            if cmsid.way in ['S', 'N']:
                d[f'{msg.replace(" ", "")}_{cmsid.way}'].append(cmsid.km)

    plt.figure(figsize=(20, 12), dpi=100)
    plt.ylim(-5, 5)
    plt.xlim(0, 375)
    for k, v in d.items():
        way = SOUTH if 'S' in k else NORTH
        plt.plot(v, [way] * len(v), 'o', label=k)
        for t in TARGET:
            if t in k:
                for x in v:
                    plt.annotate(k, xy=(x, way), xytext=(0, (1 if way == NORTH else -1) * (10 * len(k))),
                        textcoords='offset points', rotation=45,
                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
                # We found one, don't redraw again if it will match again
                break

    plt.legend(loc='lower right', bbox_to_anchor=(1.1, -0.2))
    plt.title('國道一號 CMS 超速類型')
    mplcursors.cursor(hover=True)
    plt.savefig('N1_speeding.jpg', dpi=100)



def main():
    root = read_cms()
    draw(root, 'N1')


if __name__ == '__main__':
    main()
