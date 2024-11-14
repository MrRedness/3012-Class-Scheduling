import csv
import random

class Student:
    def __init__(self, name, course_enrollment):
        self.name = name
        self.course_enrollment = course_enrollment  # Boolean array for courses

def get_random(csv_filename, num):
    with open(csv_filename, mode='r') as file:
        names = next(csv.reader(file))
    return random.sample(names, num)

def gen_students():
    try:
        num_students = int(input("Enter the number of students: "))
        names = get_random("Inputs/Names.csv", num_students)
        print(names)
    except ValueError:
        print("Not enough student names available!")
        return []

    try:
        num_courses = int(input("Enter the number of courses: "))
        all_courses = get_random("Inputs/Courses.csv", num_courses)
        print(all_courses)
    except ValueError:
        print("Not enough course names available!")
        return []
  
    num_periods = int(input("Enter the number of class periods: "))
    students = []

    for name in names:
         # Initialize an array representing course enrollment
         # with the first `num_period` being true and the rest false
        course_enrollment = [True] * num_periods + [False] * (num_courses - num_periods)
        
        # Shuffle the array to randomly distribute True and False values
        random.shuffle(course_enrollment)
        
        # Create the student with the boolean array
        students.append(Student(name, course_enrollment))
        print(f"Student {students[-1].name} has enrollment {students[-1].course_enrollment}")
    
    return students, all_courses  # Return the list of courses as well for reference

def export_students_to_csv(students, all_courses):
    filename = "Generated/" + input("Enter the filename to save to: ")
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header with course names
        header = ["Name"] + all_courses
        writer.writerow(header)

        # Write each student's information
        for student in students:
            row = [student.name] + student.course_enrollment
            writer.writerow(row)
    
    print(f"Data has been saved to {filename}")

def csv_to_lst_of_lsts(filename):

    with open(filename, "r") as f:
        csv_data = f.read()

    rows = csv_data.strip().splitlines()
    reader = csv.reader(rows)

    # Extract headers (class names)
    headers = next(reader)[1:]

    # Convert each row to a list of classes the student is taking
    student_classes = []
    for row in reader:
        classes = [headers[i] for i, val in enumerate(row[1:]) if val == "True"]
        student_classes.append(classes)

    return student_classes

if __name__ == "__main__":
    # Generate students and export to CSV
    students, all_courses = gen_students()
    if students:  # Only if students were successfully generated
        export_students_to_csv(students, all_courses)
