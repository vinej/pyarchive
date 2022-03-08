from task.memory import Memory
from task.util import get_dict_value
import logging
from message.message import gmsg
import sys
import openpyxl
from copy import copy
from openpyxl.formula.translate import Translator
from openpyxl.utils import get_column_letter

'''
The Template class is used to output memory info into an Excel template

The json object propertiesw

Name        :   the name of the task
Kind        :   template
Description :   the description of the task
Command     :   contains the list of values separated by a pipe |
Output      :   memory
'''
class Template:
    def __init__(self, jsondata):
        self.name = get_dict_value(jsondata,'Name')
        self.kind = get_dict_value(jsondata,'Kind')
        self.description = get_dict_value(jsondata,'Description')
        self.file = get_dict_value(jsondata,'File')
        self.template = get_dict_value(jsondata,'Template')
    #def


    def validate(self, mapcon, position):  
        _ = mapcon # not use here
        if self.name == None:
            logging.fatal(gmsg.get(26), position, 'Name')
            sys.exit(26)
        #if
        self.name = self.name.lower()

        if self.kind == None:
            logging.fatal(gmsg.get(27), position, self.name, 'Kind')
            sys.exit(27)
        #
        self.kind = self.kind.lower()
	#def

    def copyRange(self, startCol, startRow, endCol, endRow, sheet):
        rangeSelected = []
        rangeSelectedStyle = []
        #Loops through selected Rows
        for i in range(startRow,endRow + 1,1):
            #Appends the row to a RowSelected list
            rowSelected = []
            rowSelectedStyle = []
            for j in range(startCol,endCol+1,1):
                rowSelected.append(sheet.cell(row = i, column = j).value)
                rowSelectedStyle.append(copy(sheet.cell(row = i, column = j)._style))
            #Adds the RowSelected List and nests inside the rangeSelected
            rangeSelected.append(rowSelected)
            rangeSelectedStyle.append(rowSelectedStyle)
        return rangeSelected, rangeSelectedStyle
    #def



    #Paste data from copyRange into template sheet
    def pasteRange(self, startCol, startRow, endCol, endRow, sheetReceiving, copiedData, col_ori, row_ori):
        countRow = 0
        for i in range(startRow,endRow+1,1):
            countCol = 0
            for j in range(startCol,endCol+1,1):
                value = copiedData[countRow][countCol]
                if value[0] == '=':
                    ori = get_column_letter(j) + str(row_ori+2)
                    dst = get_column_letter(j) + str(i)
                    sheetReceiving.cell(row = i, column = j).value = Translator(value, origin=ori).translate_formula(dst)
                else:
                    sheetReceiving.cell(row = i, column = j).value = copiedData[countRow][countCol]
                countCol += 1
            countRow += 1
    #def

    #Paste data from copyRange into template sheet
    def pasteRangeStyle(self, startCol, startRow, endCol, endRow, sheetReceiving, copiedData):
        countRow = 0
        for i in range(startRow,endRow+1,1):
            countCol = 0
            for j in range(startCol,endCol+1,1):
                sheetReceiving.cell(row = i, column = j)._style = copiedData[countRow][countCol]
                countCol += 1
            countRow += 1
    #def

    def find_cr(self, sheet, value):
        for r in range(sheet.max_row):
            for c in range(sheet.max_column):
                if sheet.cell(r+1,c+1).value == value:
                    print(c+1, r+1)
                    return (c+1,r+1)
        raise Exception('not found')
    #def

    '''
    Get a list of fields name from the cell with pattern {{xxx}}
    '''
    def get_field_name(self, value):
        outnames = []
        # return a list of name {{xxx}}
        list = value.split('{{')
        for part in list:
            idx = part.find('}}')
            if idx != -1:
                outnames.append('{{'+part[:idx+2])
        return outnames
    #def

    def replace_field_name(self, row, name, value):
        field = name.replace('{{','')
        field = field.replace('}}','')
        return value.replace(name, row[field])
    #def

    def replace_fields(self, row, startCol, startRow, endCol, endRow, sheet):
        #Loops through selected Rows
        for i in range(startRow,endRow + 1,1):
            for j in range(startCol,endCol+1,1):
                if sheet.cell(i,j).value.startswith('=') == False:
                    listnames = self.get_field_name(sheet.cell(i,j).value)
                    for name in listnames:
                        sheet.cell(i,j).value = self.replace_field_name(row, name, sheet.cell(i,j).value)
            #Adds the RowSelected List and nests inside the rangeSelected
    #def

    def run(self, mapmem, mapref, mapcon, position):
        logging.info(gmsg.get(4), self.kind, self.name)

        book = openpyxl.load_workbook(self.template)

        for sheet in book.worksheets:
            source = sheet.title
            c1,r1 = self.find_cr(sheet, '{{begin}}')
            # 1,2
            c2,r2 = self.find_cr(sheet, '{{end}}')
            # 1,4
            # insert rows before the end
            sheet.insert_rows(r2,len(mapmem[source].rows)-1)
            rng,sty = self.copyRange(c1,r1+1,sheet.max_column,r2-1,sheet)
            for i in range(len(mapmem[source].rows)):
                self.pasteRange(c1,r1+i+1,sheet.max_column,r1+i+1,sheet,rng,c1,r1)
                self.pasteRangeStyle(c1,r1+i+1,sheet.max_column,r1+i+1,sheet,sty)

            for i in range(len(mapmem[source].rows)):
                self.replace_fields(mapmem[source].rows[i], c1, r1+i+1, sheet.max_column, r1+i+1, sheet)

            sheet.delete_rows(r1,1)
            sheet.delete_rows(r2+len(mapmem[source].rows)-2)
                
        book.save(self.file)

        logging.info(gmsg.get(3), self.kind, self.name)
    #def



#class

