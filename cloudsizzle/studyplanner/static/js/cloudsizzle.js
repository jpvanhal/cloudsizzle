$(document).ready(function(){
    $('form#login').attr('autocomplete', 'off');
    $('form#sign-up').attr('autocomplete', 'off');
    
    $('#login input#id_username').addClass('form-input-desc');
    $('#login input#id_username').val('Username');
    $('#login input#id_password').before('<input type="text" value="Password" id="password-clear" class="form-input-desc" />');
    $('#login input#id_password').hide();
    
    $('#login input#id_username').focus(function () {
        if ($('#login input#id_username').val() == 'Username') {
            $('#login input#id_username').removeClass('form-input-desc');
            $('#login input#id_username').val('');
        }
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

	$('table.courses').addClass('tablesorter');
	$('table.courses').tablesorter({
        widgets: ['zebra']
    });
    
    $('#advanced-search table').addClass('tablesorter');
    $('#advanced-search table.courses').tablesorter({
        widgets: ['zebra']
    });
    $('#advanced-search table.users').tablesorter({
        widgets: ['zebra'],
        headers: {
            0: {
                sorter: false
            },
            4: {
                sorter: false
            }
        }
    });
    
    $('#advanced-search table.users form').submit(function () {
        
        var actionURL = $(this).attr('action');
        var form = $(this);
        
        $(this).children('div').replaceWith('<div class="loading"></div>');
        
        $.ajax({
            url: actionURL,
            type: 'POST',
            cache: false,
            success: function(data, textStatus, XMLHttpRequest) {
                form.children('div.loading').remove();
                form.replaceWith('<span class="success">Friend request sent</span>');
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                form.children('div.loading').remove();
                form.replaceWith('<span class="error">An error occurred</span>');
            }
        });
        
        return false;
    });
    
    $('form#search').submit(function (event) {
        var query = $('form#search input#query').val();
        var scope = $('form#search input#scope').val();
        var actionURL = $(this).attr('action') + '?query=' + query + '&scope=' + scope;
        
        window.location = actionURL;

        return false;
    });
});