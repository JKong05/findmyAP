$(document).ready(function() {
    // This section of code is accounting when you click on the input field --> shows entire list of autocomplete
    let autocompleteSelected = false;
    
    $('#searchBtn').prop('disabled',true);

    $('#school_name').on('input', function(event) {
        if ($(this).val().trim() === '') {
            event.preventDefault();

            $('#school_name').autocomplete('option', 'source', displayedData);
            $('.autocomplete-load-more').hide();
        }
    });
    /** 
     * This is checking the input on this field. It cleans it up and ensures that autocompleteSelected is false 
     * which (later) means that autocomplete has not been done using search terms. This also ensure that the user
     * cannot submit the form and query input from the database until an autocompleted component is used to populate
     * the input field.
    */ 
    $('#school_name').on('input', function() {
        let inputValue = $(this).val().trim();
        
        // This is checking to ensure that the input that the user puts in is not A) empty and B) spaces.
        if (!autocompleteSelected && inputValue === '') {
            $('#searchBtn').prop('disabled', true);
            $('.autocomplete-load-more').show();
        } else {
            $('#searchBtn').prop('disabled', false);
            $('.autocomplete-load-more').hide();
        }

        if (inputValue.length > 0) {
            $('#school_name').autocomplete('option', 'source', allData);
            $('.autocomplete-load-more').hide();
        }
    });


    // This means that you selected one of the autocomplete options and inputted that into the field allowing for submission.
    $('#school_name').on('autocompleteselect', function(event, ui) {
        autocompleteSelected = true;
        $('#searchBtn').prop('disabled', false);
    });

    /** 
     * This is an extra layer of form submission prevention for the form so that the user cannot
     * immediately access the form without valid input. This helps in ensuring that the input field
     * and search button function properly.
    */
      
    $('#search-function').submit(function(event) {
        let inputValue = $('#school_name').val().trim();
        if (inputValue === '' || inputValue === null) {
            event.preventDefault(); // Prevent form submission
        }
        if (!autocompleteSelected) {
            event.preventDefault();
        }
    });

    /**
     * This frustrated me so much. Basically, this will accomplish two major things and one minor thing.
     * First, it will change the action of the form to activate the /query route, which allows the user
     * to fetch data and fulfill the autocomplete part of this script. This is important because the current
     * action when not clicking on the button or input field is set to direct you to the page
     * with the appropriate school's name. Second, when clicking on the input field (which houses #school_name),
     * it fulfills the autocomplete function with a search request with an input of blank. This may seem
     * counterintuitive, but I accounted for this in the routes file in which I made it so that if the
     * query were to be empty, it would yield a list of all possible schools --> this creates the ability to
     * scroll through the entire list of schools. Third, I wanted it to change how the placeholder would look
     * to improve UI/UX (maybe, idk).
     */
    $('#school_name').click(function() {
        $('#school_name').attr('action', '/query');
        $(this).autocomplete('search', '');
    })

    /**
     * This entire function utilizes JQuery, but this allows the user to access the
     * autocomplete route and see if their input returns any matching values from the database.
     * It will return these values stored in an array / list and will sort it by alphabetical
     * order to improve user scrolling experience. The minimumLength accounts for when
     * the user simply clicks on the input field and allows the autocompleted list to be shown
     * instantly. It lists the school_name in an unordered list and then will alow you to submit
     * that autocompleted value by clicking it. This was also super frustrating to work with.
     * 
     */

    let currentList = 0;
    let itemsPerList = 200;
    let allData = [];
    let displayedData = [];
    let loadMoreButton = $('<button>').text('Load More Schools').addClass('autocomplete-load-more');

    $('#school_name').autocomplete({
        source: function(request, response) {
            $.getJSON('/autocomplete', { query: request.term }, function(data) {
                $('#school_name').attr('placeholder', 'Scroll or search through ' + data.length + ' schools');
                allData = data.sort();

                // Reset displayed data and current list index when a new search is initiated
                displayedData = [];
                currentList = 0;
                loadMoreData(response);
            });
        },
        minLength: 0,
        select: function(event, ui) {
            $('#school_name').val(ui.item.value);
            $('#search-function').submit();
        },
        open: function(event, ui) {
            var $ul = $(this).autocomplete('widget');
            var $li = $('<li>').append(loadMoreButton);
            $ul.append($li);

            loadMoreButton.on('click', function() {
                loadMoreData(response);
            });
        }
    }).data('ui-autocomplete')._renderItem = function(ul, item) {
        return $('<li>')
            .append('<div>' + item.value + '</div>')
            .appendTo(ul)
            .addClass('autocomplete-item');
    };

    function loadMoreData(response) {
        var startIndex = currentList * itemsPerList;
        var endIndex = startIndex + itemsPerList;

        if (startIndex >= allData.length) {
            return;
        }

        // Load the next set of data
        var newData = allData.slice(startIndex, endIndex);
        displayedData = displayedData.concat(newData);
        currentList++;

        // Hide the button if all data is loaded
        if (endIndex >= allData.length) {
            $('.autocomplete-load-more').hide();
        } else {
            $('.autocomplete-load-more').show();
        }

        response(displayedData);
    }

    $(document).on('click', '.autocomplete-load-more', function() {
        loadMoreData(function(updatedList) {
            $('#school_name').autocomplete('option', 'source', updatedList);
            $('#school_name').autocomplete('search', $('#school_name').val());
        });
    });
});

