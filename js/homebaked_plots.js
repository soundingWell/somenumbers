/*
var income_vs_expenses = function(txn_list) {
    var bar_div = document.createElement('div');
    bar_div.id = 'bar_div';
    document.body.appendChild(bar_div);
            
    var labels = ["Income", "Essential", "Food", "Fun"];
    var values = [0, 0, 0, 0];
            
    for (var txn in txn_list) {                
        var txn_type = txn_list[txn].txn_type;
        var amt = txn_list[txn].amount;
                
        // Match txn_type to label.
        var label_index = labels.indexOf(txn_type);
        if (label_index != -1) {
            values[label_index] += Math.abs(parseFloat(amt));
        }
    }
            
    var income = {
        x: ['Income'],
        y: [values[0]],
        name: 'Income',
        type: 'bar'
    };
                
    var essentials = {
        x: ['Expenses'],
        y: [values[1]],
                
        name: 'Essentials',
        type: 'bar'
    };
            
    var food = {
        x: ['Expenses'],
        y: [values[2]],
        name: 'Food',
        type: 'bar'
    };
            
     var fun = {
        x: ['Expenses'],
        y: [values[3]],
        name: 'Fun',
        type: 'bar'
    };

    var data = [income, essentials, food, fun];
    // var data = [income];

        var layout = {
            title: 'Income vs. Expenses',
            barmode: 'stack',
        };

        Plotly.newPlot('bar_div', data, layout);
}*/