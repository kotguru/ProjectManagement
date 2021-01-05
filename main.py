from tkinter import *

MAX_TIME = 50
NUM_WORKS = 6


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
        self.early_start = 0
        self.late_start = 0
        self.early_end = MAX_TIME
        self.late_end = MAX_TIME

    def to_string(self):
        return str('\033[36m{}:\n'
                   'Duration = {}\n'
                   'Not later than: {}\n'
                   'Not earlier than: {}\n'
                   'Early start = {}\n'
                   'Late start = {}\n'
                   'Early end = {}\n'
                   'Late end = {};\n'.format(self.name, self.duration, [self.not_later[i].name for i in range(len(self.not_later))],
                                             [self.not_earlier[i].name for i in range(len(self.not_earlier))], self.early_start,
                                            self.late_start, self.early_end, self.late_end))


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


def later_to_earlier():
    for work in works:
        if len(work.not_later) != 0:
            for late_work in work.not_later:
                if work not in late_work.not_earlier:
                    late_work.not_earlier.append(work)


def earlier_to_later():
    for work in works:
        if len(work.not_earlier) != 0:
            for late_work in work.not_earlier:
                if work not in late_work.not_later:
                    late_work.not_later.append(work)


def critical_path(cur_len, cur_nodes, work):
    current_len = 0
    current_nodes = []
    for prev_work in work.not_earlier:
        # if flag:
        #     work.early_start += max([work.not_earlier[i].duration for i in range(len(work.not_earlier))])
        #     flag = False
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


def max_work(works):
    max_len = 0
    index = 0
    if len(works) == 0:
        return -1
    for i in range(len(works)):
        if works[i].duration > max_len:
            max_len = works[i].duration
            index = i
    return index


def leeway_helper_to(work, works_in, early_start, temp_nodes):
    temp_nodes.update(work.not_earlier)
    max_index = max_work(work.not_earlier)

    if max_index == -1:
        return works_in, early_start, temp_nodes

    early_start += work.not_earlier[max_index].duration
    works_in.append(work.not_earlier[max_index])
    works_in, early_start, temp_nodes = leeway_helper_to(work.not_earlier[max_index], works_in, early_start, temp_nodes)

    return works_in, early_start, temp_nodes


def leeway_helper_after(work, works_in, late_start, temp_nodes):
    temp_nodes.update(work.not_later)
    max_index = max_work(work.not_later)

    if max_index == -1:
        return works_in, late_start, temp_nodes

    late_start += work.not_later[max_index].duration
    works_in.append(work.not_later[max_index])
    works_in, late_start, temp_nodes = leeway_helper_after(work.not_later[max_index], works_in, late_start, temp_nodes)

    return works_in, late_start, temp_nodes


def leeway(work):
    temp_nodes = set(work.not_earlier.copy())
    works_in = list()
    early_start = 0

    works_in, early_start, temp_nodes = leeway_helper_to(work, works_in, early_start, temp_nodes)

    for tmp_work in temp_nodes:
        if tmp_work not in works_in:
            works_in.append(tmp_work)
            early_start += tmp_work.duration

    work.early_start = early_start

    temp_nodes = set(work.not_later.copy())
    works_in = list()
    late_start = 0

    works_in, late_start, temp_nodes = leeway_helper_after(work, works_in, late_start, temp_nodes)

    for tmp_work in temp_nodes:
        if tmp_work not in works_in:
            works_in.append(tmp_work)
            late_start += tmp_work.duration

    work.late_start = max_path - late_start - work.duration
    work.late_end = max_path
    work.early_end = work.early_start + work.duration


if __name__ == '__main__':
    works = list()
    T1 = Work('Work 1', duration=3)
    T2 = Work('Work 2', duration=8)
    T3 = Work('Work 3', duration=7)
    T4 = Work('Work 4', duration=10)
    T5 = Work('Work 5', duration=2)
    T6 = Work('Work 6', duration=1)

    T1.not_earlier = [T3, T2]
    T1.not_later = [T4]

    T2.not_earlier = [T3]
    T2.not_later = [T4]

    T3.not_earlier = []
    T3.not_later = [T5]

    T4.not_earlier = [T1, T2, T3]
    T4.not_later = []

    # T5.not_earlier = [T1, T2, T3]
    T6.not_earlier = [T5]

    works.append(T1)
    works.append(T2)
    works.append(T3)
    works.append(T4)
    works.append(T5)
    works.append(T6)

    paths = list()
    nodes_in_path = dict()
    cur_nodes = list()

    cur_len = 0
    later_to_earlier()
    earlier_to_later()

    for work in works:
        cur_len = work.duration
        cur_nodes.clear()
        cur_nodes.append(work)

        if len(work.not_earlier) != 0:
            critical_path(cur_len, cur_nodes, work)
        else:
            paths.append(cur_len)
            nodes_in_path[cur_len] = cur_nodes

    max_path = max(paths)

    for work in works:
        # if work not in nodes_in_path[max_path]:
        # if work not in nodes_in_path[max_path]:
        leeway(work)

        if work in nodes_in_path[max_path]:
            work.late_start = work.early_start
            work.late_end = work.early_end

        print(work.to_string())

    print("\033[30mCritial path: \033[33m")
    print("START -->", end=' ')
    for i in nodes_in_path[max_path][-1::-1]:
        print(i.name + " -->", end=' ')

    print('END')
    print("\033[32mCritial path len = " + str(max_path))

    root = Tk()
    c = Canvas(root, width=100 * NUM_WORKS, height=100 * NUM_WORKS, bg='white')
    c.pack()
    for i in range(len(nodes_in_path[max_path][-1::-1])):
        if i > 0:
            c.create_line(100 * i, 40, 100 * i + 10, 40)
        # else:
        #     if len(nodes_in_path[max_path][-1::-1][i].not_later) > 1:
        #         for j in range(len(nodes_in_path[max_path][-1::-1][i].not_later)):
        #             k = nodes_in_path[max_path][-1::-1][i].not_later[j]
        #             if k not in nodes_in_path[max_path]:
        #                 c.create_line(100 * i + 50, 60 * (j + 1), 100 * (i + 1) + 10, 40 * (j + 2))
        #                 c.create_rectangle(100 * (i + 1) + 10, 40 * (j + 2), 100 * (i + 1) + 100 * (i + 1), 40 + 40 * (j + 2))
        #                 c.create_text(55 + 100 * (i + 1), 30 * (j + 2), text=k.name)
        c.create_rectangle(10 + 100 * i, 10, 100 + 100 * i, 60)
        c.create_text(55 + 100 * i, 30, text=nodes_in_path[max_path][-1::-1][i].name)
        # c.create_rectangle(60, 80, 140, 190,
        #
        #                    fill='yellow',
        #                    outline='green',
        # width=3)
        # activedash=(5, 4))
    c.create_text(100 * NUM_WORKS - 70, 100 * NUM_WORKS - 30, text="Critical path = " + str(max(paths)))
    root.mainloop()
