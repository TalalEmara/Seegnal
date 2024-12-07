signalControlButtonStyle = """
QPushButton{
    background-color: #2d2d2d;
    color: #76D4D4;
    font-family: Sofia sans;
    font-weight: semiBold;
    font-size: 20px;
    border: 3px solid #76D4D4;
    border-radius: 10px;
    padding: 2px;
}
QPushButton:hover {
    background-color: #3a3a3a;
    border-color: #a6f1f1;
    color: #a6f1f1;
}
"""

rewindOffButtonStyle = """
QPushButton{
    background-color: #efefef;
    border: 3px solid #efefef;
    border-radius: 10px;
}
QPushButton:hover {
    background-color: #dcdcdc;
    border-color: #c0c0c0;
}
"""

rewindOnButtonStyle = """
QPushButton{
    background-color: #76D4D4;
    border: 3px solid #76D4D4;
    border-radius: 10px;
}
QPushButton:hover {
    background-color: #a6f1f1;
    border-color: #4ca6a6;
}
"""

linkedButtonOffStyle = """
QPushButton {
    color: #2D2D2D;
    background-color: #efefef;
    font-family: Sofia sans;
    font-weight: semiBold;
    font-size: 20px;
    border: 3px solid #efefef;
    border-radius: 10px;
}
QPushButton:hover {
    background-color: #dcdcdc;
    border-color: #c0c0c0;
}
"""

linkedButtonOnStyle = """
QPushButton {
    color: #2d2d2d;
    background-color: #76D4D4;
    font-family: Sofia sans;
    font-weight: semiBold;
    font-size: 20px;
    border: 3px solid #76D4D4;
    border-radius: 10px;
}
QPushButton:hover {
    background-color: #a6f1f1;
    border-color: #4ca6a6;
}
"""

labelStyle = """
QLabel {
    color: #76D4D4;
    font-family: Sofia sans;
    font-weight: 600;
    font-size:45px;
}
"""
groupBoxStyle = f"""
    QGroupBox {{
        background-color:#2D2D2D;
        border-top: 2px solid #76D4D4;
        border-bottom:none;
        border-radius: 10px 10px 0 0;
        margin-top: 10px;
        margin-bottom:5px;
        padding-top:-4px;
        padding-bottom:-10px;
        font-family: Sofia sans;
        font-weight: 600;
        font-size:10px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 3px;
        color: #76D4D4; 
    }}
"""