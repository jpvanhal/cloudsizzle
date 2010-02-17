$(document).ready(function(){
    $('#login form').attr('autocomplete', 'off');
    $('#sign-up form').attr('autocomplete', 'off');
    
    $('#login input#id_username').addClass('form-input-desc');
    $('#login input#id_username').val('Username');
    $('#login input#id_password').before('<input type="text" value="Password" id="password-clear" class="form-input-desc" />');
    $('#login input#id_password').hide();
    
    $('#login input#id_username').focus(function () {
        $('#login input#id_username').removeClass('form-input-desc');
        $('#login input#id_username').val('');
    });
    
    $('#login input#password-clear').focus(function () {
        $('#login input#password-clear').remove();
        $('#login input#id_password').show();
        $('#login input#id_password').focus();
    });
	
	// add parser through the tablesorter addParser method 
    $.tablesorter.addParser({ 
        // set a unique id 
        id: 'codes', 
        is: function(s) { 
			var match = /^[a-z]+\-[0-9]+\.[0-9]+$/i.test(s);
			
            return match; 
        }, 
        format: function(s) { 
			
			var pattern = /^([a-z]+)\-/i;
			var matches = s.match(pattern);
			
			var str = '';
			for (var i = 0; i < matches[1].length; i++) {
				var letter = matches[1].charCodeAt(i);
				str += letter + '';
			}
			
			str += s.toLowerCase().replace(/^[a-z]+\-/i, '').replace(/\./, '') + '';
			
            // format your data for normalization 
            return str;
        }, 
        // set type, either numeric or text 
        type: 'numeric' 
    });

	$('#courses table').addClass('tablesorter');
	$('#courses table').tablesorter({sortList:[[0,0],[2,1]], cssDesc: 'headerSortDown', widgets: ['zebra']});
});
