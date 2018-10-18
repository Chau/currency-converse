

var setResponseToDom = function(response){
    $('#result').html(9876);
};


var sendCurrency = function(){
    console.log('go!');
    data = {'from': $('#from-currency option:selected').val(),
            'to': $('#to-currency option:selected').val(),
            'amount': $('#amount').val()
    }
    console.log(data);
    //TODO: ajax
    setResponseToDom(null);
};