document.addEventListener('DOMContentLoaded', function() {
    let selectElems = document.querySelectorAll('select');
    let selectInstances = M.FormSelect.init(selectElems);
    

    let currYear = new Date().getFullYear();
    let currMonth = new Date().getMonth();
    let currDay = new Date().getDate();

    let dateElems = document.querySelectorAll('.datepicker');
    let dateInstances = M.Datepicker.init(dateElems, {
        format: 'yyyy-mm-dd',
        defaultDate: new Date(currYear, currMonth-1, currDay),
        maxDate: new Date(currYear, currMonth-1, currDay),
        yearRange: [2020, currYear]
    });

    let imageElems = document.querySelectorAll('.materialboxed');
    let imageInstances = M.Materialbox.init(imageElems);

    let collapibleElems = document.querySelectorAll('.collapsible');
    let collapsibleInstances = M.Collapsible.init(collapibleElems);
});

function validateForm() {
    let firstAmount = parseInt(document.querySelector('input[name="percentage_first"]').value) || 0;
    let secondAmount = parseInt(document.querySelector('input[name="percentage_second"]').value) || 0;
    let thirdAmount = parseInt(document.querySelector('input[name="percentage_third"]').value) || 0;

    let firstCurrency = document.querySelector('select[name="curr_first"]').value;
    let secondCurrency = document.querySelector('select[name="curr_second"]').value;
    let thirdCurrency = document.querySelector('select[name="curr_third"]').value;

    let startDate = document.querySelector('input[name="start_date"]').value;

    if (firstCurrency === "" || secondCurrency === "" || thirdCurrency === "") {
        alert('Proszę wybrać walutę');
        return false;
    }

    if (firstCurrency === secondCurrency || firstCurrency === thirdCurrency || secondCurrency === thirdCurrency) {
        alert('Proszę wybrać różne waluty dla każdej pozycji!');
        return false;
    }

    if (startDate.trim() === "") {
        alert('Proszę podać datę rozpoczęcia inwestycji!');
        return false;
    }
    
    let total = firstAmount + secondAmount + thirdAmount;

    if (total !== 100) {
        alert('Suma procentów musi wynosić 100%!');
        return false;
    }

    return true;
}
