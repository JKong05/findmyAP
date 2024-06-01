from schools import search_lists

class User():
    def __init__(self, school, ap_scores):
        self.school = school

def main():
    user = user_input()
    user = user_scores()


def user_input():
    while True:
        try:
            school = input("What school do you want to look at? ")
            school = search_lists(school=school)

            if school == None:
                print("Not a valid school.")
                continue
            else:
                print("Looking at " + school)
                break
        except ValueError:
            print("Null. Please try again")
            continue
        except EOFError:
            exit()
    user = User(school)
    return user

def user_scores():
    data = {}
    num_exams = get_num_exams()
    while True:
        try:
            for exam in range(num_exams):
                course = input("Enter course: ")
                course = search_courses(course=course)
        except:
            ...
def get_num_exams():
    while True:
        num = int(input("How many AP exams have you taken? "))
        if 0 < num < 39:
            return num
        else:
            print("Invalid input. Please enter a valid integer.")
            continue


if __name__ == "__main__":
    main()