document.addEventListener("DOMContentLoaded", function() {
    showEmailDate('email_date', document.getElementById('emailed'));
  });

function showEmailDate(divId, element)
{
    document.getElementById(divId).style.display = element.value == "Yes" ? 'block' : 'none';
}