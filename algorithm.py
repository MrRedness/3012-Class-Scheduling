from graph import Graph
import csv
from collections import Counter

def csv_to_lst_of_lsts(filename):
    
    with open(filename, "r") as f:
        csv_data = f.read()

    reader = csv.reader(csv_data.strip().split('\n'))
    header = next(reader)

    # Step 2: Extract course names from the header (excluding Name and Course Bitmap)
    course_names = header[2:]

    # Step 3: Process each row to create the list of classes each student is enrolled in
    students_classes = []

    for row in reader:
        course_bitmap = row[1]  # The bitmap of courses
        enrolled_courses = []
        
        for i, bit in enumerate(course_bitmap):
            if bit == '1':  # If the bit is 1, the student is enrolled in the course
                enrolled_courses.append(course_names[i])
        
        students_classes.append(enrolled_courses)

    return students_classes

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
        for node in iterNodeSet:
            neighbor_colors = [coloring[neighbor] for neighbor in graph.get_neighbors(node) if coloring[neighbor] != -1]

            frequencyMap = dict([(x, 0) for x in range(-1, max_periods)])

            # Count frequencies
            for item in neighbor_colors:
                frequencyMap[item] += 1

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
                    graph.add_node(duplicate)
                    for neighbor in graph.get_neighbors(node):
                        if coloring[neighbor] == lowestColor:
                            graph.remove_edge(node, neighbor)
                            graph.add_edge(duplicate, neighbor)
                    coloring[duplicate] = secondLowest
                    # TODO HOW TO ASSIGN THE COLOR OF THE DUPLICATE!

    first_fit_coloring()

    return coloring

if __name__ == "__main__":
    students = csv_to_lst_of_lsts("Generated\\test2.csv")
    print(first_fit_adaptive(students, 7))