function showBox() {

    document.getElementById("expenses-container").style.display = "flex";   // Show Expenses Form
    document.getElementById("expenses-container").style.transition = "all 3s ease-out";
    document.getElementById("xpenses-table").style.display = "none";
    document.getElementById("toggle-xpense-form").style.display = "none";   // Hide Form toggle btn

};


function closeBox() {
    windows.location.reload()
};