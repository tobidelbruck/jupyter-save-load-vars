# saveload vars

import dill
import logging

import logging
# general logger. Produces nice output format with live hyperlinks for pycharm users
# to use it, just call log=get_logger() at the top of your python file
# all these loggers share the same logger name 'NE1'

_LOGGING_LEVEL = logging.DEBUG # usually INFO is good

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""
    # see https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output/7995762#7995762

    # \x1b[ (ESC[) is the CSI introductory sequence for ANSI https://en.wikipedia.org/wiki/ANSI_escape_code
    # The control sequence CSI n m, named Select Graphic Rendition (SGR), sets display attributes.
    grey = "\x1b[2;37m" # 2 faint, 37 gray
    yellow = "\x1b[33;21m"
    cyan = "\x1b[0;36m" # 0 normal 36 cyan
    green = "\x1b[31;21m" # dark green
    red = "\x1b[31;21m" # bold red
    bold_red = "\x1b[31;1m"
    light_blue = "\x1b[1;36m"
    blue = "\x1b[1;34m"
    reset = "\x1b[0m"
    # File "{file}", line {max(line, 1)}'.replace("\\", "/")
    format = '[%(levelname)s]: %(asctime)s - %(name)s - %(message)s (File "%(pathname)s", line %(lineno)d, in %(funcName)s)'

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: cyan + format + reset,
        logging.WARNING: red + format + reset,
        logging.ERROR: bold_red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record).replace("\\", "/") #replace \ with / for pycharm links


def get_logger():
    """ Use get_logger to define a logger with useful color output and info and warning turned on according to the global LOGGING_LEVEL.

    :returns: the logger.
    """
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger('saveloadvars') # tobi changed so all have same name so we can uniformly affect all of them
    logger.setLevel(_LOGGING_LEVEL)
    # create console handler if this logger does not have handler yet
    if len(logger.handlers)==0:
        ch = logging.StreamHandler()
        ch.setFormatter(CustomFormatter())
        logger.addHandler(ch)
    return logger

log=get_logger()

# https://stackoverflow.com/questions/6618795/get-locals-from-calling-namespace-in-python
import inspect

def printvars():
    """ prints local variables, similar to %who in ipython jupyter notebook"""
    from types import ModuleType
    tmp=None
    frame = inspect.currentframe().f_back
    try:
        tmp = frame.f_locals
    finally:
        del frame
    if tmp is None: return
    print('variables: ',end='')
    for k,v in tmp.items():
        if k.startswith('_') or k=='tmp' or k=='In' or k=='Out' or hasattr(v, '__call__') or isinstance(v,ModuleType) or isinstance(v,logging.Logger):
            continue
        print(k, end=',')
    print('')

_DILL='.dill'

def savevars(filename):
    """
    saves all local variables to a file with dill
    
    :param filename: the name of the file. The suffix .dill is added if there is not a suffix already.
    """
    if filename is None:
        log.error('you must supply a filename')
        return
    from pathlib import Path
    p=Path(filename)
    if p.suffix=='': # if suffix is missing add .dill
        p = p.parent / (p.name + _DILL)

    import inspect,dill
    locals=None
    frame = inspect.currentframe().f_back
    try:
        locals = frame.f_locals
    finally:
        del frame
    if locals is None: return

    data={}
    could_not_pickle=[]

    from types import ModuleType
    s=f'saved to {p} variables [ '
    for k,v in locals.items():
        # don't try to pickle any pyplane objects
        if k.startswith('_') or (isinstance(v,str) and (k=='tmp' or k=='In' or k=='Out')) or hasattr(v, '__call__') \
            or isinstance(v,ModuleType) or isinstance(v,logging.Logger): 
            continue
        try:
            if not dill.pickles(v):
                could_not_pickle.append(k)
                continue
        except:
            could_not_pickle.append(k)
            continue
        s=s+k+' '
        data[k]=v
    s=s+']'
    try:
       with open(p,'wb') as f:
            try:
                dill.dump(data,f)
                log.info(f'{s}')
                if len(could_not_pickle)>0:
                    log.warning(f'could not pickle: {could_not_pickle}')
            except TypeError as e:
                log.error(f'\n Error: {e}')
    except Exception as e:
        log.error(f'could not save data to {p}')

