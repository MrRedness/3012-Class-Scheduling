from graph import Graph
from data_gen import csv_to_student_dict
from copy import deepcopy

DEBUG_MODE = False

def _generate_dup_list(iteration, name_prefix):
    # Initialize the result list
    result = []
    
    # Reconstruct the parts incrementally
    for i in range(1, iteration):
        result.append(name_prefix + '_' + str(i))
    
    return result

def first_fit_adaptive(student_classes, initNode):
    """
    Applies first-fit-coloring to a group of students to identify the schedules for each student.

    student_classes is a list of lists --> each list represents a set of X classes that given student
    wants to take.
    """

    graph = Graph()

    max_periods = len(student_classes[0])

    for student in student_classes:
        for i in range(len(student)):
            for j in range(i + 1, len(student)):
                graph.add_edge(student[i], student[j])

    coloring = dict([(className, -1) for className in graph.nodeSet])

    def first_fit_coloring(initNode):
        iterNodeSet = list(graph.nodeSet)
        if initNode:
            try:
                iterNodeSet.remove(initNode)
                iterNodeSet.insert(0, initNode)
            except:
                print(initNode in list(graph.nodeSet))
                print(initNode)
        dupsCreated = False
        for node in iterNodeSet:
            if coloring[node] != -1:
                continue

            neighbor_colors = [coloring[neighbor] for neighbor in graph.get_neighbors(
                node) if coloring[neighbor] != -1]

            frequencyMap = dict([(x, 0) for x in range(-1, max_periods)])

            # Count frequencies
            for item in neighbor_colors:
                frequencyMap[item] += 1

            # TODO initial algorithm done?
            # Can we add a thing here that doesn't automatically assign first period
            # to the duplicate colors, but instead assigns a combination of the best
            # color for the job that also happens to be the fewest already alloted?
            lowestColor = 0
            secondLowest = 1
            for key, val in frequencyMap.items():
                if key == -1:
                    continue
                # lowestColor is set to the color with the minumum frequency
                if frequencyMap[lowestColor] > val:
                    secondLowest = lowestColor
                    lowestColor = key
                # secondLowest is set to the color with the second minium frequency
                elif frequencyMap[secondLowest] > val:
                    secondLowest = key

            if lowestColor == -1:
                lowestColor = secondLowest
            if (DEBUG_MODE):
                print(f"Coloring node {node} with color {lowestColor}")
                print(frequencyMap)
                print(
                    f"Frequency of lowest color {lowestColor} is {frequencyMap[lowestColor]}")
                print(
                    f"Frequency of second lowest color {secondLowest} is {frequencyMap[secondLowest]}")
            coloring[node] = lowestColor
            if frequencyMap[lowestColor] > 0:
                if (DEBUG_MODE):
                    print(f"Creating dupe for {node}")

                index = node.rfind('_')
                new_num = int(node[(index + 1):]) + 1
                prefix = node[:index]
                duplicate = node[:index] + "_" + str(new_num)

                all_dups_so_far = _generate_dup_list(new_num, prefix)

                if len(all_dups_so_far) >= len(student_classes[0]):
                    return None, None, []

                for old_dup in all_dups_so_far:

                    for neighbor in graph.get_neighbors(old_dup):
                        if coloring[neighbor] == coloring[old_dup]:
                            if DEBUG_MODE:
                                print(f"ATTACHING DUP OF {old_dup} TO {neighbor}")
                            graph.remove_edge(old_dup, neighbor)
                            graph.add_edge(duplicate, neighbor)

                            # TODO LIST FIGURING THIS OUT!!!
                            for class_list in student_classes:
                                if (class_list.count(old_dup) > 0 and class_list.count(neighbor) > 0):
                                    if DEBUG_MODE:
                                        print(class_list)
                                    class_list.remove(old_dup)
                                    for student_class in class_list:
                                        graph.add_edge(duplicate, student_class)
                                    class_list.append(duplicate)
                                    if DEBUG_MODE:
                                        print(class_list)
                    coloring[duplicate] = -1
                    dupsCreated = True
            if (DEBUG_MODE):
                pass
                # vis = input()
                # if vis:
                #     Graph.visualize(graph, coloring)

        if dupsCreated:
            if (DEBUG_MODE):
                print("Recurse Recurse")
            first_fit_coloring(False)

    first_fit_coloring(initNode)

    return graph, coloring, student_classes

from time import sleep
def reorder_student_list(student_classes, coloring):
    new_student_classes = []
    for class_list in student_classes:
        # print(class_list)
        copy = class_list.copy()
        class_list = ["" for _ in class_list]
        for colored_class, color in coloring.items():
            # print(f"Colored class {colored_class} with color {color}")
            if copy.count(colored_class) > 0:
                # print("Found in copy")
                if (class_list[color] != ""):
                    # pass
                    if DEBUG_MODE:
                        print(f"ERROR! Class {colored_class} has color {color} but class_list already has that color used by {class_list[color]}")
                    # sleep(5)
                class_list[color] = colored_class
            
        new_student_classes.append(class_list)

    return new_student_classes

def add_suffix_to_classes(student_classes):
    for student in student_classes:
        for i in range(len(student)):
            student[i] += "_1"

if __name__ == "__main__":
    student_dict = csv_to_student_dict("Generated\\testSmall0.csv")

    # import pandas as pd
    # print(pd.DataFrame.from_dict(student_dict).to_csv("test.csv"))
    # exit()
    student_classes = list(student_dict.values())
    add_suffix_to_classes(student_classes)
    all_classes = list(set(sum(student_classes, [])))

    print(f"Finding a working schedule across {len(all_classes)} courses for {len(student_classes)} students with {len(student_classes[0])} periods each!")

    bestGraph = None
    bestColoring = None
    workingInitNode = None
    bestSchedules = None
    bestSPC = None

    for initNode in all_classes:
        try:
            graph, coloring, dup_studentClasses = first_fit_adaptive(deepcopy(student_classes), initNode)

            if not graph:
                raise RecursionError("CONFLICTING CONSTRAINTS IN GREEDY ALGORITHM!")

            all_class_periods = list(set(sum(dup_studentClasses, [])))

            ordered_schedules = reorder_student_list(dup_studentClasses, coloring)
            students_per_class = dict([(x, 0) for x in all_class_periods])

            if DEBUG_MODE:
                Graph.visualize(graph, coloring)

            for schedule in ordered_schedules:
                # print(schedule)
                for period in schedule:
                    students_per_class[period] += 1

            if not workingInitNode or (len(coloring) < len(bestColoring)):
                workingInitNode = initNode
                bestGraph = graph
                bestColoring = coloring
                bestSchedules = ordered_schedules
                bestSPC = students_per_class
            print(f"Worked with initial node, {initNode}, creating {len(coloring)} distinct class-period options")
        except RecursionError:
            print(f"RECURSION: Did not work with initial node, {initNode}")
            graph = None
            coloring = None
        except KeyError:
            print(f"MISASSIGNMENT: Did not work with initial node, {initNode}")
            graph = None
            coloring = None

    if not workingInitNode:
        print("No suitable start node found with current logic!")
        exit()

    print("-" * 30)

    print("Found a working solution stemming from initial node: ", workingInitNode)
    print("Total number of created period slots:", len(bestColoring))
    # print(coloring)
    # print(graph.adjLst)

    print("")

    print(bestSPC.values())

    Graph.visualize(bestGraph, bestColoring)
