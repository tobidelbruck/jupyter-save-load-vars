# jupyter-save-load-vars change log

## 0.3.0
## New features
* Add unix wildcard capability for _vars_ argument, e.g. `savevars('file','v_*')` will save all variables starting with 'v_'
* Add noarg invovation for default filename
* Add True='yes' and False='no' argument options

### Bug fixes
* Reorder the file overwrite to come after we know we want to save variables
* Check we have variables before checking if file needs to be overwritten
* Add pytest capability
* Rename test file to be `test_jupyter_save_load_vars.py`


## 0.2.1
### New features
* Added _vars_ argument to savevars
### Bug fixes
* Fixed _savevars_ bug that saved _In_ and _Out_ variables
* Fixed yes/no/always questions to be yes/no when always not appropriate

## 0.1.0
Initial release
