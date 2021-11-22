import dash
import dash_bootstrap_components as dbc
# from flask_caching import Cache  # for cache of .targets or .scores

URL = ''

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

# app = dash.Dash(__name__, suppress_callback_exceptions=True)
# server = app.server
# CACHE_CONFIG = {
#     # try 'filesystem' if you don't want to setup redis
#     'CACHE_TYPE': 'filesystem',
#     'CACHE_DIR': ('Cache')  # os.environ.get('REDIS_URL', 'localhost:6379')
# }
# cache = Cache()
# cache.init_app(app.server, config=CACHE_CONFIG)
