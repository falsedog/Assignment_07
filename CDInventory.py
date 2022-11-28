#------------------------------------------#
# Title: Assignment07.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# Rain Doggerel, 2022-Nov-27 Actually implemented try/except stuff, new filename function (rough)
# Rain Doggerel, 2022-Nov-26 Copied and updated to new assignment
# Rain Doggerel, 2022-Nov-20 Bug hunted and added docstrings
# Rain Doggerel, 2022-Nov-19, Moved things around
# DBiesinger, 2030-Jan-01, Created File
#------------------------------------------#

# -- IMPORTS -- #
import pickle

# -- DATA -- #
strChoice = ''  # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage filename
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Processing the data within lstTbl/copy"""

    @staticmethod
    def new_album_add(aIntID, aTitle, aArtist, aTable):
        """Function to add an entry to a list of dictionaries

        Composes a new dictionary and appends to an existing list of dictionaries.

        Args:
            aIntID (Int): the index of this new album 
            aTitle (Str): the title of the new album
            aArtist (Str): the artist of the new album
            aTable (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            Updated list of dictionaries table.
        """
        addRow = {'ID': aIntID, 'Title': aTitle, 'Artist': aArtist}
        aTable.append(addRow)
        return aTable

    @staticmethod
    def delete_album(searchID, lstTbl):
        """Function to remove an entry from a list of dictionaries

        Loops through the list of dictionaries seeking an entry that matches a
        particular ID and if found deletes it or reports otherwise.

        Args:
            searchID (Int): the index within the inventory to find and delete 
            dTable (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == searchID:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed\n')
        else:
            print('Could not find this CD!')


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def filename_handler():
        """Function to change filename or create blank file

        Offers an option to create blank file with implied filename or 
        set a new filename and return (in case it exists and we don't want to
        touch it immediately).

        Args:
            None.

        Returns:
            None.
        """
        global strFileName # To break out of the scope of this function to modify this variable
        while True:
            print(
                'Would you like to specify a different [F]ilename or [C]reate a new blank file?')
            # I want to improve the presentation here but I also don't until I can change a lot more of the presentation
            print('Please input a choice f or c')
            handlerChoice = input()
            if handlerChoice.lower() == 'c':
                try:
                    with open(strFileName, 'a') as existenceTouch: # This works for pickles sort of* like other files
                        existenceTouch.write('')
                    print(
                        'Okay, blank file exists now, if you were saving, try again') # Imperfect accounting but better to communicate more
                    return
                except Exception as e:  # Very generic error
                    print(
                        'Hey is something wrong with my access to the filesystem? You might need to fix that for me...', e, sep='\n')
                        # Not much we can do in scope if so
            elif handlerChoice.lower() == 'f':  # In the future this might become a separate function
                print('Please input the filename you would like to use (ending in .dat is conventional)')
                strFileName = input().strip()
                print('Filename changed, returning to menu, please try loading again')
                return  # Go back to main menu
            else:
                print('That wasn\'t a valid option, sorry, try that again')
                # Loops here

    @staticmethod
    def read_file(strFileName, lstTbl):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by strFileName into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            strFileName (string): name of file used to read the data from
            rTable (list of dict): 2D data structure (list of dicts) that holds the data in this function

        Returns:
            None.
        """
        lstTbl.clear()  # this clears existing data
        try:
            with open(strFileName, 'rb') as inventoryRead:
                lstTbl.extend(pickle.load(inventoryRead))
        except FileNotFoundError:
            print('Cannot find file: ', strFileName)
            FileProcessor.filename_handler()
        except EOFError: # *Pickles care a little more about what's inside
            print('File is blank, proceeding with empty database')

    @staticmethod
    def write_file(strFileName, wTable):
        """Function to write the inventory to a file

        Unpacks dictionary, composes strings and concatenates them and writes
        that to a file.

        Args:
            strFileName (Str): name of the inventory file
            wTable (list of dict): 2D data structure (list of dicts) that holds the data in this function

        Returns:
            None.
        """
        try:
            with open(strFileName, 'wb') as inventoryWrite:
                pickle.dump(wTable, inventoryWrite)
        except FileNotFoundError as e:
            print('Can\'t access the file', e, sep='\n')
            FileProcessor.filename_handler()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print(
            'Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input(
                'Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def new_album_query():
        """Queries user for new album details

        Args:
            None.

        Returns:
            List of user inputs (Int, Str, Str).

        """
        while True:
            fID = input('Enter ID: ').strip()
            try:
                fIntID = int(fID)
            except ValueError:
                print('Sorry that ID wasn\'t a valid number, please try again\n')
                continue
            else: # I understand you can keep the try blocks smaller this way but it feels weird
                fTitle = input('What is the CD\'s title? ').strip()
                fArtist = input('What is the Artist\'s name? ').strip()  # lol
                newAlbumInput = [fIntID, fTitle, fArtist]
                return newAlbumInput


# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl) # I think this should be an option still...

# 2. Start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input(
            'type \'yes\' to continue and reload from file, otherwise reload will be canceled\n')
        if strYesNo.lower().strip() == 'yes':
            print('reloading', strFileName)
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input(
                'canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        newEntry = IO.new_album_query()
        # 3.3.2 Add item to the table
        lstTbl = DataProcessor.new_album_add(
            newEntry[0], newEntry[1], newEntry[2], lstTbl)
        IO.show_inventory(lstTbl)
        continue
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        IDDel = input('Which ID would you like to delete? ').strip()
        try:
            intIDDel = int(IDDel)
        except ValueError:
            print('Search ID isn\'t a valid number to search for, please try again')
            continue # Easier way to have them try again without making a new loop
        # 3.5.2 search thru table and delete CD
        DataProcessor.delete_album(intIDDel, lstTbl)
        IO.show_inventory(lstTbl)
        continue
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input(
                'The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')
