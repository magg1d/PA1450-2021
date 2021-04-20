var today = new Date();
var dd = today.getDate();
var mm = today.getMonth() + 1; //January is 0!
var yyyy = today.getFullYear();
if (dd < 10) {
    dd = '0' + dd
}
if (mm < 10) {
    mm = '0' + mm
}

today = yyyy + '-' + mm + '-' + dd;
document.getElementById("end-date").setAttribute("max", today);
document.getElementById("start-date").setAttribute("max", today);


function formCheck()
{
    if (document.getElementById('delta-data').checked)
    {
      document.getElementById('interval').disabled = false;
    }
    else
    {
        document.getElementById('interval').disabled = true;
    }

}