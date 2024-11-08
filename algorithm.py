from graph import Graph

def first_fit_adaptive(students):
    """
    Applies first-fit-coloring to a group of students to identify the schedules for each student.
    
    students is a list of lists --> each list represents a set of X classes that given student
    wants to take.
    """

    graph = Graph()

    for student in students:
        for i in range(len(student)):
            for j in range(i + 1, len(student)):
                graph.add_edge(student[i], student[j])

    coloring = dict([(className, -1) for className in graph.nodeSet])

    