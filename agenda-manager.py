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

    def HeapSort(self):
        sorted_list = []
        heap_size = len(self.my_priority_queue)
        for i in range(heap_size-1, 0, -1):
            my_item = self.my_priority_queue[0]
            sorted_list.append(self.my_priority_queue[0])
            self.my_priority_queue[0] = self.my_priority_queue[i]
            self.my_priority_queue.pop()
            self.Heapify(self.my_priority_queue, 0)

            print("Insert ", self._rule_value(my_item), "next-heap:", self.my_priority_queue)

        print("Done")

    def Insert(self, new_rule):
        heap_rules = self.my_priority_queue
        heap_rules.append(self._get_blank_rule())
        heap_size = len(heap_rules)
        i = heap_size - 1 # last element
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

    def GetQueue(self):
        return self.my_priority_queue

    def QueueLength(self):
        return len(self.my_priority_queue)

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
    rule_file = "input-min-heap2.txt"
else:
    rule_file = argvs[1]

start_time = timeit.default_timer()

agenda_manager = AgendaManager()
end_agenda_execution = False
counter = 0
try:
    with open(rule_file) as f:
        # read line by line to save memory. If there are more than 30 valid lines, the loop with exit
        for line in f:
            line = line.rstrip()
            # create input record from a line
            rule_priority_list = convert_line_to_tuple(line)

            if isinstance(rule_priority_list, bool):
                print("Ignore an incorrect rule line: ", line)
                continue

            counter += 1
            print("****** Cycle", counter, "******")
            # print("Current unsorted list:", rule_priority_list)

            if counter < 2:
                agenda_manager.BuildQueue(rule_priority_list)

                agenda_manager.HeapSort()

            else:
                print("Insert rules: ", rule_priority_list)
                for r in rule_priority_list:
                    agenda_manager.Insert(r)
                print("Agenda After Insert rules: ", agenda_manager.GetQueue())

            max_element = agenda_manager.ExtractMax()
            print("Extract max:", max_element)

            agenda_manager.Delete(max_element)

            if counter >= 30:
                end_agenda_execution = True
                break
    # keep extracting and deleting max rule if the agenda has not reached its 30th cycle.
    while agenda_manager.HasItem() and not end_agenda_execution:
        counter += 1
        print("****** Cycle", counter, "******")

        # remove largest priority item
        rule_largest_priority = agenda_manager.ExtractMax()
        print("Extract max:", rule_largest_priority)
        agenda_manager.Delete(rule_largest_priority)

        if counter >= 30:
            end_agenda_execution = True
            break

    print("***** Inference terminate after cycle", counter, " ***")
except IOError:
    print("The file does not exist. Please verify your input file")
except:
    print("Something went wrong. please review your program")

end_time = timeit.default_timer()

print("Problem size:", (counter + agenda_manager.QueueLength()), "Execution time:", (1000*(end_time - start_time)),"ms")