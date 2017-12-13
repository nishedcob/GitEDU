
import jwt


def validate_repospec(repospec):
    # TODO: Find RepoSpec in DB
    # TODO: Validate all fields, raise error if something doesn't checkout
    pass


def decode(repospec):
    # TODO: extract repospec data and return it as a dictionary
    pass


def encode(parent, repo):
    # TODO: Create new repospec and save it to the DB
    # TODO: Return new repospec
    pass
