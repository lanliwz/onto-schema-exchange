from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod

class GoJsBaseModel(ABC, BaseModel):
    @abstractmethod
    def to_javascript(self) -> str:
        ...

class GraphLinksModel(GoJsBaseModel):
    copiesArrays: bool = True
    copiesArrayObjects: bool = True
    nodeKeyProperty:str = "key"
    dataArray: Optional[GoJsBaseModel] = None

    def __init__(
        self,
        copiesArrays: bool = True,
        copiesArrayObjects: bool = True,
        dataArray: Optional[GoJsBaseModel] = None
    ):
        super().__init__(


            nodeKeyProperty="key",
            copiesArrays=copiesArrays,
            copiesArrayObjects=copiesArrayObjects,
            dataArray=dataArray or None
        )

    def to_javascript(self) -> str:
        if self.dataArray == None:
            return_str="\n".join([
                "myDiagram.model = new go.GraphLinksModel({",
                f"  nodeKeyProperty: '{self.nodeKeyProperty}',",
                f"  copiesArrays: {str(self.copiesArrays).lower()},",
                f"  copiesArrayObjects: {str(self.copiesArrayObjects).lower()},",
                f"  nodeDataArray: nodeDataArray,",
                f"  linkDataArray: linkDataArray",
                "});"
            ])
        else:
            return_str="\n".join([
                "myDiagram.model = new go.GraphLinksModel({",
                f"  nodeKeyProperty: '{self.nodeKeyProperty}',",
                f"  copiesArrays: {str(self.copiesArrays).lower()},",
                f"  copiesArrayObjects: {str(self.copiesArrayObjects).lower()},",
                f"  {self.dataArray.to_javascript()}",
                "});"
            ])

        # print(return_str)
        return return_str