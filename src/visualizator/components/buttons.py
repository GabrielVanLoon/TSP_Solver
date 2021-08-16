class Button:
    def __init__(self):
        self.validation = "border: 1px solid;margin: 10px 0px;padding: 15px 10px 15px 50px;background-repeat: no-repeat;background-position: 10px center;"
        self.class_error = "color: #D8000C; background-color: #FFBABA;"
    
    def error(self, msg):
        html_error_msg = '<h3 style="{0}">{1}</h3>'.format(self.class_error + self.validation, msg)
        return html_error_msg
