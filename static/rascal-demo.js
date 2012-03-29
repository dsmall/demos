// glue between rascal.dnd and rascal.upload
// generic upload progress, status and completion functions

// Assumes element id="progress", sets bg position and initially makes opaque
function uploadProgress(pc) {
    $('#progress').css('background-position', pc + '% 0');
    if (pc === 100) {
        $('#progress').css('opacity', 1);
    }
}

// Assumes element id="status" and appends messages
function uploadStatus (msg) {
    $('#status').html($('#status').html() + msg + '<br />');
}

// Hide progress bar, call a completion function
function uploadComplete() {
    $('#progress').fadeTo(2000, 0);
    rascal.directory.listDirectory();
}

// Glue that enables rascal.dnd to upload files
// Sets file types that can be uploaded
// Connects progress, status and completion functions
// Removes all messages from status
function uploadItems(files, dst) {
    var ru = rascal.upload;
    // set up allowed types, progress, status and complete
    ru.allowedTypes = [ 'image/' ];
    ru.progress = uploadProgress;
    ru.status = uploadStatus;
    ru.complete = uploadComplete;
    $('#status').empty();
    ru.filesDropped(files, dst);
}
