// i know this could be way more efficient but I'm a noob
// at javascript xD



// change to next tab
function nextTab(curr_tab, next_tab) {
    document.getElementById(curr_tab).style.display = "none";
    document.getElementById(next_tab).style.display = "block";
}


// go to previous tab
function prevTab(curr_tab, prev_tab) {
    document.getElementById(curr_tab).style.display = "none";
    document.getElementById(prev_tab).style.display = "block";
}

