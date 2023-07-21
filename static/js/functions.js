// opens the about popup
function showAbout() {
    var popup = document.getElementById("about");
    popup.classList.toggle("show");
    hideAbout();
}

// hides the about popup
function hideAbout() {
    var popup = document.getElementById("about");
    setTimeout(function() {
        popup.classList.remove("show");
    }, 5000); // time in milliseconds                    
}

setTimeout(function() {
    $('.notification-success').fadeOut(1000);
}, 4000); // time in milliseconds

setTimeout(function() {
    $('.notification-danger').fadeOut(1000);
}, 4000); // time in milliseconds

// function to create a new sticky note
function createNote() {
    var sticky_note_data = {
        "action": "create",
        "noteTitle": "Add title",
        "noteContent": "Add content"
    }
                        
    fetch(`/notes/`, {
        method: "POST",
        body: JSON.stringify(sticky_note_data),
        headers: new Headers ({
            'accept': 'application/json',
            'content-type': 'application/json'
        })
    });
    location.reload();
}

// function to save the content of the sticky notes
function saveNotes() {
    $(document).ready(function () {
        var noteId = [];
        var noteTitle = [];
        var noteContent = [];

        // loops through the list to get all the ids, titles and content
        $("li.sticky__note").find("i").each(function (index, ele) {
            noteId.push($(this).attr('id'));
        });
        
        $("li.sticky__note").find("h2").each(function (index, ele) {
            noteTitle.push(ele.innerHTML);
        });

        $("li.sticky__note").find("p").each(function (index, ele) {
            noteContent.push(ele.innerHTML);
        });
        
        // maps converts the noteId, noteTitle and noteContent arrays above into json to post
        mapArrays = (noteId, noteTitle, noteContent) => { 
            sticky_note_data = []; 
            for (let i = 0; i < noteId.length; i++) { 
                sticky_note_data.push({ 
                    "action": "save",
                    "noteId": noteId[i], 
                    "noteTitle": noteTitle[i],
                    "noteContent": noteContent[i]
                }); 
            }; 
            return sticky_note_data;
        }; 
        all_sticky_notes_data = mapArrays(noteId, noteTitle, noteContent);

        // post each sticky note content
        for (let j = 0; j < all_sticky_notes_data.length; j++) {
            fetch(`/notes/`, {
                method: "POST",
                body: JSON.stringify(all_sticky_notes_data[j]),
                headers: new Headers ({
                    'accept': 'application/json',
                    'content-type': 'application/json'
                })
            });
        }
        location.reload();
    });
}

// function to delete a sticky note
function deleteNotes(id) {
    var noteId = id;
    var sticky_note_data = {
        "action": "delete",
        "noteId": noteId
    }

    fetch(`/notes/`, {
        method: "POST",
        body: JSON.stringify(sticky_note_data),
        headers: new Headers ({
            'accept': 'application/json',
            'content-type': 'application/json'
        })
    });
    location.reload();
}