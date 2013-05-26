Rascal Object
============

The Rascal object consists of four objects that perform related functions:

||**Object**||**Supports**||
||rascal.dnd||HTML5 drag and drop||
||rascal.upload||Uploads one or more files||
||rascal.directory||Lists or clears a directory||
||rascal.picture||Scales and displays a picture||

`rascal` is used both by the Rascal editor and by public templates. Some demos are provided.

### rascal.dnd

Given the ID of a drop zone container, rascal.dnd sets up event listeners for `dragover`, `drop` and `dragleave` events. A secondary function, used only by the Rascal editor, extends `jquery.filetree` to support drag and drop.

The function of the `dragover` event handler is to add class `dragover` to the drop zone container or its children with tag `a`. You can see this in action when you drag a file over the Rascal editor's file tree. Either the top level container "lights up" with a blue glowing margin or the directory names become highlighted, in either case indicating the destination of dropped items. This class is removed by the `drop` and `dragleave` handlers.

The `drop` event handler supports three scenarios:

1. One or more files dragged from the desktop has been dropped onto the drop zone or one of its children.
2. One or more files has been selected with an `input` element of type file.
3. A file or folder has been dragged from another location in the Rascal editor file tree onto the drop zone or one of its children.

In the first two cases, which are data transfers, the handler calls the function `rascal.dnd.filesDropped` with the FileList and destination directory as arguments. In the third case, which is a file or folder move, the handler calls the function `rascal.dnd.itemDropped` with the source path and destination directory as arguments.

||**Properties**||**Type**||**Default**||**Description**||
||root||String||`/var/www/public/`||Top level directory used to construct the `dstDir` passed to call back functions itemDropped and filesDropped.||
||containerID||String||`filetree`||The id of the drop zone container||
||notDraggable||Array||`[ ]`||A list of the full paths of files or folders which cannot be dragged.||
||changedFiles||Array||`[ ]`||A list of the full paths of files which have been changed but not yet saved. This list is used to highlight the file names when the filetree is expanded.||
||itemDropped||Function||`(srcPath, dstDir)`||Callback function to move a file or folder to another directory.||
||filesDropped||Function||`(files, dstDir)`||Callback function to handle a dropped FileList. Typically, this function will initialise `rascal.upload` and then call `rascal.upload.filesDropped()`.||

||**Methods**||**Type**||**Arguments**||**Description**||
||init||Function||`()`||Sets up event handlers for `dragover`, `drop` and `dragleave` events.||
||bindTree||Function||`(branch)`||Adds drag and drop support to `jquery.filetree`.||

#### Example
This example illustrates how the demo [upload-dd][udd] initialises HTML5 drag and drop:

* `containerID` is set to `dropzone`, the id of the `div` that is to become the drop zone.
* `root` is set to `static/uploads/`, the directory on Rascal that is to receive the dropped files.
* `filesDropped` is set to the function `uploadItems` that is to be called when files are dropped.
* The function `init()` is called to set up the drag and drop event handlers.

The code to perform this initialisation can be included in the jQuery `$(document).ready` function:

    $(document).ready(function () {
        "use strict";
        // Initialise rascal.dnd 
        rascal.dnd.containerID = 'dropzone';
        rascal.dnd.root = 'static/uploads/';
        rascal.dnd.filesDropped = uploadItems;
        rascal.dnd.init();
    });

You should also define a CSS style `#dropzone.dragover` which will be used to highlight the drop zone when files are dragged over it.

The root path can be relative. In this example, the full path `/var/www/public/static/uploads` is constructed by `server.py` when the dropped files are saved. This is to protect you from accidentally overwriting the Rascal operating system. 

### rascal.upload

rascal.upload receives an HTML5 `FileList` object specifying one or more files to upload to a destination directory. The files are uploaded asynchronously to the server using an HTML5 `XMLHttpRequest` object. Callback functions can display progress, warn about errors and report completion of individual uploads and all uploads.