def loadvars(filename, overwrite='prompt'):
    """ Loads variables from file into the current workspace
    This function loads the variables found in filename into the parent workspace.
    
    :param filename: the dill file to load from, e.g. lab1. The suffix .dill is added automatically unless there is already a suffix.
    :param overwrite: 'prompt' (default) asks to overwrite, 'no' does not overwrite, 'yes' overwrites silently

    :raises: Exception if it cannot load for any reason except not being able to overwrite particular variables.
    """
    if not ( overwrite=='yes' or overwrite=='no' or overwrite=='prompt' ):
        raise ValueError(f'overwrite={overwrite} is invalid, must be "yes" "no" or "prompt"')
    import dill
    from pathlib import Path
    p=Path(filename)
    if p.suffix=='': # if suffix is missing add .dill
        p = p.parent / (p.name + _DILL)
    if not p.exists:
        raise FileNotFoundError(f'{p} does not exist')
    did_not_overwrite=[]
    overwrote=[]
    try:
        with open(p,'rb') as f:
            data=dill.load(f)
            log.info(f'from {p} loaded variables {list(data.keys())}')
            import inspect
            try:
                frame = inspect.currentframe().f_back # get the workspace frame (jupyter workspace frame)
                locals = frame.f_locals # get its local variable dict
                always=False
                for k in data:
                    try:
                        if k in locals.keys(): # if variable exists
                            if overwrite=='yes' or always:
                                # if always overwrite (yes) or prompt returns True
                                locals[k] = data[k] # set a value in it
                                overwrote.append(k)
                            elif overwrite=='prompt':
                                resp=_yes_or_no_or_always(f'Overwrite existing variable "{k}" ?')
                                if resp=='always':
                                    always=True
                                    locals[k] = data[k] # set a value in it
                                    overwrote.append(k)
                                elif resp=='yes':
                                    locals[k] = data[k] # set a value in it
                                    overwrote.append(k)
                                else:
                                    did_not_overwrite.append(k)
                            else:
                                did_not_overwrite.append(k)
                        else:
                            locals[k] = data[k] # set a value in it
                    except Exception as e:
                        log.error(f'could not set variable {k}: got {e}')
            finally:
                del frame
            # didnt_overwrite_str=' '.join(did_not_overwrite)
            if len(overwrote)>0:
                log.info(f'overwrote existing variables {overwrote}')
            if len(did_not_overwrite)>0:
                log.info(f'did not overwrite existing variables {did_not_overwrite}')
            
    except Exception as e:
        raise Exception(f'could not load; got {e}')

# useful utilies to ask question at console terminal with default answer and timeout

import signal
import time

def _alarm_handler(signum, frame):
    raise TimeoutError
def _input_with_timeout(prompt, timeout=30):
    """ get input with timeout

    :param prompt: the prompt to print
    :param timeout: timeout in seconds, or None to disable

    :returns: the input
    :raises: TimeoutError if times out
    """
    # set signal handler
    if timeout is not None:
        signal.signal(signal.SIGALRM, _alarm_handler)
        signal.alarm(timeout) # produce SIGALRM in `timeout` seconds
    try:
        time.sleep(.5) # get input to be printed after logging
        return input(prompt)
    except TimeoutError as to:
        raise to
    finally:
        if timeout is not None:
            signal.alarm(0) # cancel alarm

import os
def _yes_or_no_or_always(question, default='y', timeout=None):
    """ Get Yes/No/Always answer with default choice and optional timeout

    :param question: prompt
    :param default: the default choice, i.e. 'y' or 'n' or 'a'
    :param timeout: the timeout in seconds, default is None

    :returns: 'yes' or 'no' or 'always'
    """
    if default is not None and (default!='y' and default!='n'):
        raise ValueError(f'bad option for default: {default}; must be "y" or "n")')
    yes='Yes' if default=='y' else 'yes'
    no='No' if default=='n' else 'no'
    always='always'
    while "the answer is invalid":
        try:
            to_str='' if timeout is None or os.name=='nt' else f'(Timeout {default} in {timeout}s)'
            if not timeout is None and os.name=='nt':
                log.warning('cannot use timeout signal on windows')
                time.sleep(.1) # make the warning come out first
                reply=str(input(f'{question} {to_str} ({yes}/{no}/{always}): ')).lower().strip()
            else:
                reply = str(_input_with_timeout(f'{question} {to_str} ({yes}/{no}/{always}): ', timeout=timeout)).lower().strip()
        except TimeoutError:
            log.warning(f'timeout expired, returning default={default} answer')
            reply=''
        if len(reply)==0 or reply=='':
            return yes.lower() if default=='y' else no.lower()
        elif reply[0].lower() == 'y':
            return yes.lower()
        elif reply[0].lower() == 'n':
            return no.lower()
        elif reply[0].lower()=='a':
            return always.lower()

