def main():
    data = {}
    n = get_input()
    data = ap_list(n, data)

def get_input():
    while True:
        try:
            n = int(input("How many AP exams have you taken? "))
            if n == 0 or n > 38:
                print("Null")
                exit()
            if n < 0:
                print("Please enter a positive integer.")
                continue
            return n
        except ValueError:
            print("Please enter a valid integer.")
            continue
        except EOFError:
            exit()

def ap_list(n, data):
    course_list = ["AP Calculus AB", "AP Calculus BC", "AP Chemistry", "AP Latin", "AP Biology", "AP Research", "AP Seminar", "AP Psychology", "AP United States History", "AP Macroeconomics", "AP Microeconomics", "AP Human Geography"]
    for _ in range(n):
        while True:
            try: 
                course = input("Enter course: ")
                if course in course_list:
                    break
                else:
                    print("Course not found in the list. Please enter a valid course.")
            except Exception as e:
                print(f"An error occurred: {e}. Please try again.")
        while True:
            try:
                score = int(input("Enter score: "))
                if 0 < score < 6:
                    data[course] = score
                    break
                else:
                    print("Invalid score. Please enter a valid score.")
            except Exception as e:
                print(f"An error occurred: {e}. Please try again.")

    return data



if __name__ == "__main__":
    main()