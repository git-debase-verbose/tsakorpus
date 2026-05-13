$(function() {
    rotate_placeholders();
    $('#show_text_list').unbind('click');
    $('#show_text_list').click(load_subcorpus_documents_simple);
});

function rotate_placeholders() {
    var txt = $("#all_in_one_search_txt");
    var hints = (txt.data("hints") || "").split(";");
    var iHint = 0;
    var timer;

    function rotate_placeholders_step() {
        if (hints.length === 0) return;
        txt.attr("placeholder", $.trim(hints[iHint]));
        iHint = (iHint + 1) % hints.length;
        timer = setTimeout(rotate_placeholders_step, 2000);
    }

    rotate_placeholders_step();
    txt.on("focus click", function () {
        clearTimeout(timer);
        txt.attr("placeholder", "");
    });
}

function load_subcorpus_documents_simple(e) {
    $.ajax({
        url: "search_doc_simple",
        type: "GET",
        success: print_document_list_simple,
        error: function(errorThrown) {
            alert( JSON.stringify(errorThrown) );
        }
    });
}

function print_document_list_simple(results) {
    $('#simple_text_list_table').html(results);
    $("#simple_text_list").modal('show');
    enable_datatables(".documents_list_table");
}
