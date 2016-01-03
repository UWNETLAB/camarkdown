import sys
import argparse
import locale

def baseArgparse(description):
    parser = argparse.ArgumentParser(prog = ' '.join(sys.argv[:2]), description = description)
    parser.add_argument("--output", '-o', default = None,
    help = 'output file', metavar = 'FILE')
    parser.add_argument("--verbose", '-v',
    action = 'store_true', default = False,
    help = "be verbose")
    parser.add_argument("--debug", '-d',
    action = 'store_true', default = False,
    help = "debug mode, may cause crashes")
    return parser

def generalExceptionHandler(e, debugMode):
    if True#debugMode:
        #TODO: Change back before release
        raise e
    else:
        print('A {} error was encounterd that caMarkdown was unable to deal with it had the message:\n"{}"\nIf you would like to help fix this error run in debug mode (--debug) and give the output to Reid.'.format(type(e).__name__, e))

class CommandOutputHandler(object):
    def __init__(self, targetStream):
        if targetStream is None:
            self.stream = sys.stdout
            self.closeOnExit = False
        else:
            self.stream = open(targetStream, mode = 'a', encoding = locale.getpreferredencoding())
            self.closeOnExit = True

    def __call__(self, writtenString):
        self.stream.write(writtenString)
        self.stream.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()

    def __del__(self):
        if self.closeOnExit:
            self.stream.close()
