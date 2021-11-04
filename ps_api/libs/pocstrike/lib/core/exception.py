from http.client import HTTPException


class PocstrikeBaseException(Exception):
    pass


class PocstrikeUserQuitException(PocstrikeBaseException):
    pass


class PocstrikeShellQuitException(PocstrikeBaseException):
    pass


class PocstrikeDataException(PocstrikeBaseException):
    pass


class PocstrikeGenericException(PocstrikeBaseException):
    pass


class PocstrikeSystemException(PocstrikeBaseException):
    pass


class PocstrikeFilePathException(PocstrikeBaseException):
    pass


class PocstrikeConnectionException(PocstrikeBaseException):
    pass


class PocstrikeThreadException(PocstrikeBaseException):
    pass


class PocstrikeValueException(PocstrikeBaseException):
    pass


class PocstrikeMissingPrivileges(PocstrikeBaseException):
    pass


class PocstrikeSyntaxException(PocstrikeBaseException):
    pass


class PocstrikeValidationException(PocstrikeBaseException):
    pass


class PocstrikeMissingMandatoryOptionException(PocstrikeBaseException):
    pass


class PocstrikePluginBaseException(PocstrikeBaseException):
    pass


class PocstrikePluginDorkException(PocstrikePluginBaseException):
    pass


class PocstrikeHeaderTypeException(PocstrikeBaseException):
    pass

class PocstrikeIncompleteRead(HTTPException):
    def __init__(self, partial, expected=None):
        self.args = partial,
        self.partial = partial
        self.expected = expected
    def __repr__(self):
        if self.expected is not None:
            e = ', %i more expected' % self.expected
        else:
            e = ''
        return '%s(%i bytes read%s)' % (self.__class__.__name__,
                                        len(self.partial), e)
    def __str__(self):
        return repr(self)