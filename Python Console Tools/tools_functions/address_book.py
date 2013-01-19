# address book tool
# make a file in the directory that contains an organized list of names, email addresses, and phone numbers (with service carrier)
# data would be stored in such a way that the user can access it directly, or while using one of the other programs
# NOTE: other programs will probably have to be re-written for this to work with them.
# use the settings file as a template, but it probably isn't exactly right for what we need here.
import os

def contacts_view():
    cFile = open('address_book.tool','r+')
    contactsList = cFile.read()
    contactsList = contactsList.split('\n')
    for item in contactsList:
        print(item + '\n')
    cFile.close()
    
def export(name, info_type):
    cFile = open('address_book.tool','r+')
    contactsList = cFile.read()
    cFile.close()
    contactsList = contactsList.split('\n')
    i = 0
    for item in contactsList:
        contactsList[i] = item.split(':')
        i += 1
    contactsDict = dict()
    for item in contactsList:
        contactsDict[item[0]] = item[0:]
    try:
        if info_type == 'email':
            return contactsDict[name][1]
        elif info_type == 'phone':
            return contactsDict[name][2],contactsDict[name][3]
        else:
            return -2
    except KeyError:
            return -1
    
def contacts_find():
    cFile = open('address_book.tool','r+')
    contactsList = cFile.read()
    cFile.close()
    contactsList = contactsList.split('\n')
    i = 0
    for item in contactsList:
        contactsList[i] = item.split(':')
        i += 1
    contactsDict = dict()
    for item in contactsList:
        contactsDict[item[0]] = item[0:]
    print('Search for a contact or enter "quit" to exit.')
    search = input('Search: ')
    while search != 'quit':
        try:
            print(contactsDict[search])
        except KeyError:
            print('Contact "'+ search + '" was not found.')
        search = input('Search: ')
    
def contacts_write():
    cFile = open('address_book.tool','a')
    print('New Contact')
    name = input('Name: ').lower()
    email = input('Email: ').lower()
    phoneNumber = input('Phone Number: ').lower()
    carrier = input('Carrier (for cell phones): ').lower()
    cFile.write('\n'+ name + ':' + email + ':' + phoneNumber + ':' + carrier)
    cFile.close()
    

def address_book_init():
    cFile = open('address_book.tool','w')
    cFile.close()
    
def help():
    print(func_info[3])
    
def contacts_menu(self, args):
    if not os.path.exists('address_book.tool'):
        address_book_init()
    quit = False
    commands = {'view': contacts_view,'add': contacts_write, 'help': help, 'search': contacts_find,}
    while not quit:
        command = input('(Contacts): ').strip().lower()
        if command == 'quit':
            quit = True
        elif command in commands:
            commands[command]()
        else:
            print('Error: command "' + command + '" not found.')
    

func_alias = 'contacts'
func_info = (contacts_menu,
            0,
            0,
            'stores and manipulates a dictionary of names, phone numbers, and email addresses.\n Commands are view, add and remove.',
            False,
            )
            
