from graph import Graph
from dataGen import csv_to_lst_of_lsts

def first_fit_adaptive(students, max_periods):
    """
    Applies first-fit-coloring to a group of students to identify the schedules for each student.
    
    students is a list of lists --> each list represents a set of X classes that given student
    wants to take.
    max_periods is the maximum number of periods available for scheduling.
    """

    graph = Graph()

    for student in students:
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

            neighbor_colors = [coloring[neighbor] for neighbor in graph.get_neighbors(node) if coloring[neighbor] != -1]

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
                if frequencyMap[lowestColor] > val:
                    lowestColor = key
                elif frequencyMap[secondLowest] > val:
                    secondLowest = key

            if lowestColor != -1:
                coloring[node] = lowestColor
                if frequencyMap[lowestColor] >= 0:
                    duplicate = node + "_dup"
                    for neighbor in graph.get_neighbors(node):
                        if coloring[neighbor] == lowestColor:
                            graph.remove_edge(node, neighbor)
                            graph.add_edge(duplicate, neighbor)
                            # TODO do we need to add more connective edges here than just the lowest color?

                    coloring[duplicate] = -1
                    dupsCreated = True

        if dupsCreated:
            first_fit_coloring()

    first_fit_coloring()

    return graph, coloring

def apply_coloring_to_students(students, coloring):
    # TODO NEED THIS DONE!
    # Just a helper function that assigns each student to each coloring and returns
    # maybe a CSV with a reordered class size for each student? Also need to
    # interpret duplicates for this!
    pass

if __name__ == "__main__":
    students = csv_to_lst_of_lsts("Generated\\testSmall.csv")
    # print(students)
    graph, coloring = first_fit_adaptive(students, len(students[0]))
    print(coloring)
    print(graph.adjLst)
    Graph.visualize(graph, coloring)