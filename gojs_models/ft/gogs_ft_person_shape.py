from pydantic import BaseModel

class PersonBadge(BaseModel):
    alignmentFocus: str = 'TopRight'
    alignment: tuple = (1, 0, -25, "STROKE_WIDTH - 0.5")
    figure: str = 'RoundedRectangle'
    parameter1: str = 'CORNER_ROUNDNESS'
    parameter2: str = '4 | 8'
    desiredHeight: float = 22.5
    font: str = 'theme.fonts.badgeFont'

    def to_javascript(self) -> str:
        return f"""const personBadge = () =>
  new go.Panel('Auto', {{
    alignmentFocus: go.Spot.{self.alignmentFocus},
    alignment: new go.Spot({self.alignment[0]}, {self.alignment[1]}, {self.alignment[2]}, {self.alignment[3]})
  }})
    .add(
      new go.Shape({{
        figure: '{self.figure}',
        parameter1: {self.parameter1},
        parameter2: {self.parameter2},
        desiredSize: new go.Size(NaN, {self.desiredHeight}),
        stroke: null
      }})
        .bind('fill', genderProperty, genderToFillColor),
      new go.TextBlock({{
        font: {self.font}
      }})
        .bind('stroke', genderProperty, genderToTextColor)
        .bind('text', genderProperty, genderToText)
    );"""

class PersonBirthDeathTextBlock(BaseModel):
    stroke: str = 'theme.colors.personText'
    font: str = 'theme.fonts.birthDeathFont'
    alignmentFocus: str = 'Top'
    alignment: tuple = (0.5, 1, 0, -35)

    def to_javascript(self) -> str:
        return f"""const personBirthDeathTextBlock = () =>
  new go.TextBlock({{
    stroke: {self.stroke},
    font: {self.font},
    alignmentFocus: go.Spot.{self.alignmentFocus},
    alignment: new go.Spot({self.alignment[0]}, {self.alignment[1]}, {self.alignment[2]}, {self.alignment[3]})
  }})
    .bind('text', '', ({{ born, death }}) => {{
      if (!born) return '';
      return `${{born}} - ${{death ?? ''}}`;
    }});"""

class PersonCounter(BaseModel):
    visible: bool = False
    alignmentFocus: str = 'Center'
    alignment: str = 'Bottom'
    circleSize: int = 29
    strokeWidth: str = 'STROKE_WIDTH'
    stroke: str = 'theme.colors.counterBorder'
    fill: str = 'theme.colors.counterBackground'
    font: str = 'theme.fonts.counterFont'
    textAlign: str = 'center'

    def to_javascript(self) -> str:
        return f"""const personCounter = () =>
  new go.Panel('Auto', {{
    visible: {str(self.visible).lower()},
    alignmentFocus: go.Spot.{self.alignmentFocus},
    alignment: go.Spot.{self.alignment}
  }})
    .bindObject('visible', '', (obj) => obj.findLinksOutOf().count > 0)
    .add(
      new go.Shape('Circle', {{
        desiredSize: new go.Size({self.circleSize}, {self.circleSize}),
        strokeWidth: {self.strokeWidth},
        stroke: {self.stroke},
        fill: {self.fill}
      }}),
      new go.TextBlock({{
        alignment: new go.Spot(0.5, 0.5, 0, 1),
        stroke: theme.colors.counterText,
        font: {self.font},
        textAlign: '{self.textAlign}'
      }})
        .bindObject('text', '', (obj) => obj.findNodesOutOf().count)
    );"""

class PictureStyle(BaseModel):
    def to_javascript(self) -> str:
        return """function pictureStyle(pic) {
  return pic
    .bind('source', '', ({ status, gender }) => {
      switch (status) {
        case 'king':
        case 'queen':
          return './images/king.svg';
        case 'prince':
        case 'princess':
          return './images/prince.svg';
        case 'civilian':
          return gender === 'M'
            ? './images/male-civilian.svg'
            : './images/female-civilian.svg';
        default:
          return './images/male-civilian.svg';
      }
    })
    .bind('desiredSize', 'status', status => {
      switch (status) {
        case 'king':
        case 'queen':
          return new go.Size(30, 20);
        case 'prince':
        case 'princess':
          return new go.Size(28, 20);
        case 'civilian':
        default:
          return new go.Size(24, 24);
      }
    });
}"""

