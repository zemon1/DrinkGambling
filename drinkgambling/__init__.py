from models import initialize_sql
from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from .models import DBSession, Base

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    initialize_sql(engine)
    
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('deal', '/deal')
    config.add_route('hit', '/hit')
    config.add_route('stand', '/stand')
    config.scan()
    return config.make_wsgi_app()