/********************************************************* */
$(document).ready(function() {
    let allData = [];
    let autocompleteSelected = false;
    let courseData = [];
    let deleteAllAppended = false; 
    
    $('#addCourseButton').prop('disabled', true);
    $("#course-submit").prop("disabled", true);

    $('#course_name').autocomplete({
        source: function(request, response) {
            $.getJSON('/autocomplete_courses', { query: request.term }, function(data) {
                allData = data.sort();
                response(allData);
            });
        },
        minLength: 0,
        select: function(event, ui) {
            $('#course_name').val(ui.item.value);
            autocompleteSelected = true;
            validateInput(allData);
            $(this).autocomplete("close");
        },
        open: function(event, ui) {
            $(this).autocomplete("widget").off("keydown").on("keydown", function(event) {
                if (event.keyCode === $.ui.keyCode.ENTER) {
                    event.preventDefault();
                }
            });
        }
    });

    $('#course_name').on('keydown', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
        }
    });

    $('#course_name').on('input', function(event) {
        $('#course_name').autocomplete("close");
        autocompleteSelected = true;
        validateInput(allData);
    });

    function validateInput(allData) {
        let inputValue = $('#course_name').val().trim();
        let validValue = allData.includes(inputValue);
    
        if (inputValue === '' || validValue === false) {
            $('#addCourseButton').prop('disabled', true);
        } else if ($('.list-item-container li:contains("' + inputValue + '")').length > 0) {
            $('#addCourseButton').prop('disabled', true);
        } else {
            $('#addCourseButton').prop('disabled', false);
        }
    }

    document.getElementById("addCourseButton").addEventListener("click", addCourse);
    const courseList = document.getElementById("courseList");

    courseList.addEventListener("DOMNodeInserted", function(event) {
        if (courseList.children.length > 0) {
            $('#course-submit').prop('disabled', false);
        }
    
    });
    document.getElementById("temp-user-function").addEventListener('submit', function() {
        let storedData = document.createElement('input');
        storedData.type = 'hidden';
        storedData.name = 'courseData';
        storedData.value = JSON.stringify(courseData);
        this.appendChild(storedData);

        courseData = [];
    });

    function addCourse() {
        let courseName = document.getElementById("course_name").value;
        let apScore = document.getElementById("ap_score").value;

        if (courseName === "" || apScore === "") {
            return;
        }

        courseData.push({ courseName: courseName, apScore: apScore });
        sessionStorage.setItem('courseData', JSON.stringify(courseData));
        console.log(courseData);

        addCourseToList(courseName, apScore);
    }

    loadCourseDataFromSession();

    function loadCourseDataFromSession() {
        let storedData = sessionStorage.getItem('courseData');
        if (storedData) {
            courseData = JSON.parse(storedData);
            console.log("Retrieved courseData from session storage:", courseData);
            courseData.forEach(course => {
                addCourseToList(course.courseName, course.apScore);
            });
        }
    }

    function addCourseToList(courseName, apScore) {
        let deleteButton = createDeleteButton();
        let listItem = document.createElement("li");
        listItem.classList.add("course-list-item");
        listItem.textContent = `${courseName}: ${apScore}`;
        
        let listItemContainer = createItemContainer(listItem, deleteButton);
        
        deleteButton.addEventListener("click", function() {
            removeFromCourseData(courseName, apScore);
            listItemContainer.remove();
            toggleDeleteAllButton();
            $('#course_name').val('');
            let list = document.getElementById("courseList");
            if (list.children.length > 0) {
                $('#course-submit').prop('disabled', false);
            } else {
                $('#course-submit').prop('disabled', true);
            }
        });

        if (!deleteAllAppended) {
            appendDeleteAllButton();
            deleteAllAppended = true;
        }

        document.getElementById("courseList").appendChild(listItemContainer);

        document.getElementById("course_name").value = "";
        document.getElementById("ap_score").value = "1";
        $('#addCourseButton').prop('disabled', true);
        toggleDeleteAllButton();
    }

    /* HELPER FUNCTIONS TO CREATE DYNAMIC ELEMENTS */
    function removeFromCourseData(courseName, apScore) {
        courseData = courseData.filter(course => !(course.courseName === courseName && course.apScore === apScore));
        sessionStorage.setItem('courseData', JSON.stringify(courseData));
        console.log(courseData);
    }

    function appendDeleteAllButton() {
        let deleteAll = createDeleteAllButton();
        deleteAll.addEventListener("click", function() {
            courseData = [];
            sessionStorage.removeItem('courseData');
            $('#course_name').val('');
            let list = document.getElementById("courseList");
            list.innerHTML = "";
            toggleDeleteAllButton();
        });
        document.getElementById("deleteAllContainer").appendChild(deleteAll);
    }

    function toggleDeleteAllButton() {
        let list = document.getElementById("courseList");
        let deleteAllButton = document.getElementById("deleteAllButton");
        if (list.children.length > 0) {
            deleteAllButton.style.display = "block"; 
        } else {
            deleteAllButton.style.display = "none";
        }
    }

    function createItemContainer(listItem, deleteButton) {
        let listItemContainer = document.createElement("div");
        listItemContainer.classList.add("list-item-container", "border", "border-secondary");

        listItemContainer.appendChild(listItem);
        listItemContainer.appendChild(deleteButton);

        return listItemContainer;
    }

    function createDeleteButton() {
        let deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.classList.add("delete-button");
        
        let icon = document.createElement("i");
        icon.classList.add("si-close");

        deleteButton.appendChild(icon);

        return deleteButton;
    }

    function createDeleteAllButton() {
        let deleteAll = document.createElement("button");
        deleteAll.type = "button";
        deleteAll.classList.add("delete-button-all", "btn", "btn-danger");
        deleteAll.id = "deleteAllButton";
        
        let trashIcon = document.createElement("i");
        trashIcon.classList.add("si-trash");

        deleteAll.appendChild(trashIcon);

        return deleteAll;
    }

});


