from gojs_models.ft.gojs_ft_data_model import *

king_george_v_tree_data = TreePersonDataArray(
    nodes=[
        TreeNodePersonData(name='King George V', gender='M', status='king', born='1865', death='1936'),
        TreeNodePersonData(name='King Edward VIII', gender='M', status='king', born='1894', death='1972', parent='King George V'),
        TreeNodePersonData(name='King George VI', gender='M', status='king', born='1895', death='1952', parent='King George V'),
        TreeNodePersonData(name='Princess Mary, Princess Royal and Countess of Harewood', gender='F', status='princess', born='1897', death='1965', parent='King George V'),
        TreeNodePersonData(name='Prince Henry, Duke of Gloucester', gender='M', status='prince', born='1900', death='1974', parent='King George V')
    ]
)
