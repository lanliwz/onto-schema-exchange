from gojs_models.ft.gogs_ft_person_shape import PersonShapeComponents
from gojs_models.ft.gojs_ft_template import TemplateComponents
from gojs_models.ft.gojs_ft_theme_manager import *

def stream_data_js() -> str:
    return """
const socket = new WebSocket("ws://localhost:8000/ws");
const model_data_file = "/Users/weizhang/Downloads/ft_model_data.json"
socket.onmessage = function(event) {
    if (event.data === "__connected__") {
    socket.send(model_data_file);
    }
    if (event.data === "__ping__") {
    socket.send("__pong__");
    return;
    }
    try {
        myDiagram.model = go.Model.fromJson(event.data);
        } 
    catch (err) {
        console.error("Invalid diagram JSON:", err);
        }
};
socket.onclose = function() {
    console.log("Connection closed");
};
    """

def init_diagram():
    handlers = PartEventHandlers()
    templates = TemplateComponents()
    person_shapes = PersonShapeComponents()

    return f"""function init_diagram() {{
{handlers.to_javascript()}
{person_shapes.to_javascript()}
{templates.to_javascript()}
{stream_data_js()}
}};"""

