from typing import Optional
from pydantic import BaseModel, constr

class LinkShape(BaseModel):
    # https://gojs.net/latest/samples/arrowheads.html
    stroke: constr(pattern=r'^#[0-9a-fA-F]{6}$') = '#f7f9fc'
    strokeWidth: int = 2
    fromArrow: str = 'Chevron'
    toArrow: str = 'Standard'

class TextBlock(BaseModel):
    textAlign: str = 'center'
    font: str = 'bold 14px sans-serif'
    stroke: constr(pattern=r'^#[0-9a-fA-F]{6}$') = '#000000'
    segmentIndex: int
    segmentOffset: Optional[str] = 'new go.Point(NaN, NaN)'
    segmentOrientation: str = 'go.Orientation.Upright'
    textBinding: Optional[str] = None  # field name to bind the text from data

class LinkTemplate(BaseModel):
    selectionAdorned: bool = True
    layerName: str = 'Background'
    reshapable: bool = True
    routing: str = 'go.Routing.AvoidsNodes'
    corner: int = 5
    curve: str = 'go.Curve.JumpOver'
    shape: LinkShape = LinkShape()
    from_label: Optional[TextBlock] = TextBlock(segmentIndex=1, textBinding='fromText')
    to_label: Optional[TextBlock] = TextBlock(segmentIndex=-1, textBinding='toText')
    middle_label: Optional[TextBlock] = TextBlock(segmentIndex=3, textBinding='text')

    def to_javascript(self, diagram_name: str = 'myDiagram') -> str:
        js = f"""{diagram_name}.linkTemplate = new go.Link({{
  selectionAdorned: {str(self.selectionAdorned).lower()},
  layerName: '{self.layerName}',
  reshapable: {str(self.reshapable).lower()},
  routing: {self.routing},
  corner: {self.corner},
  curve: {self.curve}
}})
  .add(
    new go.Shape({{
      stroke: '{self.shape.stroke}',
      strokeWidth: {self.shape.strokeWidth}
    }}).theme('stroke', 'link'),
    new go.Shape({{
      stroke: '{self.shape.stroke}',
      strokeWidth: {self.shape.strokeWidth},
      fromArrow: '{self.shape.fromArrow}'
    }}).theme('stroke', 'link'),
        new go.Shape({{
      stroke: '{self.shape.stroke}',
      strokeWidth: {self.shape.strokeWidth},
      toArrow: '{self.shape.toArrow}'
    }}).theme('stroke', 'link'),
    new go.TextBlock({{
      textAlign: '{self.from_label.textAlign}',
      font: '{self.from_label.font}',
      stroke: '{self.from_label.stroke}',
      segmentIndex: {self.from_label.segmentIndex},
      segmentOffset: {self.from_label.segmentOffset},
      segmentOrientation: {self.from_label.segmentOrientation}
    }}).bind('text', '{self.from_label.textBinding}')
      .theme('stroke', 'text'),
    new go.TextBlock({{
      textAlign: '{self.to_label.textAlign}',
      font: '{self.to_label.font}',
      stroke: '{self.to_label.stroke}',
      segmentIndex: {self.to_label.segmentIndex},
      segmentOffset: {self.to_label.segmentOffset},
      segmentOrientation: {self.to_label.segmentOrientation}
    }}).bind('text', '{self.to_label.textBinding}')
      .theme('stroke', 'text'),
    new go.TextBlock({{
      textAlign: '{self.middle_label.textAlign}',
      font: '{self.middle_label.font}',
      stroke: '{self.middle_label.stroke}',
      segmentIndex: {self.middle_label.segmentIndex},
      segmentOffset: {self.middle_label.segmentOffset},
      segmentOrientation: {self.middle_label.segmentOrientation}
    }}).bind('text', '{self.middle_label.textBinding}')
      .theme('stroke', 'text')
  );"""
        return js

