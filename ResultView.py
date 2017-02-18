import cx_Oracle
from time import sleep
from curses import textpad
import curses, os, curses.panel





########################################################################
class ViewData:

    """"""
    BORDER_HIGH=2  # Title heigth
    KEY_QUIT = 'Q'
    OPERATION_UPDATE = 'U'
    OPERATION_SELECT = 'S'
    OPERATION_DELETE = 'D'
    optionsBar = []


    #----------------------------------------------------------------------
    def __init__(self, data):

        """Constructor"""
        self.screen = curses.initscr() #initializes a new window for capturing key presses
        curses.noecho() # Disables automatic echoing of key presses (prevents program from input each key twice)
        curses.cbreak() # Disables line buffering (runs each key as it is pressed rather than waiting for the return key to pressed)
        curses.start_color() # Lets you use colors when highlighting selected menu option
        self.screen.keypad(1) # Capture input from keypad
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        self.screen = curses.initscr() #initializes a new window for capturing key presses
        curses.noecho() # Disables automatic echoing of key presses (prevents program from input each key twice)
        curses.cbreak() # Disables line buffering (runs each key as it is pressed rather than waiting for the return key to pressed)
        curses.start_color() # Lets you use colors when highlighting selected menu option
        self.screen.keypad(1) # Capture input from keypad

        # Change this to use different colors when highlighting
        curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE) # Sets up color pair #1, it does black text with white background
        #
        self.data = data
        #Init Options
        self.addOption('Quit', ViewData.KEY_QUIT, 2 )
    #----------------------------------------------------------------------
    def addData(self, appData):
        self.data.append(appData)
        """"""
    def replData(self, newData):
        self.data = newData

    def close(self):
        if self.tb:  # force window to close instantaneously
            self.tb.do_command = lambda x: False


    def values_textpad(self, stdscr, key, text, insert_mode=False, validator= None, confermValue='' ):
        cord_x,cord_y = self.screen.getmaxyx()
        ncols, nlines = cord_y - 4, 1
        uly, ulx = cord_x - 3, 2
        if validator is None:
            validator =  self.enter_validator
        text_info = "{} {} :".format(text, key)
        stdscr.addstr(uly, ulx, confermValue, curses.color_pair(8))
        stdscr.addstr(uly-1, ulx, text_info, curses.color_pair(3))
        win = curses.newwin(nlines, ncols-len(text_info), uly-1, ulx+len(text_info))
        textpad.rectangle(stdscr, uly-3, ulx-1, uly + nlines, ulx + ncols)
        stdscr.refresh()
        box = textpad.Textbox(win, insert_mode)
        contents = box.edit(validator).strip()
        return str(contents)

    def confermOption_textpad(self, stdscr, key, text, insert_mode=False, confermValue=''):
        conferm = self.values_textpad(stdscr, key, text, True, self.yes_no_validator, confermValue)
        return conferm.upper()

    def yes_no_validator(self, ch):
        if ch in [78, 83,110,  115]:
            return  ch
        elif ch == 10:
            return 7

    def enter_validator(self, ch):
            if ch == 10:
                return 7
            return  ch


    #----------------------------------------------------------------------
    def addOption(self, optionName, key, color, optionValues=None):
        option = {}
        option['Name'] = str(optionName)
        option['Key'] =  ord(key)
        option['Color'] = int(color)
        option['Options'] = optionValues
        ViewData.optionsBar.append(option)

    #----------------------------------------------------------------------
    def showOptions(self):
        cord_x,cord_y = self.screen.getmaxyx()
        count_y =  3 # init pos y
        optionBar1 = ""
        for option in ViewData.optionsBar:
            try:
                self.screen.addstr(cord_x-1, count_y, " {}".format(chr(option['Key'])),curses.color_pair(option['Color']))
                count_y += len(chr(option['Key'])) + 1
                self.screen.addstr(cord_x-1, count_y, " - {}".format(option['Name']),curses.A_BOLD)
                count_y += len(option['Name']) +  3
            except: pass


    def checkOption(self, x):
        values_where =  None
        for option in ViewData.optionsBar:
            if option['Key'] == x:
                #print 'KEY FOUNT Option KEY {}   x:{}'.format(option['Key'],  x)
                if x == ord(ViewData.KEY_QUIT):
                    return None
                else:
                    try:
                        ##Get Values
                        values_where = option['Options'].copy()
                        for key, value in option['Options']['Where'].iteritems():
                            strtest = self.values_textpad(self.screen, key, 'Inserisci identificatore', True)
                            #print strtest
                            values_where['Where'][key] = strtest
                        #values_where = option['Options']['Set']
                        for key, value in option['Options']['Set'].iteritems():
                            strtest = self.values_textpad(self.screen, key, 'Inserisci valore' , True)
                            #print strtest
                            values_where['Set'][key] = strtest
                        #print values_where
                        #sleep(5)
                        return values_where
                    except  :
                        pass



        return values_where




    # This function displays the
    def runbiew(self):
        option_select = None

        linescount =  len(self.data)
        rowsMaxLengh =  0
        posx=0   # Initial pos X
        posy=0   # Initial pos Y
        x = None # Key pressed
        refresh =  True # control for while loop
        while (x != ord(ViewData.KEY_QUIT) and option_select == None):
            #self.screen.addstr(0, 5, " KEY:{}".format(x), curses.A_STANDOUT) # Title for this menu curses.A_BLINK
            if refresh :# If refresh Page
                refresh = True
                self.screen.clear()
                self.screen.border(0)

                cord_x,cord_y = self.screen.getmaxyx() # get windows max coordinate
                max_rowview_x = cord_x - ViewData.BORDER_HIGH
                max_colview_y =  cord_y - ViewData.BORDER_HIGH
                line_to = posx
                row_to =  posy

                if (linescount -  posx) > max_rowview_x :
                    line_from =  max_rowview_x + posx
                else:
                    line_from = linescount

                #debug
                #self.screen.addstr(0, 5, " x:{} y:{} posx:{} posxy:{} Max x:{} Max y:{} KEY:{} maxrow:{} ".format(cord_x,cord_y,posx, posy, max_rowview_x,max_colview_y,  x, rowsMaxLengh, ), curses.A_STANDOUT) # Title for this menu curses.A_BLINK
                #self.screen.addstr(1, 1, " Len Doc:{} ".format(rowscount), curses.A_STANDOUT) # Title for this menu curses.A_BLINK

                #draw data
                for line,index in zip(range(max_rowview_x),range(line_to,line_from,1)):#for f, b in zip(foo, bar):
                    try:
                        row_from =  0
                        textLengh =  len(str(self.data[index]))
                        if rowsMaxLengh < textLengh :
                            rowsMaxLengh =  textLengh
                        # Calculate max text length
                        if (textLengh -  posy) > max_colview_y :
                            row_from =  max_colview_y + posy - 1
                        else:
                            row_from = textLengh
                        # Extract text
                        textview =    str(self.data[index])[row_to:row_from]
                        # Show text
                        self.screen.addstr(line+1, 2, "%s" % (textview),  curses.color_pair(0)) #,textstyle)

                    except ValueError, Argument:
                        curses.beep()
                        print('error:{}'.format(line))
                        self.screen.addstr(2, 5, "Error:{}".format(Argument), curses.A_STANDOUT)
                #draw Options
                self.showOptions()

                self.screen.refresh()
            #get input key
            x = self.screen.getch() # Gets user input
            #print x
            # What is user input?
            if x == 258: # down arrow
                if posx < linescount - 1:
                    posx += 1
                    refresh =  True
            elif x == 259: # up arrow
                if posx > 0:
                    posx += -1
                    refresh =  True
            elif x ==  261:
                if (posy < rowsMaxLengh - 1):
                    posy += 1
                    refresh =  True
            elif x ==  260:
                if posy > 0:
                    posy -= 1
                    refresh =  True
            else:
                option_select = self.checkOption(x)
                print option_select
                #sleep(6)
                if option_select:
                    #confirm option
                    self.screen.clear()
                    #print self.constructQuery(option_select)[0]
                    #sleep(5)
                    testo =  self.confermOption_textpad(self.screen, '(S/N)', 'Conferma?', True, self.constructQuery(option_select)[0])
                    if (testo) == 'S':
                        return option_select
                    else:
                        option_select =  None
        curses.endwin()
        #print option_select
        return None
    #----------------------------------------------------------------------
    def constructQuery(self, option_selcted, items='*'):
        str_query = ''
        res_str_query =  ''
        TEXT_AND = ' AND '
        TEXT_OR = ' OR '
        TEXT_SEPARATOR =  ','
        # Check items
        if 'select_field' in option_selcted:
            items =  option_selcted['select_field']
        if option_selcted['operation'] ==  ViewData.OPERATION_SELECT :
            str_query += 'SELECT {} from {}'.format(items, option_selcted['name'])
            cond_len = len(option_selcted['Where'])
            if cond_len >  0:
                str_query += ' WHERE '

                for key, value in option_selcted['Where'].iteritems():
                    str_query += '{} = {}'.format(key, repr(value))
                    res_str_query+= '{} = {} '.format(key, repr(value))
                    if cond_len > 1: str_query += (TEXT_AND)
                if str_query.endswith(TEXT_AND):
                    str_query = str_query[:len(str_query)-len(TEXT_AND)]

        elif option_selcted['operation'] ==  ViewData.OPERATION_UPDATE:
            str_query += 'UPDATE {} '.format(option_selcted['name'])
            sets_len = len(option_selcted['Set'])
            if sets_len >  0:
                str_query += ' SET '
                for key, value in option_selcted['Set'].iteritems():
                    str_query += ' {} = {}'.format(key, repr(value))
                    res_str_query += ' {} = {}'.format(key, repr(value))
                    if sets_len > 1: str_query += (TEXT_SEPARATOR)
                if str_query.endswith(TEXT_SEPARATOR):
                    str_query = str_query[:len(str_query)-len(TEXT_SEPARATOR)]

            cond_len = len(option_selcted['Where'])
            if cond_len >  0:
                str_query += ' WHERE '

                for key, value in option_selcted['Where'].iteritems():
                    str_query += '{} = {}'.format(key, repr(value))
                    if cond_len > 1: str_query += (TEXT_AND)
                if str_query.endswith(TEXT_AND):
                    str_query = str_query[:len(str_query)-5]
                res_str_query = str_query

        return str_query, res_str_query

