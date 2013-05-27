from flask import Blueprint, render_template, request
public = Blueprint('lib_notes', __name__, template_folder='templates')

from werkzeug import secure_filename
from server import ROOT, EDITOR

@public.route('/notes.html')
def notes():
    return render_template('/notes.html', editor=EDITOR)

@public.route('/note_read',  methods=['POST'])
def note_read():
    try:
        fdir = request.form['fdir']
        fname = request.form['fname']
        f = open(ROOT + fdir + fname, 'r')
        return f.read()
    except Exception, e:
        print '## note_read ## Unexpected error: %s' % str(e)
        return 'Not Found', 404

@public.route('/note_write', methods=['POST'])
def note_write():
    import os, shutil
    try:
        fdir = request.form['fdir']
        if not os.path.exists(ROOT + fdir):
            os.makedirs(ROOT + fdir)
        fname = request.form['fname']
        s = request.form['text']
        nameFromText = ''
        # Get first valid name
        for line in s.splitlines():
            nameFromText = secure_filename(line.strip())
            if nameFromText != '':
                nameFromText += '.md'
                break
        if nameFromText == '' and fname == '':
            return ''
        elif nameFromText == '':
            os.remove(ROOT + fdir + fname)
            return ''
        elif fname not in ['', nameFromText]:
            shutil.move(ROOT + fdir + fname, ROOT + fdir + nameFromText)
        fname = nameFromText
        f = open(ROOT + fdir + fname, 'w')
        f.write(s)
        f.close()
        return fname
    except Exception, e:
        print '## note_write ## Unexpected error: %s' % str(e)
        return 'Bad Request', 400
