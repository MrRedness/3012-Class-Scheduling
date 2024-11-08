from graph import Graph

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
        for node in graph.nodeSet:
            neighbor_colors = {coloring[neighbor] for neighbor in graph.get_neighbors(node) if coloring[neighbor] != -1}

            for color in range(max_periods):
                if color not in neighbor_colors:
                    coloring[node] = color
                    break

        handle_vertex_duplication()

    def handle_vertex_duplication():
        for node in graph.nodeSet:
            if coloring[node] == -1:
                new_node = f"{node}_duplicate"
                graph.add_edge(new_node, node)
                first_fit_coloring()

    first_fit_coloring()

    return coloring

