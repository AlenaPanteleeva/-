import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from hive import Hive
from bee import WorkBee, DroneBee, Larva, QueenBee
from bee import num_bee

class HiveSimulationApp:
    def __init__(self, master):
        self.master = master
        self.days_passed = []  # Массив для хранения количества пройденных дней
        self.honey_consumed_all = []  # Массив для хранения количества потребленного меда
        self.honey_collect_all = []
        self.flag_dead_queen = False
        master.title("Улей")

        self.create_hive()


        self.label_lichinka = tk.Label(master, text="Количество личинок:")
        self.label_truten = tk.Label(master, text="Количество трутней:")
        self.label_worker1 = tk.Label(master, text="Количество рабочих пчел-добытчиков:")
        self.label_worker2 = tk.Label(master, text="Количество рабочих пчел-уборщиков:")
        self.label_dead = tk.Label(master, text="Количество мертвых пчел:")
        self.label_consumption = tk.Label(master, text="Потребление меда:")
        self.label_production = tk.Label(master, text="Производство меда:")
        self.label_storage = tk.Label(master, text="Всего меда:")

        self.label_lichinka.pack()
        self.label_truten.pack()
        self.label_worker1.pack()
        self.label_worker2.pack()
        self.label_dead.pack()
        self.label_consumption.pack()
        self.label_production.pack()
        self.label_storage.pack()

        self.message_label = tk.Label(master, text="Матка жива")
        self.message_label.pack()

        self.pause_button = tk.Button(master, text='Pause', command=self.try_pause)
        self.pause_button.pack()

        self.is_paused = False

        self.update_labels()

        master.bind("<space>", self.try_pause)

    def update_labels(self):
        if not self.is_paused:
            result = self.hive.update()

            count_dead = next(result)

            total_dead = count_dead

            count_dead_larva = sum(isinstance(obj, Larva) for obj in self.hive.dead_bees)
            count_dead_drone = sum(isinstance(obj, DroneBee) for obj in self.hive.dead_bees)
            count_dead_worker = sum(isinstance(obj, WorkBee) for obj in self.hive.dead_bees)

            if total_dead > 0:
                percent_dead_drone = (count_dead_drone / total_dead) * 100
                percent_dead_worker = (count_dead_worker / total_dead) * 100
            else:
                percent_dead_drone = 0
                percent_dead_worker = 0

            count_cleaners = len(self.hive.cleaners)

            if count_dead < count_cleaners:
                count_remaining_cleaners = count_cleaners - count_dead
            else:
                count_remaining_cleaners = 0

            self.label_dead.config(text=f"Количество мертвых пчел: {count_dead} \n "
                                       f"Процент умерших трутней: {percent_dead_drone:.2f}%\n"
                                       f"Процент умерших рабочих пчел: {percent_dead_worker:.2f}% \n"
                                   f"Количество простаивающих пчел-уборщиков: {count_remaining_cleaners}")

            results = next(result)
            self.label_lichinka.config(text=f"Количество личинок: {results[0]}")
            self.label_truten.config(text=f"Количество трутней: {results[1]}")
            self.label_worker1.config(text=f"Количество рабочих пчел-добытчиков: {results[2]}")
            self.label_worker2.config(text=f"Количество рабочих пчел-уборщиков: {results[3]}")
            self.label_consumption.config(text=f"Потребление меда: {results[5]}")
            self.label_production.config(text=f"Производство меда: {results[6]}")
            self.label_storage.config(text=f"Всего меда: {results[7]}")

            if self.hive.queen.flag_dead and not self.flag_dead_queen:
                self.message_label.config(text="Матка умерла")
            # Добавляем данные в массивы
            self.days_passed.append(len(self.days_passed) + 1)
            self.honey_consumed_all.append(results[5])
            self.honey_collect_all.append(results[6])

        self.master.after(500, self.update_labels)

    def create_hive(self):
        self.hive = Hive()

        global num_bee
        for i in range(5):
            w = random.randint(1, 3)
            age = 1
            self.hive.workers.append(WorkBee(num_bee, w, age))
            num_bee += 1

        for i in range(5):
            w = random.randint(1, 3)
            age = 1
            self.hive.drones.append(DroneBee(num_bee, w, age))
            num_bee += 1

    def try_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.configure(text="Start")
            messagebox.showinfo(
                "Информация о погибших пчелах",
                f"Погибших от голода: {self.hive.count_hungry_dead}\n"
                f"Погибших от старости: {self.hive.count_old_dead}"
            )
            self.create_chart(self.days_passed, self.honey_consumed_all,self.honey_collect_all)
        else:
            self.pause_button.configure(text="Pause")

    def create_chart(self,days,honey_consumption,collect):

        chart_window = tk.Toplevel(self.master)
        chart_window.title("Диаграмма потребления меда пчелами")

        frame = ttk.Frame(chart_window)
        frame.pack(fill=tk.BOTH, expand=True)

        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.bar([day - 0.2 for day in days], honey_consumption, width=0.4, color='skyblue', align='center',
               label='Потребление')

        ax.bar([day + 0.2 for day in days], collect, width=0.4, color='orange', align='center', label='Производство')

        ax.set_title('Потребление и производство меда пчелами каждый день')
        ax.set_xlabel('День')
        ax.set_ylabel('Количество меда')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()

        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        chart_window.mainloop()