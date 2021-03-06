$(document).ready(function(){
    $('form#login').attr('autocomplete', 'off');
    $('form#sign-up').attr('autocomplete', 'off');
    
    $('#login input#id_login_username').addClass('form-input-desc');
    $('#login input#id_login_username').val('Username');
    $('#login input#id_login_password').before('<input type="text" value="Password" id="password-clear" class="form-input-desc" />');
    $('#login input#id_login_password').hide();
    
    $('#login input#id_login_username').focus(function () {
        if ($('#login input#id_login_username').val() == 'Username') {
            $('#login input#id_login_username').removeClass('form-input-desc');
            $('#login input#id_login_username').val('');
        }
    });
    
    $('#login input#password-clear').focus(function () {
        $('#login input#password-clear').remove();
        $('#login input#id_login_password').show();
        $('#login input#id_login_password').focus();
    });
	
	// add parser through the tablesorter addParser method 
    $.tablesorter.addParser({ 
        // set a unique id 
        id: 'codes', 
        is: function(s) { 
			var match = /^[a-z]+(?:\-[0-9]+)?\.[a-z0-9]+$/i.test(s);
			
            return match; 
        }, 
        format: function(s) { 
			var pattern = /^([a-z]+)(?:\-|\.)/i;
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
    
     $.tablesorter.addParser({ 
        // set a unique id 
        id: 'credits', 
        is: function(s) { 
			var match = /^[0-9]+\so?cr$/i.test(s);
            
            return match; 
        }, 
        format: function(s) { 
			
			str = s.toLowerCase().replace(/\so?cr/i, '');
			
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
    
    $('table.profile-courses').addClass('tablesorter');
    $('table.profile-courses:not(table#planned-courses)').tablesorter({
        widgets: ['zebra']
    });
    
    $('table#planned-courses').tablesorter({
        widgets: ['zebra'],
        headers: {
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
    
    $('#recommend-friend-list form input[type=checkbox]').hide();
    
    $('#recommend-friend-list form input[type=checkbox]').each(function () {
        if ($(this).attr('checked')) {
            $(this).parent('div').css('border', '2px solid #0252C0');
            $(this).parent('div').css('background-color', '#e8eafe');
            $(this).parent('div').css('margin-right', '6px');
            $(this).parent('div').css('margin-bottom', '11px');
        }
        
        $(this).parent('div').children().each(function () {
            $(this).css('cursor', 'pointer');
        });
    });
    
    $('#recommend-friend-list form div:not(div.button)').click(function () {
        
        if (!$(this).children('input[type=checkbox]').attr('checked')) {
            $(this).children('input[type=checkbox]').attr('checked', true);
            $(this).css('border', '2px solid #0252C0');
            $(this).css('background-color', '#e8eafe');
            $(this).css('margin-right', '6px');
            $(this).css('margin-bottom', '11px');
        } else {
            $(this).children('input[type=checkbox]').attr('checked', false);
            $(this).css('border', 'none');
            $(this).css('background-color', '#fff');
            $(this).css('margin-right', '10px');
            $(this).css('margin-bottom', '15px');
        }
        
        return false;
    });
});