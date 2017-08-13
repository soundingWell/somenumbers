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
}

var expense_breakdown = function(start_date=0, end_date=0) {
            remove_child_nodes("expense_breakdown_div");
            var json_txn_list = {{db_txns|safe}};
            var txn_list = json_txn_list.txns;
        
            data = [];
            pie_graph = {};
            
            labels = ["Essential", "Food", "Fun"];
            values = [0, 0, 0];

            // Loop through txns and pie chart main expense types.
            for (txn in txn_list) {
                txn_date = txn_list[txn].date;

                if (start_date != 0) {
                    if (txn_date < start_date) {
                        continue;
                    }
                }
                if (end_date != 0) {
                    if (txn_date > end_date) {
                        break;
                    }
                }
                
                txn_type = txn_list[txn].txn_type;
                amt = txn_list[txn].amount;

                // Match txn_type to label.
                label_index = labels.indexOf(txn_type);
                if (label_index != -1) {
                    values[label_index] += parseFloat(amt) * -1;
                }
            }
            
            pie_graph['values'] = values;
            pie_graph['labels'] = labels;
            pie_graph['type'] = 'pie';
            data.push(pie_graph);
            
            if (start_date == 0) {
                start_date = "Beginning";
            } else {
                start_date = date_int_to_str(start_date);
            }
            if (end_date == 0) {
                end_date = "End";
            } else {
                end_date = date_int_to_str(end_date);
            }
            
            var layout = {
                title: ('Expenses By Type from ' + start_date + ' to ' + end_date),
                height: 400,
                width: 500,
                paper_bgcolor: '#ecf0f1',
                plot_bgcolor: '#ecf0f1',
            };
            
            Plotly.newPlot('expense_breakdown_div', data, layout);
        }
*/