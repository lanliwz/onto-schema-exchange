from gojs_models.er.gojs_er_init import *

product_data_array = ModelDataArray(
    nodeDataArray=[
        Node(
            key='Products',
            location=Location(b=250, k=250, h=False),
            items=[
                NodeItem(name='ProductID', iskey=True, figure='Decision', color='purple'),
                NodeItem(name='ProductName', iskey=False, figure='Hexagon', color='blue'),
                NodeItem(name='ItemDescription', iskey=False, figure='Hexagon', color='blue'),
                NodeItem(name='WholesalePrice', iskey=False, figure='Circle', color='green'),
                NodeItem(name='ProductPhoto', iskey=False, figure='TriangleUp', color='red'),
            ],
            inheritedItems=[
                NodeItem(name='SupplierID', iskey=False, figure='Decision', color='purple'),
                NodeItem(name='CategoryID', iskey=False, figure='Decision', color='purple'),
            ],
        ),
        Node(
            key='Suppliers',
            location=Location(b=500, k=0, h=False),
            items=[
                NodeItem(name='SupplierID', iskey=True, figure='Decision', color='purple'),
                NodeItem(name='CompanyName', iskey=False, figure='Hexagon', color='blue'),
                NodeItem(name='ContactName', iskey=False, figure='Hexagon', color='blue'),
                NodeItem(name='Address', iskey=False, figure='Hexagon', color='blue'),
                NodeItem(name='ShippingDistance', iskey=False, figure='Circle', color='green'),
                NodeItem(name='Logo', iskey=False, figure='TriangleUp', color='red'),
            ]
        ),
        Node(
            key='Categories',
            location=Location(b=0, k=30, h=False),
            items=[
                NodeItem(name='CategoryID', iskey=True, figure='Decision', color='purple'),
                NodeItem(name='CategoryName', iskey=False, figure='Hexagon', color='blue'),
                NodeItem(name='Description', iskey=False, figure='Hexagon', color='blue'),
                NodeItem(name='Icon', iskey=False, figure='TriangleUp', color='red'),
            ],
            inheritedItems=[
                NodeItem(name='SupplierID', iskey=False, figure='Decision', color='purple'),
            ],
        ),
        Node(
            key='Order Details',
            location=Location(b=600, k=350, h=False),
            items=[
                NodeItem(name='OrderID', iskey=True, figure='Decision', color='purple'),
                NodeItem(name='UnitPrice', iskey=False, figure='Circle', color='green'),
                NodeItem(name='Quantity', iskey=False, figure='Circle', color='green'),
                NodeItem(name='Discount', iskey=False, figure='Circle', color='green'),
            ],
            inheritedItems=[
                NodeItem(name='ProductID', iskey=False, figure='Decision', color='purple'),
            ],
        ),
    ],
    linkDataArray=[
        Link(from_node='Products', to_node='Suppliers', fromText='0..N', toText='1', text="isSuppliedBy"),
        Link(from_node='Products', to_node='Categories', fromText='0..N', toText='1',text="isCategorizedBy"),
        Link(from_node='Order Details', to_node='Products', fromText='0..N', toText='1',text="includes"),
        Link(from_node='Categories', to_node='Suppliers', fromText='0..N', toText='1',text="lists"),
    ]

)
# print(product_data_array.to_javascript())