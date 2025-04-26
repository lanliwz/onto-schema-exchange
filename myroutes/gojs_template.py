from pydantic import BaseModel, Field
from typing import List, Optional

class ItemTemplate(BaseModel):
    def generate_js(self) -> str:
        return """
        const itemTempl = new go.Panel('Horizontal', { margin: new go.Margin(2, 0) })
          .add(
            new go.Shape({
              desiredSize: new go.Size(15, 15),
              strokeWidth: 0,
              margin: new go.Margin(0, 5, 0, 0)
            })
              .bind('figure')
              .themeData('fill', 'color'),
            new go.TextBlock({
              font: '14px sans-serif',
              stroke: 'black'
            })
              .bind('text', 'name')
              .bind('font', 'iskey', (k) => (k ? 'italic 14px sans-serif' : '14px sans-serif'))
              .theme('stroke', 'text')
          );
        """

class NodeTemplate(BaseModel):
    def generate_js(self) -> str:
        return """
        myDiagram.nodeTemplate = new go.Node('Auto', {
          selectionAdorned: true,
          resizable: true,
          layoutConditions: go.LayoutConditions.Standard & ~go.LayoutConditions.NodeSized,
          fromSpot: go.Spot.LeftRightSides,
          toSpot: go.Spot.LeftRightSides
        })
          .bindTwoWay('location')
          .bindObject('desiredSize', 'visible', (v) => new go.Size(NaN, NaN), undefined, 'LIST')
          .add(
            new go.Shape('RoundedRectangle', {
              stroke: '#e8f1ff',
              strokeWidth: 3
            })
              .theme('fill', 'primary'),
            new go.Panel('Table', {
              margin: 8,
              stretch: go.Stretch.Fill
            })
              .addRowDefinition(0, { sizing: go.Sizing.None })
              .add(
                new go.TextBlock({
                  row: 0,
                  alignment: go.Spot.Center,
                  margin: new go.Margin(0, 24, 0, 2),
                  font: 'bold 18px sans-serif'
                })
                  .bind('text', 'key')
                  .theme('stroke', 'text')
              )
          );
        """

class LinkTemplate(BaseModel):
    def generate_js(self) -> str:
        return """
        new go.Link({
          selectionAdorned: true,
          layerName: 'Background',
          reshapable: true,
          routing: go.Routing.AvoidsNodes,
          corner: 5,
          curve: go.Curve.JumpOver
        })
        .add(
            new go.Shape({
              stroke: '#f7f9fc',
              strokeWidth: 3
        })
        .theme('stroke', 'link'),
        new go.TextBlock({
              textAlign: 'center',
              font: 'bold 14px sans-serif',
              stroke: 'black',
              segmentIndex: 0,
              segmentOffset: new go.Point(NaN, NaN),
              segmentOrientation: go.Orientation.Upright
        })
        .bind('text')
        .theme('stroke', 'text')
        );
        """

def generate_js() -> str:
    item_template = ItemTemplate().generate_js()
    node_template = NodeTemplate().generate_js()
    link_template = LinkTemplate().generate_js()
    return f"""
    {item_template}
    {node_template}
    {link_template}
    """

print(generate_js())
