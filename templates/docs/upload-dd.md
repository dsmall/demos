Upload - Drag and Drop 
--------------------

This is the second of the examples that use the _rascal.js_ object to upload files
and builds on the previous example [Upload using Choose File][upload-cf].
In this demo, you use HTML5 drag and drop to drag image files from your desktop and
drop them onto the dashed box. The dropped files are uploaded and the directory listing updated.
In other respects, this demo is similar to the previous one so only the differences will be described.
For safety, the demo is restricted to uploading image files to the folder _static/uploads_.
You will need to create this folder with the editor before running the demo.
After uploading, you can view the images in [Upload Pictures][upload-pics] or the editor.

#### Drop Zone
The drop zone is a variant of class `infobox` used also for the file listing, the
addition being a CSS style `#dropzone.dragover` which causes the border to light up when
the mouse cursor is over the drop zone. Javascript initialization code executed by the
jQuery <code>$(document).ready</code> completion function sets up the drop zone:

    // Initialise rascal.dnd 
    rascal.dnd.containerID = 'dropzone';
    rascal.dnd.root = 'static/uploads/';
    rascal.dnd.filesDropped = uploadItems;
    rascal.dnd.init();

Calling the function `rascal.dnd.init()` attaches event handlers for `dragover`, `drop` and
`dragleave` to the drop zone. You can see this in action by dragging a file over the
drop zone when you should see the border lighting up.

#### Uploading
A glue function `uploadItems` connects rascal.dnd to rascal.uploads and is located in _static/js/demo-upload.js_:

    function uploadItems(files, dst) {
        "use strict";
        var ru = rascal.upload;
        // set up allowed types, progress, status and complete
        ru.allowedTypes = [ 'image/' ];
        ru.progress = uploadProgress;
        ru.status = uploadStatus;
        ru.complete = uploadComplete;
        $('#status').empty();
        ru.filesDropped(files, dst);
    }

This receives the dropped files and destination directory from rascal.upload, sets up the allowed
types and handlers for progress, status and completion (also located in _demo-upload.js_),
then passes on the files to the`rascal.upload.filesDropped` function which uploads them to
the Rascal. Experiment by dragging some image files to the drop zone. You can also try dropping
an image that is larger than the default limit (1 MB) and dropping non-image files.

The next example in this series is [Upload Pictures][upload-pics].

More information about _rascal.js_ can be found [here][rascal_object].

<small>dsmall 12 May 2013</small>

[upload-cf]: /upload-cf.html
[upload-pics]: /upload-pics.html
[rascal_object]: /docs/Rascal_Object.md

<script type="text/javascript">
    $(document).ready(function () {
        $('#doc-content a')
            .attr('target', '_blank');
    });
</script>

