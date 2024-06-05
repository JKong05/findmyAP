import csv

# Implementation of AP course data
def load_courses(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        list_of_courses = [row[0] for row in csv_reader]
    return list_of_courses

list_of_courses = load_courses("ap_courses.csv")

# Lists needed for validation
list_of_schools = ["Vanderbilt University", "Harvard University", "University of Pennsylvania", "Duke University", "Princeton University", "Massachusetts Institute of Technology", "Harvard University", "Stanford University", "Yale University", "Brown University", "John Hopkins University", "Northwestern University", "Columbia University"]
modified_list = [i.replace("University of Pennsylvania", "UPENN").replace("Massachusetts Institute of Technology","MIT").replace(" College","").replace(" University","") for i in list_of_schools]

# Searching through casefolded normal list + modified list for specific cases
def search_lists(school):
    list_of_schools_casefold = [s.casefold() for s in list_of_schools]
    modified_list_casefold = [s.casefold() for s in modified_list]

    school = school.casefold().strip()
    if "university" in school or "college" in school:  # Check to see if school attr
        if school in list_of_schools_casefold:
            return list_of_schools[list_of_schools_casefold.index(school)]
        
    elif school not in list_of_schools_casefold:
        if school in modified_list_casefold:
            return modified_list[modified_list_casefold.index(school)]
        
    else:
        return None

# Searching through casefolded normal courses list
def search_courses(course):
    list_of_courses_casefold = [s.casefold() for s in list_of_courses]
    
    course = course.casefold().strip()
    if course in list_of_courses_casefold:
        return list_of_courses[list_of_courses_casefold.index(course)]
    return None

req_scores = {
    "Vanderbilt": {
        "AP Statistics": 5,
        "AP Human Geography": 5
    }
}