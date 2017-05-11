function add_swimmer() {
    window.location.href = '/new_swimmer';
}

function new_times(swim_id) {
    window.location.href = '/add_times/'+swim_id;
}

function search_swimmer() {
    var text = document.getElementById('search_box').value;
    if (text) {
        window.location.href = '/search_swimmer='+text;
    }
    else {
        alert("Text field is empty. Please enter a search term to continue.");
    }
}

function search_team() {
    var text = document.getElementById('search_box').value;
    if (text) {
        window.location.href = '/search_team='+text;
    }
    else {
        alert("Text field is empty. Please enter a search term to continue.");
    }
}

function ajax_buttion() {
	
}