class PersonImage(BaseModel):
    alignmentFocus: str = 'Top'
    alignment: tuple = (0, 0, 'STROKE_WIDTH/2', 'IMAGE_TOP_MARGIN')
    figure: str = 'Circle'
    diameter: str = 'IMAGE_DIAMETER'
    pictureScale: float = 0.9

    def to_javascript(self) -> str:
        return f"""const personImage = () =>
  new go.Panel('Spot', {{
    alignmentFocus: go.Spot.{self.alignmentFocus},
    alignment: new go.Spot({self.alignment[0]}, {self.alignment[1]}, {self.alignment[2]}, {self.alignment[3]})
  }})
    .add(
      new go.Shape({{
        figure: '{self.figure}',
        desiredSize: new go.Size({self.diameter}, {self.diameter})
      }})
        .apply(strokeStyle),
      new go.Picture({{ scale: {self.pictureScale} }})
        .apply(pictureStyle)
    );"""

class PersonMainShape(BaseModel):
    figure: str = 'RoundedRectangle'
    size: tuple = (215, 110)
    portId: str = ''
    parameter1: str = 'CORNER_ROUNDNESS'

    def to_javascript(self) -> str:
        return f"""const personMainShape = () =>
  new go.Shape({{
    figure: '{self.figure}',
    desiredSize: new go.Size({self.size[0]}, {self.size[1]}),
    portId: '{self.portId}',
    parameter1: {self.parameter1}
  }})
    .apply(strokeStyle);"""

class PersonNameTextBlock(BaseModel):
    stroke: str = 'theme.colors.personText'
    font: str = 'theme.fonts.nameFont'
    desiredSize: tuple = (160, 50)
    overflow: str = 'Ellipsis'
    textAlign: str = 'center'
    verticalAlignment: str = 'Center'
    toolTipMargin: int = 4
    alignmentFocus: str = 'Top'
    alignment: tuple = (0.5, 0, 0, 25)

    def to_javascript(self) -> str:
        return f"""const personNameTextBlock = () =>
  new go.TextBlock({{
    stroke: {self.stroke},
    font: {self.font},
    desiredSize: new go.Size({self.desiredSize[0]}, {self.desiredSize[1]}),
    overflow: go.TextOverflow.{self.overflow},
    textAlign: '{self.textAlign}',
    verticalAlignment: go.Spot.{self.verticalAlignment},
    toolTip: go.GraphObject.build('ToolTip')
      .add(new go.TextBlock({{ margin: {self.toolTipMargin} }}).bind('text', nameProperty)),
    alignmentFocus: go.Spot.{self.alignmentFocus},
    alignment: new go.Spot({self.alignment[0]}, {self.alignment[1]}, {self.alignment[2]}, {self.alignment[3]})
  }})
    .bind('text', nameProperty);"""

class PersonShapeComponents(BaseModel):
    personBadge: PersonBadge = PersonBadge()
    personBirthDeathTextBlock: PersonBirthDeathTextBlock = PersonBirthDeathTextBlock()
    personCounter: PersonCounter = PersonCounter()
    pictureStyle: PictureStyle = PictureStyle()
    personImage: PersonImage = PersonImage()
    personMainShape: PersonMainShape = PersonMainShape()
    personNameTextBlock: PersonNameTextBlock = PersonNameTextBlock()

    def to_javascript(self) -> str:
        return '\n\n'.join([
            self.personBadge.to_javascript(),
            self.personBirthDeathTextBlock.to_javascript(),
            self.personCounter.to_javascript(),
            self.pictureStyle.to_javascript(),
            self.personImage.to_javascript(),
            self.personMainShape.to_javascript(),
            self.personNameTextBlock.to_javascript()
        ])
