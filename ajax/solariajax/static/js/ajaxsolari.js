// Copyright (c) 2010 Eli Stevens
// 
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.


function process(data, textStatus, XMLHttpRequest) {
    //alert(data, textStatus)
    for (var i in data) {
        var command = data[i];
        var action = command.action;
        
        // These are roughly ordered by usage frequency.
        if (action == 'replace') {
            //var where = $(command.where);
            //TODO: handle anim
            $(command.selector).html(command.html);
        }
        else if (action == 'eval') {
            eval(command.script)
        }
        else if (action == 'append') {
            $(command.selector).html(function(index, old) { return old + command.html });
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
            else if (this.type == 'checkbox' || this.type == 'radio') {
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
