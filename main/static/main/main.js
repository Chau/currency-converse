
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


//--
var setResponseToDom = function(response){
    console.log(response);
    if (response['status'] == 400 ){
        var error_messages = response['error']['message'];
        alert(error_messages.join('\n'));
        return;
    };
    var converted_amount = response['converted_amount'];
    $('#result').html(converted_amount);
};


var sendCurrency = function(){
    var from_currency = $('#from-currency option:selected').val();
    var to_currency = $('#to-currency option:selected').val();
    if (from_currency == to_currency) {
        alert('Select different currency types!');
        return false;
    }
    var amount = $('#amount').val();

    if (amount == '' || amount == undefined){
        alert("Fill amount field, please!");
        return false;
    }
    data = {'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount
    }
    $.post('/api/currency/converse', data, setResponseToDom);

};