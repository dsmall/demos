About Notes
----------

--

* Click the `+` button to start a new note
* Type a title on the first line
* Type the rest of the note as plain text, or use [Markdown][mwp]
* Click `View` to see a note in the browser, or shift-click it in the file list
* To delete a note, just delete its contents

--

<small>Notes was built from [Upload Pictures][upics] and [CodeMirror][cm],
with read write support in `lib_notes.py`.
No skeuomorphs were harmed during the making of this application.</small>

[mwp]: /docs/about-docs.md
[upics]: /upload-pics.html
[cm]: http://codemirror.net/

<script type="text/javascript">
    $(document).ready(function () {
		$('#doc-content li')
            .css('list-style-type', 'circle')
        	.css('margin-bottom', '10px');
        $('#doc-content a')
            .attr('target', '_blank');
    });
</script>
