HTML=doc/_build/html

rsync $HTML/*.html .
rsync $HTML/objects.inv .
rsync $HTML/searchindex.js .
rsync _sources/ .
rsync  _static/ .
rsync _modules/ .
rsync-r generated/ .


