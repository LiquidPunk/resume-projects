
function toggleMenu(x)
{
    x.classList.toggle("change");
    var dropdown = x.parentElement.querySelector('.dropdown-menu');
    dropdown.classList.toggle("show");
}
document.addEventListener('click', function(event)
{
    var dropdown = document.querySelector('.user-dropdown');
    if (!dropdown.contains(event.target))
    {
        var button = dropdown.querySelector('div.container');
        if (button.classList.contains('change'))
        {
            button.classList.remove('change');
            dropdown.querySelector('.dropdown-menu').classList.remove("show");
        }
    }
});

