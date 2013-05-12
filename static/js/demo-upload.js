// glue between rascal.dnd and rascal.upload
// generic upload progress, status and completion functions
// JSLint 6 Oct 2012 jQuery $ rascal {}
// Updated 16 Apr 2013 dsmall for rascal-1.04
/*global $, rascal */

// Assumes element id="progress", sets bg position and initially makes opaque
function uploadProgress(pc) {
    "use strict";
    $('#progress').css('background-position', (100 - pc) + '% 0');
    if (pc === 0) {
        $('#progress').css('opacity', 1);
    }
}

// Assumes element id="status" and appends messages
function uploadStatus(msg) {
    "use strict";
    $('#status').html($('#status').html() + msg + '<br />');
}

// Hide progress bar, call a completion function
function uploadComplete() {
    "use strict";
    $('#progress').fadeTo(2000, 0);
    rascal.directory.listDirectory();
}

// Glue that enables rascal.dnd to upload files
// Sets file types that can be uploaded
// Connects progress, status and completion functions
// Removes all messages from status
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