||**Properties**||**Type**||**Default**||**Description**||
||postURL||String||`/xupload`||Server upload URL||
||allowAll||Boolean||`false`||Allow all MIME types to be uploaded (editor only)||
||allowedTypes||Array||`[ 'image/' ]`||Allowed MIME types. This is a "begins with" match, e.g. the default value will match a file of MIME type `'image/jpeg'`.||
||allowedExtensions||Array||`[ ]`||Used when you need to allow a file type whose MIME type isn't known to the browser, e.g. Markdown files can be allowed by setting this property to `[ 'md' ]`.||
||maxFileBytes||Number||`1024 * 1024`||Maximum size of each file||
||timeout||Number||`40`||Number of seconds to wait for a file upload to finish||
||totalBytes||Number||`0`||Total bytes to be uploaded (read only)||
||savedFiles||Number||`0`||Number of files successfully uploaded (read only)||
||lastUpload||String||`''`||Filename of the last file uploaded (read only)||
||progress||Function||`(pc)`||Callback function to update a progress bar. Called with a number between 0 and 100 which is the percentage of `totalBytes` uploaded so far.||
||status||Function||`(msg)`||Callback function to display an error message, e.g. file is too large.||
||uploaded||Function||`(filename, dstDir)`||Callback function when a file has been successfully uploaded. Used by the Rascal editor Save command to remove file changed indicators.||
||complete||Function||`(dstDir)`||Callback function when all files have been uploaded. Typically, this function might remove stripes from a progress bar or perform other housekeeping.||

||**Methods**||**Type**||**Arguments**||**Description**||
||filesDropped||Function||`(files, dstDir)`||Receives one or more files in a FileList object and uploads them to a destination directory.||

#### Example
This example is the glue function used by [upload-dd][udd] to connect rascal.dnd to rascal.upload:

* Variable `ru` is set to the rascal.upload namespace. This makes subsequent accesses more efficient.
* Files whose MIME types begin with `image/` are allowed. For example, files of MIME type `image/jpeg` can be uploaded.
* Callback functions uploadProgress, uploadStatus and uploadComplete are provided. For details, please refer to [demo-upload.js][dupl].
* The function `filesDropped` is called to start the upload.

The code for the uploadItems function is:

    function uploadItems(files, dst) {
        "use strict";
        var ru = rascal.upload;
        // set up allowed types, progress, status and complete
        ru.allowedTypes = [ 'image/' ];
        ru.progress = uploadProgress;
        ru.status = uploadStatus;
        ru.complete = uploadComplete;
        ru.filesDropped(files, dst);
    }

Note that there are further checks of the file types and destination directory in the function `xupload_file` in `server.py`, checking against the constant arrays `ALLOWED_EXTENSIONS` and `ALLOWED_DIRECTORIES`. If a file or directory fails these checks, rascal.upload returns the status message `Upload of xxx failed (403 FORBIDDEN)`.

If you wish to save data using rascal.upload yourself (rather than receiving a FileList via drag and drop or an input of type file), you can construct your own FileList and File object from a `Blob`. Here's an example, where `s` is some data, `f` is a filename and `dst` is the destination directory:

    blob = new Blob([s], {type: 'text'});
    blob.name = f;
    files = { 0: blob, length: 1};
    uploadItems(files, dst);

### rascal.directory

rascal.directory provides methods to list or clear the specified directory. These methods are asynchronous so callback functions can be provided which will be called after the operation has been completed.

||**Properties**||**Type**||**Default**||**Description**||
||directory||String||`static/uploads`||Directory to list||
||listID||String||`filelist`||The id of the container that will receive the directory listing||
||prefix||String||`''`||HTML prefix to be added to the start of the directory listing||
||transform||Function||`undefined`||A function which is called for each directory item and returns a transformed version of the item, for example, embedded in an `A` tag.||
||delimiter||String||`<br/>`||A string which will be inserted between each item||
||suffix||String||`''`||HTML prefix to be added to the end of the directory listing||
||complete||Function||`()`||Callback function when the directory listing is complete||

