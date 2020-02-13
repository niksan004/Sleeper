import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import csv

movement = []

no_movement = 0
little_movement = 0
awake = 0
all_minutes = 0


class Graph:
    fig = plt.figure(figsize=(15, 10))
    time_title = []
    file_name = ''

    time = []
    movement = []
    sound_avg = []
    sound_max = []

    def __init__(self, file_name):
        self.file_name = file_name
        with open(file_name + '.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                self.time.append(pd.to_datetime(row[0]))
                self.time_title.append(row[0])
                movement.append(int(row[1]))
                self.sound_avg.append(int(row[2]))
                self.sound_max.append(int(row[3]))

    def entitle_fig(self):
        x = self.time_title[0].split()
        self.fig.suptitle(f'Графика на съня - {x[0]}', fontsize=40, fontweight='bold')

    def movement_graph(self):
        m = self.fig.add_subplot(313)
        m.plot(self.time, movement, label='Движение', color='tab:green')
        m.set_xlabel('Време', fontsize=30)
        m.set_ylabel('Движение(%)', fontsize=20)
        m.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=30))
        m.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    def sound_avg_graph(self):
        sa = self.fig.add_subplot(312)
        sa.plot(self.time, self.sound_avg, label='Среден шум', color='tab:blue')
        sa.set_ylabel('Среден шум', fontsize=20)
        sa.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=30))
        sa.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    def sound_max_graph(self):
        sm = self.fig.add_subplot(311)
        sm.plot(self.time, self.sound_max, label='Най-висок шум', color='tab:orange')
        sm.set_ylabel('Максимален шум', fontsize=20)
        sm.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=30))
        sm.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    def save(self):
        self.fig.savefig(self.file_name + '.png')


class Analysis:

    def movement_data(self):
        for perc in movement:
            if perc == 0:
                global no_movement
                no_movement += 1
            elif perc > 0 and perc < 20:
                global little_movement
                little_movement += 1
            else:
                global awake
                awake += 1

            global all_minutes
            all_minutes += 1

    def deep_sleep(self):
        return little_movement

    def REM(self):
        REM = 15
        additional = 0

        all_minutes_local = all_minutes - 70

        for c in range(int(all_minutes_local / 90)):
            REM += 15
            additional += 2

        return int(REM + additional)

    def light_sleep(self):
        ds = self.deep_sleep()
        REM = self.REM()
        return all_minutes - (ds + REM)

    def range(self):
        REM_lower = int((20 / 100) * all_minutes)
        REM_upper = int((25 / 100) * all_minutes)

        deep_lower = int((13 / 100) * all_minutes)
        deep_upper = int((23 / 100) * all_minutes)

        return [(REM_lower, REM_upper), (deep_lower, deep_upper)]


class Histogram(Analysis):
    fig = plt.figure(figsize=(10, 5))

    # stages = ()
    # y_pos = ()
    # time = []

    def subplot(self):
        stages = ('Буден', 'Лек сън', 'Дълбок сън', 'REM')
        y_pos = np.arange(len(stages))
        time = [awake, self.light_sleep(), self.deep_sleep(), self.REM()]

        ax = self.fig.add_subplot()

        ax.set_title('Фази на съня', fontsize=26, fontweight='bold')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(stages, fontsize=12)

        for i, v in enumerate(time):
            ax.text(2, i - .10, str(v) + ' min(your)', color='black')

        ax.tick_params(axis='x',
                       which='both',
                       bottom=False,
                       top=False,
                       labelbottom=False,
                       right=False,
                       left=False,
                       labelleft=False)

        stages_range = ('Буден', 'Лек сън', 'Дълбок сън', 'REM')
        y_pos_range = np.arange(len(stages_range))
        time_range = [0, 0, self.range()[1][0], self.range()[0][0]]

        ax_range = self.fig.add_subplot()

        ax_range.set_title('Фази на съня', fontsize=26, fontweight='bold')
        ax_range.set_yticks(y_pos_range)
        ax_range.set_yticklabels(stages_range, fontsize=12)

        for i, v in enumerate(time_range):
            if i > 1:
                ax_range.text(v, i - .10, str(v) + ' min(normal)', color='black')

        ax_range.tick_params(axis='x',
                             which='both',
                             bottom=False,
                             top=False,
                             labelbottom=False,
                             right=False,
                             left=False,
                             labelleft=False)

        ax.barh(y_pos, time, alpha=0.5, align='center', color='blue', label='Your sleep statistics')
        ax_range.barh(y_pos_range, time_range, alpha=0.5, align='center', color='purple',
                      label='Normal sleep statistics')

        ax.legend()
        self.fig.savefig('test2')


g = Graph('201912032156')
a = Analysis()
h = Histogram()

a.movement_data()
h.subplot()

g.entitle_fig()
g.movement_graph()
g.sound_avg_graph()
g.sound_max_graph()
g.save()