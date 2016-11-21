// Monotonically increasing.
var G_BTN_ID = 0;
        
function replace_txn_type(txn_json, btn_id) {
    var btn = document.getElementById(btn_id);
    var row = btn.parentNode.parentNode;
    var txn = JSON.parse(txn_json);
    row.cells[3].innerHTML = txn.txn_type;
}
        
function send_txn(txn_json, btn_id) {
    replace_txn_type(txn_json, btn_id);
        
    $.ajax({
        type: "POST",
        url: "/mod_expenses",
        dataType: "text",
        data: txn_json,
        success: function (data) {
            window.console.log('data: ' + data);
            window.console.log('Success');
        },
        error: function (xhr, status, error) {
            window.console.log(xhr.responseText);
        }
    });
}
        
// Make the txn_type button. txn_type is a param.
function create_txn_type_button(txn, txn_type) {
    var btn = document.createElement("BUTTON"); // Create a <button> element
            
    txn.txn_type = txn_type;
    var txn_json = JSON.stringify(txn);
            
    btn.innerHTML=txn_type;
    btn.id = 'btn' + G_BTN_ID.toString();
    G_BTN_ID += 1;
    btn.value = txn_json;
            
    // When the button is clicked, send the dict to be put.
    btn.onclick = function() { send_txn(this.value, this.id); };
            
    return btn;
}

// Cell with buttons to select charge type.
function create_txn_type_cell(date, desc, amt) {
    var txn_type_cell = document.createElement('td');
    var txn = {};
    txn.date = date;
    txn.desc = desc;
    txn.amt = amt;
            
    txn_type_cell.appendChild(create_txn_type_button(txn, 'Essential'));
    txn_type_cell.appendChild(create_txn_type_button(txn, 'Food'));
    txn_type_cell.appendChild(create_txn_type_button(txn, 'Fun'));
    txn_type_cell.appendChild(create_txn_type_button(txn, 'Income'));
    txn_type_cell.appendChild(create_txn_type_button(txn, 'Transfer'));
    txn_type_cell.appendChild(create_txn_type_button(txn, 'Rent'));
    txn_type_cell.appendChild(create_txn_type_button(txn, 'Car Insurance'));
    txn_type_cell.appendChild(create_txn_type_button(txn, 'Other'));
            
    return txn_type_cell;
}

// Returns an html table_header object.
function create_header(categories) {
    var header = document.createElement('thead');
    var table_head = document.createElement('tr'); // Creating the row

    for (var i = 0; i < categories.length; i++) {
        var curr_cell = document.createElement('td');
        curr_cell.innerHTML= "<b>" + categories[i] + "</b>";
        curr_cell.style.color= "rgb(0,109,176)";
        table_head.appendChild(curr_cell);   
    }

    header.appendChild(table_head);
            
    return header;
}

// Return html text cell for placement in a row.
function create_text_cell(text) {
    var text_cell = document.createElement('td');
    text_cell.innerHTML = text;
    text_cell.style.textAlign = "center";
            
    return text_cell;
}

// Text cell where text is red if it's < 0, green if amt > 0
function create_amt_text_cell(amt) {
    var amt_cell = document.createElement('td');
    amt_cell.innerHTML = amt;
    amt_cell.style.textAlign = "center";
    if (parseFloat(amt) < 0) {
        amt_cell.style.color = "rgb(128, 0, 0)";
    }  else {
        amt_cell.style.color = "rgb(0, 128, 0)";
    }

    return amt_cell;
 }

// Return html row for placement in a table.
function create_row(date, desc, amt, txn_type) {
    var row = document.createElement('tr');
    row.appendChild(create_text_cell(date));
    row.appendChild(create_text_cell(desc));
    row.appendChild(create_amt_text_cell(amt));
    row.appendChild(create_text_cell(txn_type));
    row.appendChild(create_txn_type_cell(date, desc, amt));
            
    return row; 
}

function create_txn_table(txn_list) {
    var tbl = document.createElement('table');
    tbl.id='theTable';
    tbl.setAttribute('border', '1');
    tbl.cellPadding = "3";
    tbl.cellSpacing = "3";
    var categories = ["Date", "Description", "Amount", "Current Type", "Type"];
    tbl.appendChild(create_header(categories));

    for (var txn in txn_list) {
        tbl.appendChild(
            create_row(txn_list[txn].date, txn_list[txn].desc, 
            txn_list[txn].amount, txn_list[txn].txn_type));
    }
          
    return tbl;
}