function process_response(data, replacement) {
    if (data.hasOwnProperty('text')) {
        $(replacement).replaceWith('<div>' + data['text'] + '</div>')
    }
    if (data.hasOwnProperty('eval')) {
        eval(data['eval']);
    }
    if (data.hasOwnProperty('append')) {
        $(replacement).append('<div class="success">' + data['append'] + '</div>')
    }
    if (data.hasOwnProperty('redirect')) {
        document.location.href = data['redirect']
    }
}
function submitform(e) {
    $('.success').remove();
    $.ajax({
        type: "GET",
        url: $(e).attr('action'),
        data: $(e).serialize(),
        success: function(data) {
            process_response(data, e)
        },
        error: function(resp) {
            $('.form-group').removeClass('has-error');
            $('.help-block').remove();
            $('#upl').remove();
            var errors = JSON.parse(resp.responseText);
            for (error in errors['errors']) {
                if (error == '__all__')
                    $(e).before('<div id="upl" class="alert alert-danger">' + errors['errors'][error] + '</div>');
                else {
                    $('#id_' + error).parents('.form-group:first').addClass('has-error');
                    $('#id_' + error).after('<span class="help-block">' + errors['errors'][error] + '</span>')
                }
            }
        }
    });
}
function user_exists() {
    var mail = $('#id_email').val();
    if (mail != '') {
        $.ajax({
            type: "POST",
            url: '/userexists/',
            data: {
                'mail': mail
            },
            success: function(data) {
                $('#id_password').parents('.form-group:first').show();
            },
            error: function(resp) {
                $('#id_password').parents('.form-group:first').hide();
            }
        });
    } else {
        $('#id_password').parents('.form-group:first').hide();
    }
}
function like(id_hash) {
    $.ajax({
        type: "GET",
        url: '/like/',
        data: {
            "id_hash": id_hash
        },
        success: function(data) {
            $('#num-likes' + id_hash).html(data);
            $('#btn-likes' + id_hash).html(data);
        }
    });
}
var loading = false;
function load_latest(url) {
    var last = $('.artwork-row').children().last();
    var lastid = last.attr('id');
    if (!loading) {
        loading = true;
        $.ajax({
            type: "GET",
            url: url,
            data: {
                'last': lastid
            },
            success: function(data) {
                loading = false;
                last.after(data)
            }
        });
    }
}
$(function() {
    $('a[href*=#]:not([href=#]):not(.carousel-control):not(.tab)').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html,body').animate({
                    scrollTop: (target.offset().top - 50)
                }, 750);
                return false;
            }
        }
    });
});
