from gojs_models.ft.gogs_ft_person_shape import PersonShapeComponents
from gojs_models.ft.gojs_ft_template import TemplateComponents
from gojs_models.ft.gojs_ft_theme_manager import *

def init():

    handlers = PartEventHandlers()
    templates = TemplateComponents()
    person_shapes = PersonShapeComponents()
    return (
        handlers.to_javascript() + '\n'
        + person_shapes.to_javascript() + '\n'
        + templates.to_javascript() + '\n'
    )

