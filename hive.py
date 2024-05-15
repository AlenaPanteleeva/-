from bee import WorkBee, DroneBee, Larva, QueenBee
from variables import max_age_queen, num_bee, day_to_lay
import random



class Hive:
    def __init__(self):
        self.queen = QueenBee(0,5, 10)
        self.honey_storage = 30
        self.dead_bees = []
        self.eggs = []
        self.workers = []
        self.cleaners = []
        self.drones = []
        self.last_egg_id = 0
        self.count_hungry_dead = 0
        self.count_old_dead = 0

    def added_cleaners(self):
        if (len(self.dead_bees) + self.count_heavy_dead_bee) > len(self.cleaners):
            for _ in range(len(self.dead_bees) - len(self.cleaners)):
                if self.workers:
                    cleaner = self.workers.pop(-1)
                    self.cleaners.append(cleaner)

    def clean_dead_bees(self):
        if self.dead_bees:
            self.added_cleaners()
            for dead_bee in self.dead_bees:
                for cleaner in self.cleaners:
                    if dead_bee.weight > cleaner.weight:
                        self.count_heavy_dead_bee += 1
                        break
            self.added_cleaners()
            self.count_heavy_dead_bee = 0
            if len(self.dead_bees) <= len(self.cleaners):
                self.dead_bees.clear()
            else:
                return

    def collect_honey(self):
        for worker in self.workers:
            worker.collect_honey(self)

    def check_dead_worker(self):
        for worker in self.workers:
            worker.check_dead(self, 'worker')

    def check_dead_drone(self):
        for drone in self.drones:
            drone.check_dead(self, 'drone')

    def check_dead_cleaner(self):
        for cleaner in self.cleaners:
            cleaner.check_dead(self, 'cleaner')

    def lay(self):
        if not (self.queen.flag_dead):
            self.queen.age += 1

            honey_q = self.queen.consume_honey(self)
            if honey_q is not None:
                self.queen.weight += honey_q
                global day_to_lay
                day_to_lay += 1
                if (day_to_lay) == 10:
                    self.queen.lay_eggs(self)
                    day_to_lay = 0
            else:
                self.queen.weight -= self.queen.weight / 5
                if self.queen.weight < 1:
                    self.queen.flag_dead = True
                    self.dead_bees.append(self.queen)
                    self.count_hungry_dead += 1

            if ((self.queen.age > max_age_queen) and (self.queen.flag_dead is False)):
                self.queen.flag_dead = True
                self.count_old_dead += 1

    def fertilize(self):
        if self.eggs:
            for i in range(len(self.drones)):
                if i == 0:
                    self.last_egg_id = self.drones[i].fertilize_eggs(self)
                else:
                    self.last_egg_id = self.drones[i].fertilize_eggs(self, self.last_egg_id)

    def transform_larv(self):
        for larva in self.eggs:
            if larva.flag:
                larva.grow(self)

    def update(self):
        self.consum_honey_all = 0
        self.collect_honney_all = 0

        self.mean_productivity = 2
        self.count_heavy_dead_bee = 0

        self.collect_honey()

        self.check_dead_worker()

        self.check_dead_drone()

        self.check_dead_cleaner()

        self.lay()

        yield len(self.dead_bees)

        self.clean_dead_bees()

        self.collect_honey()
        self.mean_productivity *= self.honey_storage / 100
        self.mean_productivity += random.randint(-5, 5)

        self.fertilize()

        self.transform_larv()

        self.honey_storage = round(self.honey_storage, 2)
        self.consum_honey_all = round(self.consum_honey_all, 2)

        self.collect_honney_all = round(self.collect_honney_all, 2)

        yield (len(self.eggs), len(self.drones), len(self.workers), len(self.cleaners), len(self.dead_bees),
               self.consum_honey_all, self.collect_honney_all, self.honey_storage)