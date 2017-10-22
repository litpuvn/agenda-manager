import heapq
import itertools
import re

class AgendaManager:

    def _left(self, parent_index):
        return 2*parent_index + 1

    def _right(self, parent_index):
        return 2*parent_index + 2

    def _parent(self, current_index):
        return (current_index - 1) // 2

    def _rule_value(self, rules, index):
        rule = rules[index]
        return rule[1]

    def BuildQueue(self, rules):
        # self.heap_rules = []
        if len(rules) < 1:
            return rules

        parent_of_last_leaf_index = self._parent(len(rules) - 1)

        # include index zero
        for i in range(parent_of_last_leaf_index, -1, -1):
            print("heapify for", i)
            self.Heapify(rules, i)

        print("BuildQueue:", rules)

    def Heapify(self, rules, index):

        left_index = self._left(index)
        right_index = self._right(index)

        heap_size = len(rules)

        if left_index < heap_size and self._rule_value(rules, left_index) > self._rule_value(rules, index):
            largest = left_index
        else:
            largest = index

        if right_index < heap_size and self._rule_value(rules, right_index) > self._rule_value(rules, largest):
            largest = right_index

        if largest != index:
            tmp = rules[index]
            rules[index] = rules[largest]
            rules[largest] = tmp
            self.Heapify(rules, largest)

    def Insert(self, new_rule):
        entry = self._create_entry(new_rule)

        heapq.heappush(self.heap_rules, entry)

    def Delete(self, rule):
        print("delete a rule", rule)

    def ExtractMax(self):
        if len(self.heap_rules) < 1:
            return KeyError("Heap queue is empty")

        max = heapq.nlargest(1, self.heap_rules)
        max = max[0]
        found = [max[2], max[0]]
        print("Extract max: ", found)
        return found

    def HasItem(self):
        return len(self.heap_rules) > 0

# return an array of rules
def convert_line_to_tuple(line):
    if len(line) < 1:
        return False

    line = line.rstrip()
    tmp = re.split(",", line)

    if len(tmp) % 2 != 0:
        return False

    my_tuples = []
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
                my_tuples.append(entry)
                entry = []
        if index % 2 == 1 and not item.isnumeric():
            return False

        entry.append(item)

    # append last item
    if len(entry) > 0:
        my_tuples.append(entry)

    if len(my_tuples) < 1:
        return False

    return my_tuples


agenda_manager = AgendaManager()

counter = 0
with open('input.txt') as f:
    for line in f:
        line = line.rstrip()
        rule_priority_list = convert_line_to_tuple(line)

        if isinstance(rule_priority_list, bool):
            print("Ignore an incorrect rule line: ", line)
            continue

        counter += 1
        print("Cycle", counter)
        print("Current unsorted list:", rule_priority_list)
        agenda_manager.BuildQueue(rule_priority_list)

        rule_largest_priority = agenda_manager.ExtractMax()
        agenda_manager.Delete(rule_largest_priority)

while agenda_manager.HasItem():
    counter += 1
    print("Cycle", counter)

    # remove largest priority item
    rule_largest_priority = agenda_manager.ExtractMax()
    agenda_manager.Delete(rule_largest_priority)