||**Methods**||**Type**||**Arguments**||**Description**||
||listDirectory||Function||`()`||Lists the directory `rascal.directory.directory` and saves the listing in the container whose id is `rascal.directory.listID`.||
||clearDirectory||Function||`(cf)`||Clears the files in directory `rascal.directory.directory`. If callback function `cf` is specified, it will be called after the directory has been cleared.||

#### Examples
The first example shows the code used by [upload-dd][udd] for a simple directory listing:

    // Initialise rascal.directory
    rascal.directory.directory = 'static/uploads/';
    rascal.directory.listID = 'filelist';

    // Load file names from the uploads folder
    rascal.directory.listDirectory();
	
In this example, the filenames are separated by break tags `<br/>`, resulting in the names appearing as a list on separate lines.

The second example, from [upload-pics][up], shows how you can create a clickable file list. The list is is an unordered list using the `ul` tag, where each list element contains an `a` tag built by the function `transform`:

    // Initialise rascal.directory
    rascal.directory.directory = 'static/uploads/';
    rascal.directory.listID = 'filelist';
    rascal.directory.prefix = '<ul class="files">';
    rascal.directory.transform = list_transform;
    rascal.directory.delimiter = '';
    rascal.directory.suffix = '</ul>';

    function list_transform(filename) {
        return '<li class="file"><a href="#" rel="' + filename + '">' + filename + '</a></li>';
    }

The appearance of the list is customised with CSS. Delegated event handlers provide support for highlighting and clicking. For details, see the source code for [upload-pics][up].

### rascal.picture

rascal.picture scales an image to fit a target container, then centres and displays it. There are also methods to resize the current image and empty the picture container.

||**Properties**||**Type**||**Default**||**Description**||
||imgRoot||String||`'/'`||Root path. The image `src` attribute will be set to `root + fpath` ||
||containerID||String||`''`||The id of the picture container (required)||
||captionID||String||`''`||The id of the caption container (optional)||
||gap||Number||50||Minimum difference between width or height of frame and image.||
||naturalWidth||Number||0||Natural width of image (read only)||
||naturalHeight||Number||0||Natural height of image (read only)||
||showing||Boolean||false||True if a picture is being shown (read only)||

||**Methods**||**Type**||**Arguments**||**Description**||
||show||Function||`(fpath)`||Scale and display specified image in the container whose id is `rascal.picture.containerID`, optionally displaying its path and size in the container whose id is `rascal.picture.captionID` ||
||resize||Function||`()`||Resize current image (called after resizing picture container)||
||empty||Function||`()`||Empty the picture container||

#### Example
This example shows the code used by [upload-pics][up] to display a picture after clicking its filename:

    // Initialise rascal.picture
    rascal.picture.containerID = 'frame-p';
    rascal.picture.captionID = 'caption-p';

    function showPicture(file) {
        "use strict";
        rascal.picture.show(rascal.directory.directory + file);
    }

<small>dsmall 25 May 2013</small>

<script type="text/javascript">
    $(document).ready(function () {
		$('table')
        	.css('background-color', '#f8f8f8')
        	.css('margin-top', '20px')
            .addClass('table table-condensed table4');
		$('table').eq(0)
        	.removeClass('table4')
        	.width('66%');
        $('table.table4 tr > td:first-child').css('width', '15%');
        $('table.table4 tr > td:nth-child(2)').css('width', '10%');
        $('table.table4 tr > td:nth-child(3)').css('width', '18%');
        $('a').attr('target', '_blank');
    });
</script>

[udd]: /upload-dd.html
[up]: /upload-pics.html
[dupl]: /static/js/demo-upload.js

<!--
Local Variables:
markdown-extras: wiki-tables
End:
-->
