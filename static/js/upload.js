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
let submitting = false;
function submitform(e) {
    $('.success').remove();
    if (submitting){
        alert("已提交，正在处理，请稍后");
        return;
    }
    submitting = true;
    $.ajax({
        type: "GET",
        url: $(e).attr('action'),
        data: $(e).serialize(),
        success: function(data) {
            process_response(data, e);
            submitting = false;
        },
        error: function(resp) {
            $('.form-group').removeClass('has-error');
            $('.help-block').remove();
            $('#upl').remove();
            var errors = JSON.parse(resp.responseText);
            $(e).before('<div id="upl" class="alert alert-danger">' + errors['msg'] + '</div>');
            submitting = false;
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
