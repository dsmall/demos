## Rascal on demos/red ##

### red status Apr 22 2013

##### CHANGES IN A NUTSHELL

* Support for C, Ruby and JSON modes
* Create Python template
* __init__.py now imports editor.py
* Single point of config in editor.py for RASCAL, MAC and WINDOWS (just change value of env)
* Editor page has tooltips on icons
* Editor page title includes file being edited
* Can use meta-click on file in file tree or location bar to display as page (varies with browser)
* Save file now uses XMLHttpRequest with true progress (requires rascal-1.04.js)
* Supports CM v3.0 (but not yet later versions)
* Rename file now has Copy file option
* Cmd-J in JSON document prettifies it
* Cmd-/ toggles comments (supports HTML, CSS, Javascript and Python)
* Minor bug fixes

##### SUBJECT TO CHANGE
There are some changes to disallow spaces in names. I've had second thoughts and expect to roll these back

### demos status Apr 22 2013

##### CHANGES INCLUDE

* General changes to make clicking the rascal micro logo move between editor and public work on all environments
* Home page shows uptime
* rascal-1.04.js (needs documentation)
* Updated versions of upload-cf, upload-dd and album (documentation in progress)
* New demo upload-pics
* email demo now a blueprint based on libsmtp
* Works on iPad

--
