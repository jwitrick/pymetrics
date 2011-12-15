
import sys
import os

class HTMLOut(object):
    
    def __init__(self, outdir, outfile):
        self.fileName = outfile
        self.outdir = outdir
        mode = "w"
        self.html_output = ""
        try:
            if self.fileName:
                if not os.path.exists(self.outdir):
                    os.mkdir(self.outdir)
                self.fd = open( os.path.join(self.outdir, self.fileName), mode )
                self._add_html_opening()
            else:
                self.fd = sys.stdout
        except IOError:
            raise
        
    def _add_html_opening(self):
        html_str = """\
            <html>
            <head></head>
            <body>
                <h1>McCabe Code Complexity</h1>
            """
        self.write(html_str)
        
    def _add_html_closing(self):
        html_str = """\
            </body>
            </html>
        """
        self.write(html_str)
        
    def createNewTableForFile(self, file_data):
        table_open = """\
        <table border=\"1\"\
        """
        table_close = """\
        </table>\
        """
        #output_html = self.createFileHeading(file_name, 3)
        html_table = table_open
        html_table += self.createTableRowHeader()
        for key in file_data.keys():
            val_dict = {"score":file_data[key], "function":key}    
            html_table += self.createTableRow(val_dict)
        html_table += table_close
        
        return html_table
            
    def createTableRowHeader(self):
        row_str = """<tr>\
            <th>McCabe Score:</th>\
            <th>Function Name:</th>\
            </tr>"""
        return row_str
        
    def createTableRow(self, val_dict):
        row_str = """\
            <tr>\
                <td>%(score)s</td>\
                <td>%(function)s</td>\
            </tr>"""
        if int(val_dict["score"]) > 7:
            row_str = """\
                <tr>\
                    <td><font color=\"red\">%(score)s</font></td>\
                    <td>%(function)s</td>\
                </tr>"""    
        return row_str % val_dict        
        
    def createFileHeading(self, file_name, header_level=3):
        header_open = "<h%s>"%str(header_level)
        header_close = "</h%s>"%str(header_level)
        return header_open+"%s"%file_name+header_close
        
    def close( self ):
        if self.fileName:
            self._add_html_closing()
            self.fd.flush()
            self.fd.close()
    
    def write(self, context):
        self.fd.write('%s' % context)