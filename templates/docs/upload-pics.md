Upload - Pictures 
---------------

This is the third of the examples that use the _rascal.js_ object to upload files.
It builds on the previous example [Upload using Drag and Drop][upload-dd] and adds
three new features:

* The directory list is formatted and clickable
* Clicking an image file scales and displays it
* The filelist and picture frame adjust to the size of the browser window

Only the new features will be described here.

#### File list
Here the file list container is also the drop zone with a `.dragover` class and an upload progress bar
implemented using Bootstrap. The list is an HTML `UL` element, built automatically by setting properties of
`rascal.directory`:

    rascal.directory.prefix = '<ul class="files">';
    rascal.directory.transform = list_transform;
    rascal.directory.delimiter = '';
    rascal.directory.suffix = '</ul>';
    
    // Transform a filename into a list element with a link
    function list_transform(filename) {
    return '<li class="file"><a href="#" rel="' + filename + '">' + filename + '</a></li>';
    }
    
Event handlers delegated to the file list container provide highlighting of file names on mouseover and
click handling.

#### ShowPicture
Scaling the picture to its container and displaying it is handled by `rascal.picture`. The containers
for the picture and caption are set up in the `$(document).ready` function:

    // Initialise rascal.picture
    rascal.picture.containerID = 'frame-p';
    rascal.picture.captionID = 'caption-p';

When a file name is clicked, the event handler calls `showPicture` with the filename and
`rascal.picture` scales and displays the image and updates the caption:

    function showPicture(file) {
        "use strict";
        rascal.picture.show(rascal.directory.directory + file);
    }

#### Resizing
Bootstrap classes `.container-fluid` and `.row-fluid` automatically adjust their width
to the size of the browser window but we have to deal with changes in height. The `$(document).ready`
function sets up an event handler for `$(window).resize` with a 0.5s delay to avoid jitter:

    $(window).resize(function () {
        delay(function () {
            adjustGeometry();
        }, 500);
    });

The function `adjustGeometry` is responsible for adjusting the height of the file list and picture
frame, calling `rascal.picture.resize` to rescale the picture to the new frame size:

    function adjustGeometry() {
        "use strict";
        var h, dh;
        if (ADJUSTSIZE) {
            h = $(window).height();
            dh = (h > (440 + XH)) ? h - (440 + XH) : 0;
            $('#filelist').height(440 + dh);
            $('#frame-p').height($('#filelist-well').height()-$('#caption-p').height());
            if (rascal.picture.showing) {
                rascal.picture.resize();
            }
        }
    }

The next example in this series is [Album][album].

More information about _rascal.js_ can be found [here][rascal_object].

<small>dsmall 18 May 2013</small>

[upload-dd]: /upload-dd.html
[album]: /album.html
[rascal_object]: /docs/Rascal_Object.md
