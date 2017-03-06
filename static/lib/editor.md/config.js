// body
(function () {
    var context = setTimeout(function () {
        var body_father = document.getElementsByClassName('field-body')[0].childNodes[1];
        var divtag = document.createElement('div');
        var text = document.getElementById('id_body');
        divtag.setAttribute("id", "bodytext");
        divtag.appendChild(text);
        body_father.appendChild(divtag);
        $(function () {
            var editor = editormd("bodytext", {
                height: "720px",
                path: "/static/lib/editor.md/lib/",
                imageUpload: true,
                imageFormats: ["jpg", "jpeg", "gif", "png"],
                imageUploadURL: "/upload/"
            });
        });
    }, 1)
})();