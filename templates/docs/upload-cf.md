Upload - Choose File 
------------------

This is the first of several examples that use the _rascal.js_ object to upload files.
In this demo, you choose the files to upload by clicking the __Choose File__ button.
When you click __Open__ the selected files are uploaded and the directory listing updated.
For safety, the demo is restricted to uploading image files to the folder _static/uploads_.
You will need to create this folder with the editor before running the demo.
After uploading, you can view the images in [Upload Pictures][upload-pics] or the editor.

#### Input File Button
You can use an <code>&lt;input type="file"&gt;</code> button to browse for files
but it is rather ugly. This demo</a> improves the button's appearance by overlaying
a standard Rascal button:

    <span id="fileinput">
        <input id="fakefile" type="button" value="Choose File"
                class="btn btn-large btn-danger rascal" />
        <input id="file" type="file" name="file" accept="image/*" multiple="multiple" />
    </span>

The input file attributes allow you to choose one or more image files. The Rascal 
"fake" file button is overlayed using CSS:

    /* Hide real file input button behind fake button */
    #fileinput {
        position: relative;
    }
    #fakefile {
        z-index: 2;
    }
    #file {
        position: absolute;
        visibility: hidden;
        top: 0;
        left: 0;
        z-index: 1;
    }

When you click the fake file button, the click is passed on to the real file button which opens its
file selection dialogue.

#### Uploading
Javascript initialization code executed by the jQuery <code>$(document).ready</code> completion function
sets up a change handler for the real file button which uses the <code>rascal.dnd.handleDrop()</code> function
to retrieve the HTML5 file list. A glue function <code>uploadItems()</code> in _demo-upload.js_ 
sets up the progress bar and completion function, then passes the file list to <code>rascal.upload</code>. 
After the files have been uploaded, the completion function calls <code>rascal.listDirectory</code> which updates
the directory listing.

The next example in this series is [Upload using Drag and Drop][upload-dd].

More information about _rascal.js_ can be found [here][rascal_object].

<small>dsmall 19 April 2013</small>

[upload-dd]: /upload-dd.html
[upload-pics]: /upload-pics.html
[rascal_object]: /docs/Rascal_Object.md
