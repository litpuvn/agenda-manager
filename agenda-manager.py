import heapq
import itertools

class AgendaManager:
    pq = []  # list of entries arranged in a heap
    entry_finder = {}  # mapping of tasks to entries
    REMOVED = '<removed-task>'  # placeholder for a removed task
    counter = itertools.count()  # unique sequence count

    heap_rules = []

    def BuildQueue(self, rules):
        self.heap_rules = []
        for rule in rules:
            self.Insert(rule)

        self.Heapify()

    def Heapify(self):
        heapq.heapify(self.heap_rules)

    def Insert(self, new_rule):
        count = next(self.counter)
        priority = new_rule[1]
        rule = new_rule[0]
        entry = [priority, count, rule]
        heapq.heappush(self.heap_rules, entry)

    def Delete(self):
        print("delete a rule")



    def Run(self, rules):
        self.BuildQueue(rules)
        print(self.heap_rules)


    def _add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self._remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.heap_rules, entry)

    def _remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def _pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.heap_rules:
            priority, count, task = heapq.heappop(self.heap_rules)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

my_rules = [('arule', 12), ('brule', 21), ('crule', 70), ('drule', 25), ('erule', 10)]

print(my_rules)

AgendaManager().Run(my_rules)