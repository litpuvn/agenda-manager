import heapq
import itertools
import ast
import re

class AgendaManager:
    # pq = []  # list of entries arranged in a heap
    # entry_finder = {}  # mapping of tasks to entries
    # REMOVED = '<removed-task>'  # placeholder for a removed task

    counter = itertools.count()  # unique sequence count
    heap_rules = []

    def BuildQueue(self, rules):
        # self.heap_rules = []
        for rule in rules:
            entry = self._create_entry(rule)
            self.heap_rules.append(entry)

        self.Heapify()

    def Heapify(self):
        heapq.heapify(self.heap_rules)

    def Insert(self, new_rule):
        entry = self._create_entry(new_rule)

        heapq.heappush(self.heap_rules, entry)

    def Delete(self):
        print("delete a rule")

    def ExtractMax(self):
        if len(self.heap_rules) < 1:
            return KeyError("Heap queue is empty")

        max = heapq.nlargest(1, self.heap_rules)
        max = max[0]

        return (max[2], max[0])

    def Run(self, rules):
        self.BuildQueue(rules)
        print(self.heap_rules)

        max_item = self.ExtractMax()
        print(max_item)

    def Print(self):
        print(self.heap_rules)

    def _create_entry(self, rule):
        count = next(self.counter)
        priority = rule[1]
        rule = rule[0]

        return [priority, count, rule]

    #
    #
    # def _add_task(self, task, priority=0):
    #     'Add a new task or update the priority of an existing task'
    #     if task in self.entry_finder:
    #         self._remove_task(task)
    #     count = next(self.counter)
    #     entry = [priority, count, task]
    #     self.entry_finder[task] = entry
    #     heapq.heappush(self.heap_rules, entry)
    #
    # def _remove_task(self, task):
    #     'Mark an existing task as REMOVED.  Raise KeyError if not found.'
    #     entry = self.entry_finder.pop(task)
    #     entry[-1] = self.REMOVED
    #
    # def _pop_task(self):
    #     'Remove and return the lowest priority task. Raise KeyError if empty.'
    #     while self.heap_rules:
    #         priority, count, task = heapq.heappop(self.heap_rules)
    #         if task is not self.REMOVED:
    #             del self.entry_finder[task]
    #             return task
    #     raise KeyError('pop from an empty priority queue')

my_rules = [('arule', 12), ('brule', 21), ('crule', 70), ('drule', 25), ('erule', 10)]

# return an array of rules
def convert_line_to_tuple(line):
    if len(line) < 1:
        return False

    line = line.rstrip()
    tmp = re.split(",", line)

    if len(tmp) % 2 != 0:
        return False

    my_tuple = []
    entry = []
    for index, item in enumerate(tmp):
        item = item.strip()
        item = item.strip('(')
        item = item.strip(')')
        item = item.strip()
        if len(item) < 1:
            continue

        if index % 2 == 0:
            if len(entry) > 0:
                my_tuple.append(entry)
                entry = []
        if index % 2 == 1 and not item.isnumeric():
            return False

        entry.append(item)

    # append last item
    if len(entry) > 0:
        my_tuple.append(entry)

    return my_tuple




agenda_manager = AgendaManager()

with open('input.txt') as f:
    for line in f:
        line = line.rstrip()
        tuple_list = convert_line_to_tuple(line)
        if isinstance(tuple_list, bool):
            print("Ignore an incorrect rule line: ", line)
            continue

        agenda_manager.BuildQueue(tuple_list)
        agenda_manager.Print()




# AgendaManager().Run(my_rules)