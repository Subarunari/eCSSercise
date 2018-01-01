window.onload = function(e) {
    var editor = ace.edit("csseditor");
    editor.setTheme("ace/theme/twilight");
    editor.session.setMode("ace/mode/css");
    editor.session.on('change', function(){
        iframe.contentWindow.addStyleString(editor.getValue());
    });

    var iframe = document.getElementById("rendered_html");
    var style_node = iframe.contentDocument.createElement('style');
    iframe.contentWindow.addStyleString = function(str) {
        style_node.innerHTML = str;
        iframe.contentDocument.head.appendChild(style_node);
    }

    var readonly_editor = ace.edit("rawhtml-editor");
    readonly_editor.setTheme("ace/theme/twilight");
    readonly_editor.session.setMode("ace/mode/html");
    readonly_editor.setOptions({
            readOnly: true
    });
}
