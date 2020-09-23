function openWindow(url, target = 'newwindow', height = 800, width = 800)
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

function search_company()
{
    $.widget("custom.autocomplete", $.ui.autocomplete, {
        // _renderItem: function (ul, item) {
        //     var link = '/stocks/';
        //     if (item.category === 'Sector') {
        //         link = '/sector/'
        //     }
        //
        //     return $("<li>")
        //         .append($("<div>").text(item.label))
        //         .attr('data-link', link)
        //         .appendTo(ul);
        // },
        _renderMenu: function (ul, items) {
            var that = this,
                currentCategory = "";

            $.each(items, function (index, item) {
                var li;
                if (item.category !== currentCategory) {
                    ul.append("<div class='ui-autocomplete-category'>" + item.category + "</div>");
                    currentCategory = item.category;
                }
                li = that._renderItemData(ul, item);
                if (item.category) {
                    li.attr("aria-label", item.category);
                }
            });
        }
    });

    var search_company_obj = $("#search_company");
    var search_company_id_obj = $("#search_company_id");
    var search_company_link_obj = $("#search_company_link");

    search_company_obj.autocomplete({
        source: function (request, response) {
            $.ajax({
                type: 'get'
                , url: '/stocks/company/list'
                , dataType: "json"
                , data: {
                    term: request.term,
                }
                , success: function (result) {
                    response(
                        $.map(result, function (item) {
                            return {
                                'code': item.code,
                                'label': item.name,
                                'value': item.name,
                                'category': item.category,
                            }
                        })
                    );
                }
                , error: function (jqXHR, textStatus, errorThrown) {
                    alert("Search error : " + errorThrown);
                }
            });
        },
        minLength: 1,
        autoFocus: true,
        delay: 500,
        classes: {
            'ui-autocomplete': 'highlight'
        },
        select: function (event, ui) {
            search_company_id_obj.val(ui.item.code);
            search_company_link_obj.val(ui.item.category);
        },
        focus: function (event, ui) {
            return false;
        },
        close: function (event) {
        }
    });

    search_company_obj.keydown(function (key) {
        if (key.keyCode === 13) {
            if (search_company_id_obj.val() === '') {
                return false;
            }

            if (search_company_link_obj.val() === '') {
                location.replace('/stocks/company/' + search_company_id_obj.val())
            }
            else {
                location.replace('/' + search_company_link_obj.val() + '/' + search_company_id_obj.val())
            }
        }
    })
}


/*
<div class="d-flex justify-content-center">
    <div class="spinner-border" role="status" style="visibility: hidden">
        <span class="sr-only">Loading...</span>
    </div>
</div>
* */
function set_spinner_visible()
{
    $(".spinner-border").css('visibility', 'visible');
}

function set_spinner_invisible()
{
    $(".spinner-border").css('visibility', 'hidden');
}