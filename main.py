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

    def CriticalPath(self):
        cur_path = 0
        cur_name = None
        for prev_work in self.not_earlier:
            if prev_work.duration > cur_path:
                cur_path = prev_work.duration
                cur_name = prev_work.name
        return cur_path, cur_name

    def ToString(self):
        return str('\033[33mWork {};\nDuration = {}\nNot later than: {}\n'
                   'Not earlier than: {}\n'.format(self.name, self.duration, self.not_later, self.not_earlier))


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    works = list()
    T3 = Work('Work 3', duration=7)
    T4 = Work('Work 4', duration=10, not_earlier=[T3])
    T2 = Work('Work 2', duration=8, not_earlier=[T3], not_later=[T4, T3])
    T1 = Work('Work 1', duration=3, not_earlier=[T3, T2], not_later=[T4])

    works.append(T1)
    works.append(T2)
    works.append(T3)
    works.append(T4)
    # works.append(Work('T1', not_earlier=[Work('T3'), Work('T2')], not_later=[Work('T4')]))
    # works.append(Work('T2', not_earlier=[Work('T1')], not_later=[Work('T4'), Work('T1')]))

    works_in_cr_path = list()
    critical_path_len = 0
    for work in works:
        work_len, work_name = work.CriticalPath()
        if work_name not in works_in_cr_path:
            critical_path_len += work_len
            if work_name is not None:
                works_in_cr_path.append(work_name)
        # print(work.ToString())
        pass

    print(works_in_cr_path)

    root = Tk()
    c = Canvas(root, width=100*NUM_WORKS, height=100*NUM_WORKS, bg='white')
    c.pack()
    for i in range(len(works)):
        if i > 0:
            c.create_line(100*i, 40, 100*i + 10, 40)
        c.create_rectangle(10 + 100*i, 10, 100 + 100*i, 60)
        c.create_text(55 + 100*i, 30, text=works[i].name)
        # c.create_rectangle(60, 80, 140, 190,
        #
        #                    fill='yellow',
        #                    outline='green',
                           # width=3)
                           # activedash=(5, 4))
    c.create_text(100*NUM_WORKS - 70, 100*NUM_WORKS - 30, text="Critical path = " + str(critical_path_len))
    root.mainloop()