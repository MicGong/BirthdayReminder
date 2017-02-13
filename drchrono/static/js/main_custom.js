
$(document).ready(function() {
    // Set select all checkbox
    $("input[name='select-all-patients']").click(function(e) {
        $('.patient-checkbox').prop('checked', e.target.checked);
    });

    // Set search button
    $('#search-btn').click(function(e) {
        var first_name = $('#search-first-name').val();
        var last_name = $('#search-last-name').val();
        var date_of_birth = $('#search-bday').val();
        var result = $();
        if (first_name) {
            result = result.add(
                $('#patient-table > tbody > tr .first-name-col').filter(':contains('+first_name+')').closest('tr'));
        }
        if (last_name) {
            result = result.add(
                $('#patient-table > tbody > tr .last-name-col').filter(':contains('+last_name+')').closest('tr'));
        }
        if (date_of_birth) {
            result = result.add(
                $('#patient-table > tbody > tr .date-of-birth-col').filter(':contains('+date_of_birth+')').closest('tr'));
        }
        $('#patient-table > tbody > tr').not(result).hide();
    });

    // Set reset button
    $('#reset-btn').click(function(e) {
        $('#patient-table > tbody > tr').show();
        $(e.target).closest('form').find('input[type="text"]').val("");
    });

    // Save email with Ajax
    $('#email-form :submit, #save-btn-custom').click(function(e) {
        e.preventDefault();
        console.log('save email!');
        var title = $(e.target).closest('form').find('input[type=text]').val();
        var body = $(e.target).closest('form').find('textarea').val();
        $.ajax({
            method: "POST",
            url: "edit-email/",
            data: {"title":title, "body":body}
        }).done(function(data){
            if ('error' in data) {
                warning = ""
                for (var key in data['error'])
                    warning += "error in " + key + ": " + data['error'][key].join(',')
                alert(warning)
            } else {
                $('#default-email-title').html(data['title']);
                $('#default-email-body').html(data['body']);
                $('#default-email-edit-modal').modal('hide');
            }
        });
    });

    var get_checked_rows = function() {
        var rows = $('#patient-table > tbody').find('input:checked').closest('tr');
        var emails = $(rows).find('.email-col').toArray();
        var first_names = $(rows).find('.first-name-col').toArray();
        var last_names = $(rows).find('.last-name-col').toArray();
        var emails_arr = [], first_names_arr = [], last_names_arr = [];
        for (var i = 0; i < emails.length; i++) {
            emails_arr[i] = $(emails[i]).html();
            first_names_arr[i] = $(first_names[i]).html();
            last_names_arr[i] = $(last_names[i]).html();
        }
        return [emails_arr, first_names_arr, last_names_arr];
    };

    // Send emails with default email tempalte
    $('#send-btn-default').click(function(e) {
        // e.preventDefault();
        // var rows = $('#patient-table > tbody').find('input:checked').closest('tr');
        // var emails = $(rows).find('.email-col').toArray();
        // var first_names = $(rows).find('.first-name-col').toArray();
        // var last_names = $(rows).find('.last-name-col').toArray();
        // var emails_arr = [], first_names_arr = [], last_names_arr = [];
        // for (var i = 0; i < emails.length; i++) {
        //     emails_arr[i] = $(emails[i]).html();
        //     first_names_arr[i] = $(first_names[i]).html();
        //     last_names_arr[i] = $(last_names[i]).html();
        // }
        [emails_arr, first_names_arr, last_names_arr] = get_checked_rows();
        $.ajax({
            method: "POST",
            url: "send-email-default/",
            data: {"emails":emails_arr, "first_names":first_names_arr, "last_names":last_names_arr},
            ContentType: "application/json",
            traditional: true,
        }).done(function(data) {
            console.log("sent email with saved template!");
            alert("Email Sent!");
        }).error(function(e) {
            alert("Error when sending email!");
            console.log("error sending emails!")
        });
    });

    // Send emails with custom email without saving
    $('#send-btn-custom-no-saving').click(function(e) {
        [emails_arr, first_names_arr, last_names_arr] = get_checked_rows();
        var title = $(e.target).closest('form').find('input[type=text]').val();
        var body = $(e.target).closest('form').find('textarea').val();
        $.ajax({
            method: "POST",
            url: "send-email-custom/",
            data: {"emails":emails_arr, "first_names":first_names_arr, "last_names":last_names_arr, "title":title, "body":body},
            ContentType: "application/json",
            traditional: true,
        }).done(function(data) {
            console.log("sent email with custom mail!");
            alert("Email Sent!");
        }).error(function() {
            alert("Error when sending email!");
            console.log("error sending emails!")
        });
    });

    // Send emails with custom email and save to template
    $('#send-btn-custom-with-saving').click(function(e) {
        [emails_arr, first_names_arr, last_names_arr] = get_checked_rows();
        var title = $(e.target).closest('form').find('input[type=text]').val();
        var body = $(e.target).closest('form').find('textarea').val();
        $.ajax({
            method: "POST",
            url: "edit-email/",
            data: {"title":title, "body":body}
        }).done(function(data){
            if ('error' in data) {
                warning = ""
                for (var key in data['error'])
                    warning += "error in " + key + ": " + data['error'][key].join(',')
                alert(warning)
            } else {
                $('#default-email-title').html(data['title']);
                $('#default-email-body').html(data['body']);
                $('#default-email-edit-modal').modal('hide');
            }
        });
        $.ajax({
            method: "POST",
            url: "send-email-custom/",
            data: {"emails":emails_arr, "first_names":first_names_arr, "last_names":last_names_arr, "title":title, "body":body},
            ContentType: "application/json",
            traditional: true,
        }).done(function(data) {
            console.log("sent email with custom mail!");
            alert("Email Sent!");
        }).error(function() {
            alert("Error when sending email!");
            console.log("error sending emails!")
        });
    });

    // CSRF token
    function getCookie(name) {  
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});