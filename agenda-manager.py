import heapq
import itertools
import re
import timeit
import sys


class AgendaManager:

    my_priority_queue = []

    def _left(self, parent_index):
        return 2*parent_index + 1

    def _right(self, parent_index):
        return 2*parent_index + 2

    def _parent(self, current_index):
        return (current_index - 1) // 2

    def _heap_rule_value(self, rules, index):
        rule = rules[index]

        return self._rule_value(rule)

    def _rule_value(self, rule):

        return rule[1]

    def _get_blank_rule(self):
        return ['rule', -1]

    def _get_root_index(self):
        return 0

    # def _build_heap(self, rules):
    #     # self.heap_rules = []
    #     if len(rules) < 1:
    #         return rules
    #
    #     parent_of_last_leaf_index = self._parent(len(rules) - 1)
    #
    #     # include index zero
    #     for i in range(parent_of_last_leaf_index, -1, -1):
    #         print("heapify for", i)
    #         self.Heapify(rules, i)
    #
    #     print("BuildQueue:", rules)

    def BuildQueue(self, rules):

        print("BUILD QUEUE")
        if len(rules) < 1:
            print("Nothing to build")
            return

        print("Build queue: ", rules)

        self.my_priority_queue.extend(rules)
        last_leaf_index = len(self.my_priority_queue) - 1
        parent_of_last_leaf_index = self._parent(last_leaf_index)

        for i in range(parent_of_last_leaf_index, -1, -1):
            # print("heapify for", i)
            self.Heapify(self.my_priority_queue, i)

        print("Agenda after build queue:", self.my_priority_queue)


    def Heapify(self, rules, index):

        # print("Heapify at", index, rules)
        left_index = self._left(index)
        right_index = self._right(index)

        heap_size = len(rules)

        if left_index < heap_size and self._heap_rule_value(rules, left_index) > self._heap_rule_value(rules, index):
            largest = left_index
        else:
            largest = index

        if right_index < heap_size and self._heap_rule_value(rules, right_index) > self._heap_rule_value(rules, largest):
            largest = right_index

        # print("Largest index is:", largest, "; heapify index:", index)

        if largest != index:
            tmp = rules[index]
            rules[index] = rules[largest]
            rules[largest] = tmp
            self.Heapify(rules, largest)

    def Insert(self, heap_rules, new_rule):
        heap_rules.append(self._get_blank_rule())
        hea_size = len(heap_rules)
        i = hea_size
        parent_of_i = self._parent(i)

        root_index = self._get_root_index()
        inserted_priority = self._rule_value(new_rule)

        while i > root_index and self._heap_rule_value(heap_rules, parent_of_i) < inserted_priority:
            heap_rules[i] = heap_rules[parent_of_i]
            i = parent_of_i
            parent_of_i = self._parent(i)

        heap_rules[i] = new_rule

    def Delete(self, rule):
        # print("EXTRACT AND DELETE MAX", self.my_priority_queue)
        heap_rules = self.my_priority_queue
        heap_size = len(heap_rules)
        if heap_size < 1:
            return KeyError("Heap queue is empty")

        max_rule = self.ExtractMax()
        if self._rule_value(rule) != self._rule_value(max_rule):
            print("Rule", rule, "is not max rule to be deleted")
            return
        root_index = self._get_root_index()
        heap_rules[root_index] = heap_rules[heap_size-1]
        del heap_rules[-1]
        self.Heapify(heap_rules, root_index)

        print("Agenda after delete max:", self.my_priority_queue)


    def ExtractMax(self):
        heap_rules = self.my_priority_queue
        heap_size = len(heap_rules)
        if heap_size < 1:
            return KeyError("Heap queue is empty")

        root_index = self._get_root_index()
        max_value = heap_rules[root_index]

        return max_value

    def HasItem(self):
        return len(self.my_priority_queue) > 0

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
        if index % 2 == 1:
            if not item.isnumeric():
                return False
            item = int(item)

        entry.append(item)

    # append last item
    if len(entry) > 0:
        my_tuples.append(entry)

    if len(my_tuples) < 1:
        return False

    return my_tuples


argvs = sys.argv
if(len(argvs) < 2):
    print("The program accepts only one argument which is a rule file.")
    exit(1)

rule_file = argvs[1]
if len(argvs) > 2:
    log_file = argvs[2]

agenda_manager = AgendaManager()

counter = 0
try:
    with open(rule_file) as f:
        for line in f:
            line = line.rstrip()
            rule_priority_list = convert_line_to_tuple(line)

            if isinstance(rule_priority_list, bool):
                print("Ignore an incorrect rule line: ", line)
                continue

            counter += 1
            print("****** Cycle", counter, "******")
            # print("Current unsorted list:", rule_priority_list)

            agenda_manager.BuildQueue(rule_priority_list)
            max_element = agenda_manager.ExtractMax()
            print("Extract max:", max_element)

            agenda_manager.Delete(max_element)

    while agenda_manager.HasItem():
        counter += 1
        print("****** Cycle", counter, "******")

        # remove largest priority item
        rule_largest_priority = agenda_manager.ExtractMax()
        print("Extract max:", rule_largest_priority)
        agenda_manager.Delete(rule_largest_priority)

    print("***** Inference terminate after cycle", counter, " ***")
except IOError:
    print("The file does not exist. Please verify your input file")
except:
    print("Something went wrong. please review your program")