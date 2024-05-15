import random
from variables import max_age_queen, num_bee, day_to_lay

class Bee:
    def __init__(self, number, weight, age):
        self.number = number
        self.weight = weight
        self.age = age
        self.max_age = random.randint(17, 22)

    def consume_honey(self, hive, lych=0):
        if lych == 0:
            honey_consumed = self.weight * 0.3
        else:
            honey_consumed = self.weight * 0.5
        if honey_consumed <= hive.honey_storage:
            honey_consumed = round(honey_consumed, 2)
            hive.honey_storage -= honey_consumed
            hive.consum_honey_all += honey_consumed
            return honey_consumed
        return None

    def check_dead(self, hive, type):
        types = {'worker':hive.workers, 'drone':hive.drones, 'cleaner':hive.cleaners}
        clas = types[type]

        self.age += 1
        if self.age > self.max_age:
            hive.count_old_dead+=1
            hive.dead_bees.append(self)
            clas.remove(self)
        else:
            honey = self.consume_honey(hive)
            if honey is not None:
                self.weight += honey
            else:
                self.weight -= self.weight/3
                if self.weight<1:
                    hive.dead_bees.append(self)
                    hive.count_hungry_dead+=1
                    clas.remove(self)

class WorkBee(Bee):
    def __init__(self, number, weight, age):
        super().__init__(number, weight, age)

    def collect_honey(self, hive):
        honey_collected = round(random.uniform(3, 8), 2)
        hive.honey_storage += honey_collected
        hive.collect_honney_all += honey_collected

class DroneBee(Bee):
    def __init__(self, number, weight, age):
        super().__init__(number, weight, age)

    def fertilize_eggs(self, hive, last_egg_id=0):
        self.capacity = random.randint(10, 20)
        self.capacity += int(hive.mean_productivity)
        count = 0
        count_eggs = len(hive.eggs)
        if count_eggs > 0:
            for i in range(last_egg_id, count_eggs):
                count += 1
                if count > self.capacity:
                    break
                if hive.eggs[i].flag:
                    continue
                hive.eggs[i].flag = True
                last_egg_id = i

        return last_egg_id

class Larva(Bee):
    def __init__(self, number, weight, age):
        super().__init__(number, weight, age)
        self.time_to_adult = random.randint(2, 5)
        self.time_to_transformation = random.randint(1, 3)
        self.flag = False

    def grow(self, hive):
        self.age += 1
        if self.age >= self.time_to_adult:
            honey = self.consume_honey(hive)
            if honey is not None:
                self.weight += honey
            else:
                hive.count_hungry_dead += 1
                hive.eggs.remove(self)
                return

            if self.age >= self.time_to_adult + self.time_to_transformation:
                global num_bee
                if random.random() < 0.3:
                    hive.drones.append(DroneBee(num_bee, self.weight, 1))
                else:
                    hive.workers.append(WorkBee(num_bee, self.weight, 1))
                hive.eggs.remove(self)

                num_bee += 1

class QueenBee(Bee):
    def __init__(self, number, weight, age):
        super().__init__(number, weight, age)
        self.flag_dead = False

    def lay_eggs(self, hive):
        count_eggs_produced = int(random.randint(2, 5) * hive.honey_storage / 20 / (1 + len(hive.dead_bees)))
        for i in range(count_eggs_produced):
            hive.eggs.append(Larva(0, 1, 1))