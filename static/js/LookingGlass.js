/**
 * LookingGlass jQuery file
 */
$(document).ready(function() {
    // onclick, set user IP to input value
    $('#userip').click(function () {
        $('#host').val($('#userip').text());
    });
    // form submit
    $('#networktest').submit(function() {
        // define vars
        var router  = $('select[name=router]').val();
        var host    = $('input[name=host]').val();
        var cmd     = $('select[name=cmd]').val();
        var version = $('select[name=version]').val();

        var data = 'router=' + router + '&cmd=' + cmd + '&host=' + host + '&version=' + version;

        // quick validation
        // submit form
        // disable submit button + blank response
        $('#submit').attr('disabled', 'true').text('Loading...');
        $('#response').html();

        // call async request
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'ajax?' + data, true);
        xhr.send(null);
        var timer;
        timer = window.setInterval(function() {
            // on completion
            if (xhr.readyState == XMLHttpRequest.DONE) {
                window.clearTimeout(timer);
                $('#submit').removeAttr('disabled').text('Run Test');
            }

            // show/hide results
            if (xhr.responseText == '') {
                $('#response').hide();
            } else {
                $('#hosterror').removeClass('error');
                $('#response, #results').show();
            }

            // output response
            if (xhr.responseText == 'Unauthorized request') {
                $('#results').hide();
                $('#hosterror').addClass('error');
            } else {
                $('#response').html(xhr.responseText.replace(/<br \/> +/g, '<br />'));
            }
        }, 500);

        // cancel default behavior
        return false;
    });
});
