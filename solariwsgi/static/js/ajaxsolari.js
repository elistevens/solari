function process(data, textStatus, XMLHttpRequest) {
    //alert(data, textStatus)
    for (var i in data) {
        var args = data[i];
        if (args.what == 'replace') {
            //var where = $(args.where);
            $(args.where).html(args.html);
        }
        else if (args.what == 'append') {
            $(args.where).html(function(index, old) { return old + args.html});
        }
        else if (args.what == 'eval') {
            eval(args.script)
        }
    }
}

function collectInput() {
    var input = {};
    for(var i=0; i< arguments.length; i++) {
        $(arguments[i]).each(function(index) {
            if (this.disabled == true) {
                ;
            }
            else if (this.selectedIndex != null) {
                input[this.name] = this.options[this.selectedIndex].value;
            }
            else if (this.type == 'checkbox') {
                if (this.checked) {
                    input[this.name] = this.value;
                }
            }
            else {
                input[this.name] = this.value;
            }
        });
    }
    
    return input;
}

//$(document).ready(function() {
//    $.ajax({
//        url: '/rsvp/display_login',
//        dataType: 'json',
//        data: {},
//        success: process
//    });
//});
