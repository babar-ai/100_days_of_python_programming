"""
How Custom Logging Fixes Problems discussed in tut1.py

By creating a custom logger (like your get_logger() function):
Logs include timestamps, module names, and severity levels
Logs can be sent to files, console, or remote servers
Each module can have its own logger name and level
You can format logs consistently
Can be centralied for entire project, making debugging and monitoring much easier

"""

import logging
from logging.handlers import RotatingFileHandler               # In Python’s logging module, a Handler is a component that decides where your log messages go. RotatingFileHandler is a special file handler that automatically creates a new log file when the current one reaches a certain size.

# Logging flow →
# Logger → Handler → Formatter → Output     

def setup_logger(name: str = None):


    if name is None:
        name = __name__  # Use caller's module name  # Built-in variable that stores module’s name
    
    logger = logging.getLogger(name)           # Using logging.getLogger(name) with a meaningful name like "ingest" or "document_loader" creates a named logger hierarchy:

    '''root
         └── ingest
         └── document_loader
         └── api.routes
    '''
 

    # 1: Prevent duplicate handler
    if logger.handlers:
        return logger
    

    logger.setLevel(logging.INFO)                              # means: “Ignore everything below INFO — only log INFO, WARNING, ERROR, and CRITICAL messages.”
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # : Add rotation (5MB max, 3 backups)
    file_handler = RotatingFileHandler(                  # RotatingFileHandler to manage log file size and backups
        "automation.log",      
        maxBytes=5*1024*1024,              # file size
        backupCount=3,
        encoding="utf-8"
    )

    '''
    3. RotatingFileHandler (5MB max, 3 backups)
Without rotation, log files grow forever. RotatingFileHandler solves this:

automation.log       ← Current log (max 5MB)
automation.log.1     ← Previous file (backup 1)
automation.log.2     ← Older backup
automation.log.3     ← Oldest backup (after this, .1 is deleted)
    '''
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    

    return logger
