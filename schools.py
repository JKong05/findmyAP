list_of_schools = ["Vanderbilt University", "Harvard University", "University of Pennsylvania", "Duke University", "Princeton University", "Massachusetts Institute of Technology", "Harvard University", "Stanford University", "Yale University", "Brown University", "John Hopkins University", "Northwestern University", "Columbia University"]
modified_list = [i.replace("University of Pennsylvania", "UPENN").replace("Massachusetts Institute of Technology","MIT").replace(" College","").replace(" University","") for i in list_of_schools]
list_of_courses = [
    "AP African American Studies", 
    "AP Art & Design: 2D", 
    "AP Art & Design: 3D",
    "AP Art & Design: Drawing",
    "AP Art History",
    "AP Biology",
    "AP Calculus AB",
    "AP Calculus BC",
    "AP Chemistry",
    "AP Chinese",
    "AP Comparative Government",
    "AP Computer Science A",
    "AP Computer Science Principles",
    "AP English Language",
    "AP English Literature",
    "AP Environmental Science",
    "AP European History",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    ""]


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

def search_courses(course):
