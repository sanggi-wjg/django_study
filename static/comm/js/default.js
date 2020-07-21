function openWindow(url, height = 800, width = 800)
{
    window.open(url, 'newwindow', 'height=' + height + ', width=' + width + ', top=0,left=0, toolbar=no, menubar=no, scrollbars=no, resizable=no,location=no,status=no')
}

function showGlobalLoading()
{
    document.getElementById("GlobalLoadingBox").style.display = "block";
    return true;
}

function removeGlobalLoading()
{
    document.getElementById("GlobalLoadingBox").style.display = "none";
    return true;
}