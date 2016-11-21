$(document).ready(function() {
    $("#balance_btn").click(function() {
            window.location = "/";
    });
    $("#adj_exp_btn").click(function() {
        window.location = "/mod_expenses";
    });
    $("#view_btn").click(function() {
        window.location = "/expenses";
    });
    $("#clear_btn").click(function() {
        window.location = "/delete_all";
    });
});