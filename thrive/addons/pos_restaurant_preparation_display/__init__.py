from . import models
from thrive.tools import convert

def _pos_restaurant_preparation_display_post_init(env):
    env['pos.config']._load_preparation_display_data()
