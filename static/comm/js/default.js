function openWindow(url, target='newwindow', height = 800, width = 800)
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

function request_ajax_n_reload(url)
{
    showGlobalLoading();

    $.ajax({
        type: 'POST',
        url: url,
        accept: 'application/json',
        dataType: 'json',
        processData: false,
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN)
            xhr.setRequestHeader('Content-Type', 'application/json')
        },
        success: function (result) {
            if (result.code === '0000') { location.reload(); }
            else { alert(result.msg); }
            removeGlobalLoading();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert(errorThrown)
            removeGlobalLoading();
        },
    })
}