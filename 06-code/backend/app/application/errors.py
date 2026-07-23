class DuplicateEmail(Exception):
    pass


class DatabaseUnavailable(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class InvalidAccessToken(Exception):
    pass


class AuthenticatedUserNotFound(Exception):
    pass


class InvalidPagination(Exception):
    pass


class ExternalOpportunitySourceUnavailable(Exception):
    pass
