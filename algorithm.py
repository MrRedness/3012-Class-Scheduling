from graph import Graph
from data_gen import csv_to_classes_dict, csv_to_student_dict

DEBUG_MODE = False

def first_fit_adaptive(student_classes):
    """
    Applies first-fit-coloring to a group of students to identify the schedules for each student.

    student_classes is a list of lists --> each list represents a set of X classes that given student
    wants to take.
    """

    graph = Graph()

    max_periods = len(student_classes[0])
    print(f"Max num of periods: {max_periods}")

    for student in student_classes:
        for i in range(len(student)):
            for j in range(i + 1, len(student)):
                graph.add_edge(student[i], student[j])

    coloring = dict([(className, -1) for className in graph.nodeSet])

    def first_fit_coloring():
        iterNodeSet = list(graph.nodeSet)
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
            secondLowest = 0
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
                duplicate = node + "_dup"

                for neighbor in graph.get_neighbors(node):
                    if coloring[neighbor] == lowestColor:
                        graph.remove_edge(node, neighbor)
                        graph.add_edge(duplicate, neighbor)

                        for class_list in student_classes:
                            if (class_list.count(node) > 0 and class_list.count(neighbor) > 0):
                                class_list.remove(node)
                                for student_class in class_list:
                                    graph.add_edge(duplicate, student_class)
                                class_list.append(duplicate)

                        # TODO do we need to add more connective edges here than just the lowest color?

                coloring[duplicate] = -1
                dupsCreated = True
            if (DEBUG_MODE):
                Graph.visualize(graph, coloring)

        if dupsCreated:
            if (DEBUG_MODE):
                print("Recurse Recurse")
            first_fit_coloring()

    first_fit_coloring()

    return graph, coloring

from time import sleep
def reorder_student_list(student_classes, coloring):
    for class_list in student_classes:
        print(class_list)
        copy = class_list.copy()
        class_list = ["" for _ in class_list]
        for colored_class, color in coloring.items():
            # print(f"Colored class {colored_class} with color {color}")
            if copy.count(colored_class) > 0:
                # print("Found in copy")
                if (class_list[color] != ""):
                    print(f"ERROR! Class {colored_class} has color {color} but class_list already has that color used by {class_list[color]}")
                    # sleep(5)
                class_list[color] = colored_class
            
        print(class_list)
        # sleep(2)
        print("\n\n")

if __name__ == "__main__":
    student_dict = csv_to_student_dict("Generated\\testSmall2.csv")

    print(student_dict)
    
    student_classes = list(student_dict.values())

    graph, coloring = first_fit_adaptive(student_classes)

    print("\n\n")

    print(coloring)
    # print(graph.adjLst)

    print("\n\n")

    reorder_student_list(student_classes, coloring)
    
    Graph.visualize(graph, coloring)
