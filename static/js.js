// stolen from guide to copy spotify front end, just for convenience since front end was not the focus of the project

/* Grab all the inputs that can be deleted from the document */
const _input_els = document.querySelectorAll('.input-group.can-delete input');
_input_els.forEach(_el => {
    /* When the user writes something on the input */
    _el.addEventListener('input', (e) => {
        const value = _el.value;
        /* Grab the nearest 'X' icon */
        const _clear_icon_el = _el.parentNode.querySelector('.clear--search');
        if (value == '') {
            /* Hide 'X' icon */
            _clear_icon_el.style.zIndex = '0';
        } else {
            /* Show 'X' icon */
            _clear_icon_el.style.zIndex = '2';
        }
    });
});

/* Get all the 'X' icons */
const _clear_icon_els = document.querySelectorAll('.clear--search');
_clear_icon_els.forEach(_el => {
    /* Clicking the 'X' icon */
    _el.addEventListener('click', (e) => {
        const _clear_icon_el = e.target;
        /* Get the input */
        const _input_el = e.target.parentNode.querySelector('input');
        if (_input_el) {
            /* Clear the input and hide the 'X' icon */
            _input_el.value = '';
            _clear_icon_el.style.zIndex = '0';
        }
    });
})
