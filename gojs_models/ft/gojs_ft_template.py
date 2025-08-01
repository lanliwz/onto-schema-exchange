from pydantic import BaseModel

class NodeTemplate(BaseModel):
    def to_javascript(self) -> str:
        return """const createNodeTemplate = () =>
  new go.Node('Spot', {
    selectionAdorned: false,
    mouseEnter: onMouseEnterPart,
    mouseLeave: onMouseLeavePart,
    selectionChanged: onSelectionChange
  })
    .add(
      new go.Panel('Spot')
        .add(
          personMainShape(),
          personNameTextBlock(),
          personBirthDeathTextBlock()
        ),
      personImage(),
      personBadge(),
      personCounter()
    );"""

class LinkTemplate(BaseModel):
    def to_javascript(self) -> str:
        return """const createLinkTemplate = () =>
  new go.Link({
    selectionAdorned: false,
    routing: go.Routing.Orthogonal,
    layerName: 'Background',
    mouseEnter: onMouseEnterPart,
    mouseLeave: onMouseLeavePart
  })
    .add(
      new go.Shape({
        stroke: theme.colors.link,
        strokeWidth: 1
      })
        .bindObject('stroke', 'isHighlighted', (isHighlighted) =>
          isHighlighted ? theme.colors.selectionStroke : theme.colors.link
        )
        .bindObject('stroke', 'isSelected', (selected) =>
          selected ? theme.colors.selectionStroke : theme.colors.link
        )
        .bindObject('strokeWidth', 'isSelected', (selected) => selected ? 2 : 1)
    );"""

class DiagramConfig(BaseModel):
    root_key: str = 'King George V'  # configurable!
    diagram_div: str = "myDiagramDiv"

    def to_javascript(self) -> str:
        return f"""
const myDiagram = new go.Diagram('{self.diagram_div}', {{
      layout: new go.TreeLayout({{
      angle: 90,
      nodeSpacing: 20,
      layerSpacing: 50,
      layerStyle: go.TreeLayout.LayerUniform,
      treeStyle: go.TreeStyle.LastParents,
      alternateAngle: 90,
      alternateLayerSpacing: 35,
      alternateAlignment: go.TreeAlignment.BottomRightBus,
      alternateNodeSpacing: 20
    }}),
    'toolManager.hoverDelay': 100,
    linkTemplate: createLinkTemplate(),
    model: new go.TreeModel({{ nodeKeyProperty: 'name' }})
}});

myDiagram.nodeTemplate = createNodeTemplate();
const nodes = familyData;
myDiagram.model.addNodeDataCollection(nodes);

myDiagram.addDiagramListener('InitialLayoutCompleted', () => {{
const root = myDiagram.findNodeForKey('{self.root_key}');
if (!root) return;
myDiagram.scale = 0.6;
myDiagram.scrollToRect(root.actualBounds);
}});

document.getElementById('zoomToFit').addEventListener('click', () => diagram.commandHandler.zoomToFit());
document.getElementById('centerRoot').addEventListener('click', () => {{
myDiagram.scale = 1;
myDiagram.commandHandler.scrollToPart(diagram.findNodeForKey('{self.root_key}'));
}});"""

class TemplateComponents(BaseModel):
    create_node_template: NodeTemplate = NodeTemplate()
    create_link_template: LinkTemplate = LinkTemplate()
    configuration: DiagramConfig = DiagramConfig()

    def to_javascript(self) -> str:
        return '\n\n'.join([
            self.create_node_template.to_javascript(),
            self.create_link_template.to_javascript(),
            self.configuration.to_javascript()
        ])