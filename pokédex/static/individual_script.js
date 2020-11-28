function switch_form(event) {
    var new_form = event.target.closest('.form_wrapper')
    if (!new_form.classList.contains('active')) {
        document.querySelector('.active').classList.remove('active');
        new_form.classList.add('active');
        document.querySelector('.current_form').classList.add('disabled_form');
        document.querySelector('.current_form').classList.remove('current_form');
        matching_form_div = document.querySelector(`#${new_form.id}.form`)
        matching_form_div.classList.add('current_form');
        matching_form_div.classList.remove('disabled_form');
        var sidebar =document.querySelector('#sidebar')
        sidebar.classList.value = ''
        sidebar.classList.add(matching_form_div.firstElementChild.classList.item(3))
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.form_wrapper').forEach((el) => {
        el.addEventListener('click', switch_form)
    })
})