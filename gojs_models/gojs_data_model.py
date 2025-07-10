from typing import List, Dict, Any
from pydantic import BaseModel, Field

class GraphLinksModel(BaseModel):
    copiesArrays: bool = True
    copiesArrayObjects: bool = True
    nodeDataArray: List[Dict[str, Any]] = Field(default_factory=list)
    linkDataArray: List[Dict[str, Any]] = Field(default_factory=list)

    def __init__(
        self,
        copiesArrays: bool = True,
        copiesArrayObjects: bool = True,
        nodeDataArray: List[Dict[str, Any]] = None,
        linkDataArray: List[Dict[str, Any]] = None
    ):
        super().__init__(
            copiesArrays=copiesArrays,
            copiesArrayObjects=copiesArrayObjects,
            nodeDataArray=nodeDataArray or [],
            linkDataArray=linkDataArray or []
        )

    def to_javascript(self) -> str:
        return "\n".join([
            "myDiagram.model = new go.GraphLinksModel({",
            f"  copiesArrays: {str(self.copiesArrays).lower()},",
            f"  copiesArrayObjects: {str(self.copiesArrayObjects).lower()},",
            f"  nodeDataArray: nodeDataArray,",
            f"  linkDataArray: linkDataArray",
            "});"
        ])