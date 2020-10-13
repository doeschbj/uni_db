

    restoreContents();

    function saveContents() {
        var aList = $('#auftragsliste').html();
        localStorage['auftragsliste'] = aList;
    }

    function restoreContents() {
        var aList = localStorage['auftragsliste'];
        if (aList != undefined) {
            $('#auftragsliste').html(aList);
        }
    }
    function resetContent(e) {
        localStorage.clear();
        window.location.reload();
    }

    var save_list  = document.getElementById('save_list');

    save_list.addEventListener ('click', saveContents, true);
