from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from settings import settings


engine = create_engine(settings['ENGINE'])
Session = sessionmaker(bind=engine)


class SessionScope(object):
    """Content manager that creates sessions."""
    def __init__(self):
        """Create a session."""
        self._session = Session()
    def __enter__(self):
        """Return the session."""
        return self._session
    def __exit__(self, e_type, e_value, trace):
        """Commit or roll back, then do cleanup."""
        if e_type is not None:
            # Exception occured
            self._session.rollback()
        else:
            self._session.commit()
            self._session.close()


def get_or_create(session, model, create_method='',
                  create_method_kwargs=None, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one(), False
    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created, True
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), True
