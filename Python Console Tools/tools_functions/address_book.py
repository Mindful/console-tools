# address book tool
# make a file in the directory that contains an organized list of names, email addresses, and phone numbers (with service carrier)
# data would be stored in such a way that the user can access it directly, or while using one of the other programs
# NOTE: other programs will probably have to be re-written for this to work with them.
# use the settings file as a template, but it probably isn't exactly right for what we need here.
import os.path, os

def contacts_view(address):
    cFile = open(address,'r+')
    contactsList = cFile.read()
    contactsList = contactsList.split('\n')
    for item in contactsList:
        print(item + '\n')
    cFile.close()
    
def export(name, info_type, address):
    cFile = open(address,'r+')
    contactsList = cFile.read()
    cFile.close()
    contactsList = contactsList.split('\n')
    i = 0
    for item in contactsList:
        contactsList[i] = item.split(':')
        for field in contactsList[i]:
          field = field.strip()
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
    
def contacts_find(address):
    cFile = open(address,'r+')
    contactsList = cFile.read()
    cFile.close()
    contactsList = contactsList.split('\n')
    print('Search for a contact or enter "exit" to exit.')
    search = input('Search: ').lower().strip()
    results = [a for a in contactsList if a.startswith(search)]
    while search != 'exit':
        if len(results) > 0:
            for item in results:
              print(item)
              if len(results) > 1:
                print('\n')
        else:
            print('Contact "'+ search + '" was not found.')
        search = input('Search: ')
    
def contacts_write(address):
    cFile = open(address,'a')
    print('New Contact')
    name = input('Name: ').lower()
    email = input('Email: ').lower()
    phoneNumber = input('Phone Number: ').lower()
    carrier = input('Carrier (for cell phones): ').lower()
    if carrier not in carrierCodes:
        print('Invalid carrier')
        return
    cFile.write('\n'+ name + ' : ' + email + ' : ' + phoneNumber + ' : ' + carrier)
    cFile.close()

def address_book_init(address):
    cFile = open(address,'w')
    cFile.close()
    
def help(address):
    print(func_info[3])
    
def contacts_menu(self, args):
    address = os.path.join(self.homeRoute, 'address_book.tool')
    if not os.path.exists(address):
        address_book_init()
    quit = False
    commands = {'view': contacts_view, 'add': contacts_write, 'help': help, 'search': contacts_find, 'remove': remove}
    while not quit:
        command = input('(Contacts): ').strip().lower()
        if command == 'exit':
            quit = True
        elif command in commands:
            commands[command](address)
        else:
            print('Error: command "' + command + '" not found.')
            
def remove(contact_name):
    cFile = open(address,'r+')
    contactsList = cFile.read()
    cFile.close()
    contactsList = contactsList.split('\n')
    i = 0
    contactsList = [a for a in contactsList if not a.startswith(contact_name)]

func_alias = 'contacts'
func_info = (contacts_menu,
            0,
            0,
            'stores and manipulates a dictionary of names, phone numbers, and email\naddresses. Commands are view, add, search and exit.',
            False,
            )


carrierCodes = {
    'sprint',
    'verizon',
    't-mobile',
    'at&t',
    'virgin mobile',
    'us cellular',
    'nextel',
    'boost',
    'alltel'}