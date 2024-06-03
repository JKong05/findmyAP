from schools import search_lists, search_courses

# User object
class User():
    def __init__(self, school, ap_data):
        self.school = school
        self.ap_data = ap_data

# Housing the attributes for user input
def main():
    user = user_input()

# Obtain school information and call to get information about how many courses / exams student took,
# which course they took (cross-checking with AP course catalog), and gather information about
# what score the student received on this exam. 
def user_input():
    while True:
        try:
            school = input("What school do you want to look at? ")
            school = search_lists(school=school)

            if school is None:
                print("Not a valid school.")
                continue
            else:
                print("Looking at " + school)
                break
        except ValueError:
            print("Null. Please try again.")
            continue
        except EOFError:
            exit()
    ap_data = user_scores()
    user = User(school, ap_data)
    return user

# Assisting user_input() function --> dictionary for ap_data
def user_scores():
    data = {}
    count = 1
    for exam in range(get_num_exams()):
        print("\n[Exam " + str(count) + "]")
        while True:
            try:
                course = input("Enter course: ")
                course = search_courses(course=course)

                if course is None:
                    print("Did you enter the course in as it appears on Collegeboard? Please try again.")
                    continue
                
                data = helper_scores(data, course)
                break
            except ValueError:
                print("Null. Please try again.")
                continue
            except EOFError:
                exit()
        count += 1
    return data

# Helper function for getting the number of exams student took. 
def get_num_exams():
    while True:
        try:
            num = int(input("How many AP exams have you taken? "))
            if 0 < num < 39:
                return num
            else:
                print("Invalid input. Please enter a valid integer.")
                continue
        except ValueError:
            print("Null. Please try again.")
            continue
        except EOFError:
            exit()

def helper_scores(data, course):
    while True:
        try:
            score = int(input("Enter score received for this course: "))
            if 0 < score <= 5:
                data[course] = score
                return data
            else:
                print("Invalid input. An official AP score will be between 1 and 5.")
                continue
        except ValueError:
                    print("Null. Please try again.")
                    continue
        except EOFError:
                     exit()


if __name__ == "__main__":
    main()