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
    for exam in range(n):
        course = input("Enter course: ")
        score = input("Enter score received: ")
        data[course] = score

    return data

if __name__ == "__main__":
    main()