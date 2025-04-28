from pydantic import BaseModel

class BasicProperties(BaseModel):
    name_property: str = 'name'
    gender_property: str = 'gender'
    status_property: str = 'status'
    count_property: str = 'count'

    def to_javascript(self) -> str:
        return f"""const nameProperty = '{self.name_property}';
const genderProperty = '{self.gender_property}';
const statusProperty = '{self.status_property}';
const countProperty = '{self.count_property}';"""

class ThemeColors(BaseModel):
    femaleBadgeBackground: str = '#FFCBEA'
    maleBadgeBackground: str = '#A2DAFF'
    femaleBadgeText: str = '#7A005E'
    maleBadgeText: str = '#001C76'
    kingQueenBorder: str = '#FEBA00'
    princePrincessBorder: str = '#679DDA'
    civilianBorder: str = '#58ADA7'
    personText: str = '#383838'
    personNodeBackground: str = '#FFFFFF'
    selectionStroke: str = '#485670'
    counterBackground: str = '#485670'
    counterBorder: str = '#FFFFFF'
    counterText: str = '#FFFFFF'
    link: str = '#686E76'

class ThemeFonts(BaseModel):
    badgeFont: str = 'bold 12px Poppins'
    birthDeathFont: str = '14px Poppins'
    nameFont: str = '500 18px Poppins'
    counterFont: str = '14px Poppins'

class ThemeConfiguration(BaseModel):
    colors: ThemeColors = ThemeColors()
    fonts: ThemeFonts = ThemeFonts()

    def to_javascript(self) -> str:
        return f"""const theme = {{
  colors: {{
    femaleBadgeBackground: '{self.colors.femaleBadgeBackground}',
    maleBadgeBackground: '{self.colors.maleBadgeBackground}',
    femaleBadgeText: '{self.colors.femaleBadgeText}',
    maleBadgeText: '{self.colors.maleBadgeText}',
    kingQueenBorder: '{self.colors.kingQueenBorder}',
    princePrincessBorder: '{self.colors.princePrincessBorder}',
    civilianBorder: '{self.colors.civilianBorder}',
    personText: '{self.colors.personText}',
    personNodeBackground: '{self.colors.personNodeBackground}',
    selectionStroke: '{self.colors.selectionStroke}',
    counterBackground: '{self.colors.counterBackground}',
    counterBorder: '{self.colors.counterBorder}',
    counterText: '{self.colors.counterText}',
    link: '{self.colors.link}'
  }},
  fonts: {{
    badgeFont: '{self.fonts.badgeFont}',
    birthDeathFont: '{self.fonts.birthDeathFont}',
    nameFont: '{self.fonts.nameFont}',
    counterFont: '{self.fonts.counterFont}'
  }}
}};"""

class PartEventFunctions(BaseModel):
    mouse_enter_function: str = 'onMouseEnterPart'
    mouse_leave_function: str = 'onMouseLeavePart'
    selection_change_function: str = 'onSelectionChange'

    def to_javascript(self) -> str:
        return f"""// toggle highlight on mouse enter/leave
const {self.mouse_enter_function} = (e, part) => part.isHighlighted = true;
const {self.mouse_leave_function} = (e, part) => {{ if (!part.isSelected) part.isHighlighted = false; }};
const {self.selection_change_function} = (part) => {{ part.isHighlighted = part.isSelected; }};"""

class ConstantsDefinition(BaseModel):
    STROKE_WIDTH: int = 3
    ADORNMENT_STROKE_WIDTH: str = "STROKE_WIDTH + 1"
    CORNER_ROUNDNESS: int = 12
    IMAGE_TOP_MARGIN: int = 20
    MAIN_SHAPE_NAME: str = 'mainShape'
    IMAGE_DIAMETER: int = 40

    def to_javascript(self) -> str:
        return (
            f"const STROKE_WIDTH = {self.STROKE_WIDTH};\n"
            f"const ADORNMENT_STROKE_WIDTH = {self.ADJUST_EXPRESSION(self.ADORNMENT_STROKE_WIDTH)};\n"
            f"const CORNER_ROUNDNESS = {self.CORNER_ROUNDNESS};\n"
            f"const IMAGE_TOP_MARGIN = {self.IMAGE_TOP_MARGIN};\n"
            f"const MAIN_SHAPE_NAME = '{self.MAIN_SHAPE_NAME}';\n"
            f"const IMAGE_DIAMETER = {self.IMAGE_DIAMETER};"
        )

    @staticmethod
    def ADJUST_EXPRESSION(value: str) -> str:
        # If the value looks like a math expression, output as-is without quotes
        if any(op in value for op in ['+', '-', '*', '/', '(', ')']):
            return value
        else:
            return f"'{value}'"

class GetStrokeForStatus(BaseModel):
    def to_javascript(self) -> str:
        return """const getStrokeForStatus = (status) => {
  switch (status) {
    case 'king':
    case 'queen':
      return theme.colors.kingQueenBorder;
    case 'prince':
    case 'princess':
      return theme.colors.princePrincessBorder;
    case 'civilian':
    default:
      return theme.colors.civilianBorder;
  }
};"""

class StrokeStyleFunction(BaseModel):
    def to_javascript(self) -> str:
        return """function strokeStyle(shape) {
  return shape
    .set({
      fill: theme.colors.personNodeBackground,
      strokeWidth: STROKE_WIDTH
    })
    .bind('stroke', statusProperty, status => getStrokeForStatus(status))
    .bindObject('stroke', 'isHighlighted', (isHighlighted, obj) =>
      isHighlighted
        ? theme.colors.selectionStroke
        : getStrokeForStatus(obj.part.data.status)
    );
}"""

class GenderConverters(BaseModel):
    def to_javascript(self) -> str:
        return """const genderToText = (gender) => (gender === 'M' ? 'MALE' : 'FEMALE');

const genderToTextColor = (gender) =>
  gender === 'M' ? theme.colors.maleBadgeText : theme.colors.femaleBadgeText;

const genderToFillColor = (gender) =>
  gender === 'M'
    ? theme.colors.maleBadgeBackground
    : theme.colors.femaleBadgeBackground;"""

class PartEventHandlers(BaseModel):
    basic_properties: BasicProperties = BasicProperties()
    theme_configuration: ThemeConfiguration = ThemeConfiguration()
    part_event_functions: PartEventFunctions = PartEventFunctions()
    constants_definition: ConstantsDefinition = ConstantsDefinition()
    get_stroke_for_status: GetStrokeForStatus = GetStrokeForStatus()
    stroke_style_function: StrokeStyleFunction = StrokeStyleFunction()
    gender_converters: GenderConverters = GenderConverters()

    def to_javascript(self) -> str:
        return '\n\n'.join([
            self.basic_properties.to_javascript(),
            self.theme_configuration.to_javascript(),
            self.part_event_functions.to_javascript(),
            self.constants_definition.to_javascript(),
            self.get_stroke_for_status.to_javascript(),
            self.stroke_style_function.to_javascript(),
            self.gender_converters.to_javascript()
        ])