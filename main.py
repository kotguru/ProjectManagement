from tkinter import *

# MAX_TIME = 20
NUM_WORKS = 4


class Work:
    def __init__(self, name, duration=1, not_earlier=None, not_later=None):
        if not_later is None:
            not_later = list()
        if not_earlier is None:
            not_earlier = list()
        self.name = name
        self.duration = duration
        self.not_earlier = not_earlier
        self.not_later = not_later

    def to_string(self):
        return str('\033[33mWork {};\nDuration = {}\nNot later than: {}\n'
                   'Not earlier than: {}\n'.format(self.name, self.duration, self.not_later, self.not_earlier))


def init_works():
    start_work = list()
    for i in range(NUM_WORKS):
        T = Work('Work ' + str(i+1))
        start_work.append(T)
    return start_work


def input_data_parser(in_str):
    name = in_str[:2]
    start_out = in_str.find(":")
    end_out = in_str.find(">")
    start_in = end_out + 2

    return [name, in_str[start_out + 2: end_out - 2], in_str[start_in:]]


def critical_path(cur_len, cur_nodes, work):
    current_len = 0
    current_nodes = []
    for prev_work in work.not_earlier:
        current_len = cur_len
        current_nodes = cur_nodes.copy()

        current_len += prev_work.duration
        current_nodes.append(prev_work)
        #         tmp_nodes_in_path[cur_len] += (prev_work.name + "; ")

        if len(prev_work.not_earlier) == 0:
            paths.append(current_len)
            nodes_in_path[current_len] = current_nodes
        #             nodes_in_path[cur_len] = tmp_nodes_in_path[cur_len]
        else:
            critical_path(current_len, current_nodes, prev_work)


if __name__ == '__main__':
    works = list()
    T1 = Work('Work 1', duration=3)
    T2 = Work('Work 2', duration=8)
    T3 = Work('Work 3', duration=7)
    T4 = Work('Work 4', duration=10)

    T1.not_earlier = [T3, T2]
    T1.not_later = [T4]

    T2.not_earlier = [T3]
    T2.not_later = [T4]

    T3.not_earlier = []
    T3.not_later = []

    T4.not_earlier = [T1, T2, T3]
    T4.not_later = []

    works.append(T1)
    works.append(T2)
    works.append(T3)
    works.append(T4)

    paths = list()
    nodes_in_path = dict()
    cur_nodes = list()

    cur_len = 0

    for work in works:
        cur_len = work.duration
        cur_nodes.clear()
        cur_nodes.append(work)

        if len(work.not_earlier) != 0:
            critical_path(cur_len, cur_nodes, work)
        else:
            paths.append(cur_len)
            nodes_in_path[cur_len] = cur_nodes

    root = Tk()
    c = Canvas(root, width=100 * NUM_WORKS, height=100 * NUM_WORKS, bg='white')
    c.pack()
    for i in range(len(nodes_in_path[max(paths)])):
        if i > 0:
            c.create_line(100 * i, 40, 100 * i + 10, 40)
        c.create_rectangle(10 + 100 * i, 10, 100 + 100 * i, 60)
        c.create_text(55 + 100 * i, 30, text=nodes_in_path[max(paths)][i].name)
        # c.create_rectangle(60, 80, 140, 190,
        #
        #                    fill='yellow',
        #                    outline='green',
        # width=3)
        # activedash=(5, 4))
    c.create_text(100 * NUM_WORKS - 70, 100 * NUM_WORKS - 30, text="Critical path = " + str(max(paths)))
    root.mainloop()
