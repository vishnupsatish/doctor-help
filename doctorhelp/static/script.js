$(document).ready(function() {
    $('.datepicker').datepicker({
        maxDate: new Date()
    });
    $('select').formSelect();
    $('.sidenav').sidenav();
    $('.fixed-action-btn').floatingActionButton();

});

function openNew() {
    document.location.href = "/new"
}
