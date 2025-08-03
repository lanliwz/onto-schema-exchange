from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Callable


class ColorTheme(BaseModel):
    pink: str
    blue: str
    green: str
    yellow: str
    background: str


class DiagramConfig(BaseModel):
    div_id: str = "myDiagramDiv"
    diagram_var: str = "myDiagram"
    colors: ColorTheme = ColorTheme(
        pink="#facbcb",
        blue="#b7d8f7",
        green="#b9e1c8",
        yellow="#faeb98",
        background="#e8e8e8"
    )
    colors_dark: ColorTheme = ColorTheme(
        green="#3fab76",
        yellow="#f4d90a",
        blue="#0091ff",
        pink="#e65257",
        background="#161616"
    )

    def create_diagram_js(self) -> str:
        return f"""
        var {self.diagram_var} = new go.Diagram("{self.div_id}", {{
            'animationManager.initialAnimationStyle': go.AnimationStyle.None,
            InitialAnimationStarting: (e) => {{
                var animation = e.subject.defaultAnimation;
                animation.easing = go.Animation.EaseOutExpo;
                animation.duration = 800;
                animation.add(e.diagram, 'scale', 0.3, 1);
                animation.add(e.diagram, 'opacity', 0, 1);
            }},
            'toolManager.mouseWheelBehavior': go.WheelMode.Zoom,
            'clickCreatingTool.archetypeNodeData': {{ text: 'new node' }},
            'undoManager.isEnabled': true
        }});
        {self.diagram_var}.div.style.backgroundColor = "{self.colors.background}";
        """

    def add_modified_listener_js(self) -> str:
        return f"""
        {self.diagram_var}.addDiagramListener("Modified", (e) => {{
            var button = document.getElementById("SaveButton");
            if (button) button.disabled = !{self.diagram_var}.isModified;
            var idx = document.title.indexOf("*");
            if ({self.diagram_var}.isModified) {{
                if (idx < 0) document.title += "*";
            }} else {{
                if (idx >= 0) document.title = document.title.slice(0, idx);
            }}
        }});
        """

    def define_node_template_js(self) -> str:
        return f"""
        {self.diagram_var}.nodeTemplate = new go.Node("Auto", {{
            isShadowed: true,
            shadowBlur: 0,
            shadowOffset: new go.Point(5, 5),
            shadowColor: "black"
        }})
        .bindTwoWay("location", "loc", go.Point.parse, go.Point.stringify)
        .add(
            new go.Shape("RoundedRectangle", {{
                strokeWidth: 1.5,
                fill: "{self.colors.blue}",
                portId: "",
                fromLinkable: true, fromLinkableSelfNode: false, fromLinkableDuplicates: true,
                toLinkable: true, toLinkableSelfNode: false, toLinkableDuplicates: true,
                cursor: "pointer"
            }})
            .bind("fill", "type", (type) => {{
                if (type === "Start") return "{self.colors.green}";
                if (type === "End") return "{self.colors.pink}";
                return "{self.colors.blue}";
            }})
            .bind("figure", "type", (type) => {{
                if (type === "Start" || type === "End") return "Circle";
                return "RoundedRectangle";
            }}),
            new go.TextBlock({{
                font: "bold 14px sans-serif",
                stroke: "#333",
                margin: 8,
                editable: true
            }}).bindTwoWay("text")
        );
        """

    def define_selection_adornment_js(self) -> str:
        return f"""
        {self.diagram_var}.nodeTemplate.selectionAdornmentTemplate = new go.Adornment("Spot")
        .add(
            new go.Panel("Auto")
            .add(
                new go.Shape("RoundedRectangle", {{ fill: null, stroke: "{self.colors.pink}", strokeWidth: 3 }}),
                new go.Placeholder()
            ),
            go.GraphObject.build("Button", {{
                alignment: go.Spot.TopRight,
                click: addNodeAndLink
            }}).add(
                new go.Shape("PlusLine", {{ width: 6, height: 6 }})
            )
        );
        """

    def define_add_node_and_link_js(self) -> str:
        return """
        function addNodeAndLink(e, obj) {
            var adornment = obj.part;
            var diagram = e.diagram;
            diagram.startTransaction("Add State");

            var fromNode = adornment.adornedPart;
            var fromData = fromNode.data;
            var toData = { text: "new" };
            var p = fromNode.location.copy();
            p.x += 200;
            toData.loc = go.Point.stringify(p);

            var model = diagram.model;
            model.addNodeData(toData);

            var linkdata = {
                from: model.getKeyForNodeData(fromData),
                to: model.getKeyForNodeData(toData),
                text: "transition"
            };
            model.addLinkData(linkdata);

            var newnode = diagram.findNodeForData(toData);
            diagram.select(newnode);
            diagram.commitTransaction("Add State");
            diagram.scrollToRect(newnode.actualBounds);
        }
        """

    def define_link_template_js(self) -> str:
        return f"""
        {self.diagram_var}.linkTemplate = new go.Link({{
            isShadowed: true,
            shadowBlur: 0,
            shadowColor: "black",
            shadowOffset: new go.Point(2.5, 2.5),
            curve: go.Curve.Bezier,
            curviness: 40,
            adjusting: go.LinkAdjusting.Stretch,
            reshapable: true,
            relinkableFrom: true,
            relinkableTo: true,
            fromShortLength: 8,
            toShortLength: 10
        }})
        .bindTwoWay("points")
        .bind("curviness")
        .add(
            new go.Shape({{ strokeWidth: 2, stroke: "black" }})
                .bind("strokeDashArray", "progress", (progress) => progress ? [] : [5, 6])
                .bind("opacity", "progress", (progress) => progress ? 1 : 0.5),
            new go.Shape({{ fromArrow: "circle", strokeWidth: 1.5, fill: "white" }})
                .bind("opacity", "progress", (progress) => progress ? 1 : 0.5),
            new go.Shape({{ toArrow: "standard", scale: 1.5, fill: "black" }})
                .bind("opacity", "progress", (progress) => progress ? 1 : 0.5),
            new go.Panel("Auto")
                .add(
                    new go.Shape("RoundedRectangle", {{
                        fill: "{self.colors.yellow}",
                        strokeWidth: 0.5
                    }}),
                    new go.TextBlock({{
                        font: "9pt helvetica, arial, sans-serif",
                        margin: 1,
                        editable: true,
                        text: "Action"
                    }}).bind("text")
                )
        );
        """

    def init_diagram(self) -> str:
        return (
            self.create_diagram_js()
            + self.add_modified_listener_js()
            + self.define_node_template_js()
            + self.define_selection_adornment_js()
            + self.define_add_node_and_link_js()
            + self.define_link_template_js()
        )

def stream_data_js() -> str:
    diagram = DiagramConfig()
    return f"""
const socket = new WebSocket("ws://localhost:8000/ws");
const model_data_file = "/Users/weizhang/Downloads/wf_model_data.json"
socket.onmessage = function(event) {{
    if (event.data === "__connected__") {{
    socket.send(model_data_file);
    }}
    if (event.data === "__ping__") {{
    socket.send("__pong__");
    return;
    }}
    try {{
        {diagram.diagram_var}.model = go.Model.fromJson(event.data);
        }} 
    catch (err) {{
        console.error("Invalid diagram JSON:", err);
        }}
}};
socket.onclose = function() {{
    console.log("Connection closed");
}};
"""

def init_diagram():
    wf_diagram = DiagramConfig()
    return f"""function init_diagram() {{
{wf_diagram.init_diagram()}
{stream_data_js()}
}};"""