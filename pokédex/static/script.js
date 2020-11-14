function pokésearch(event) {
    var query = event.target.value.toLowerCase();
    document.querySelectorAll(`.card`).forEach((element) => {
        if (element.id.includes(query)) {
            element.classList.remove('name_hidden')
        } else {
            element.classList.add('name_hidden');
        };
    })
}



let filter_set = new Set()

function includes_array(arr1, arr2) {
    var included = true
    arr2.forEach((el) => {
        if (!arr1.includes(el)) {
            included = false
        }
    })
    return included
}

function type_filter(event) {
    var type = event.target.classList[1].toLowerCase();
    console.log(type)
    if (event.target.classList.contains('inactive')) {
        event.target.classList.remove('inactive')
        filter_set.add(type)
    } else {
        event.target.classList.add('inactive')
        filter_set.delete(type)
    };
    document.querySelectorAll(`.card`).forEach((element) => {
        if (includes_array(element.dataset.types, filter_set)) {
            element.classList.remove('type_hidden');
        } else {
            element.classList.add('type_hidden');
        }
    })
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('pokésearch').addEventListener('keyup', pokésearch);
    document.querySelectorAll('.inactive').forEach((button) => { button.addEventListener('click', type_filter) })
})