if __name__ == '__main__':
    List1 = ['physics physics physics physics physics physics physics physics physics physics physics physics', 'chemistry chemistrychemistrychemistrychemistrychemistrychemistrychemistrychemistry', 1997, 2000, 'physics', 'chemistry', 1997, 2000, 'physics', 'chemistry', 1997, 2000, 'physics', 'chemistry', 1997, 2000];
    List1.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"% ("CODICE", "CDRL", "ODR", "NOME", "COGNOME", "CF", "DATA_NASCITA", "SESSO", "EMAIL", "FASE","ULTIMA_MODIFICA","IDKIT","TITOLO","NAZIONE","NUMERO_CELLULARE","COD_CONVENZ.", "COD_LICENZA","ORGANIZZAZIONE"))
    TABLE_NAME =  'EMPLOYER'
    print List1

    valuse_modify =  {
        'name': TABLE_NAME,
        'operation': ViewData.OPERATION_UPDATE,
        'Where': {'COD_ID': '','COD_ID_2':''},
        'Set':   {'Name': '', 'Cognome': ''},
    }
    valuse_select =  {
        'name': TABLE_NAME,
        'operation': ViewData.OPERATION_SELECT,
        'Where': {'COD_ID': ''},
    }




    view =  ViewData(List1)
    view.addOption('Modify', 'M', 3,valuse_modify )
    view.addOption('Select', 'S', 4,valuse_select )
    option_selcted =  view.runbiew()
    print option_selcted
    print List1




