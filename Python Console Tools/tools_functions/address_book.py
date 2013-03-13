# address book tool
# make a file in the directory that contains an organized list of names, email addresses, and phone numbers (with service carrier)
# data would be stored in such a way that the user can access it directly, or while using one of the other programs
# NOTE: other programs will probably have to be re-written for this to work with them.
# use the settings file as a template, but it probably isn't exactly right for what we need here.
import os.path, os

def contacts_view(address):
    for item in contacts:
        print(str(item) + '\n')
    
def export(name, info_type, address):
    try:
        if info_type == 'email':
            return contacts[name].email
        elif info_type == 'phone':
            return contacts[name].number,contactsDict[name].provider
        else:
            return -2
    except KeyError:
            return -1
    
def contacts_find(address):
    print('Search for a contact or enter "exit" to exit.')
    search = input('Search: ').lower().strip()
    while search != 'exit':
        results = [a for a in contacts if a.name.startswith(search)]
        if len(results) > 0:
            for item in results:
              print('\n' + item + '\n')
        else:
            print('Contact "'+ search + '" was not found.')
        search = input('Search: ')
    
def contacts_add(address):
    print('New Contact')
    name = input('Name: ').lower()
    email = input('Email: ').lower()
    phoneNumber = input('Phone Number: ').lower()
    carrier = input('Carrier (for cell phones): ').lower()
    if carrier not in carrierCodes:
        print('Invalid carrier')
        return
    contacts.add(name, phoneNumber, carrier, email)

def address_book_init(address):
    cFile = open(address,'w')
    cFile.close()
    
def help(address):
    print(func_info[3])
    
def contacts_menu(self, args):
    address = os.path.join(self.homeRoute, 'address_book.tool')
    if not os.path.exists(address):
        address_book_init(address)
    
    cFile = open(address,'r+')
    contactsList = cFile.read().split('\n')
    cFile.close()
    
    for item in contactsList:
        if item is not "":
            item = item.split(" : ")
            contacts.add(item[0], item[2], item[3], item[1])
    
    quit = False
    commands = {'view': contacts_view, 'add': contacts_add, 'help': help, 'search': contacts_find, 'remove': remove}
    while not quit:
        command = input('(Contacts): ').strip().lower()
        if command == 'exit':
            quit = True
        elif command in commands:
            commands[command](address)
        else:
            print('Error: command "' + command + '" not found.')
    
    cFile = open(address,'w')
    for item in contacts:
        cFile.write(str(item) + '\n')
    cFile.close()
    
def remove(address):
    contact_name = input('Contact to remove from list: ')
    del contacts[contact_name]
    
class ContactsList:
    def __init__(self):
        self.list = []
        self.dict = {}

    def __getitem__(self, index):
        if type(index) is int:
            return self.list[index]
        elif type(index) is str:
            return self.dict[index]
        else: raise LookupError("Contact must be accessed by name or index")

    def __delitem__(self, index):
        if type(index) is int:
            del self.dict[self.list[index].name]
            del self.list[index]
        elif type(index) is str:
            self.list.remove(self[index]) #This must come first because we are using the dict to fetch the item
            del self.dict[index]
            #search for and remove from string

    def __len__(self):
        return len(self.list)

    def __contains__(self, item):
        'Searches for the contact by name, not object reference'
        return item in self.dict.keys()

    def fromList(self, list):
        self.list = sorted(list)
        for item in self.list:
            self.dict[item.name]=item

    def add(self, name, number, provider, email):
        contact = Contact(name, number, provider, email)
        lo = 0
        hi = len(self.list) #insorting
        while lo < hi:
            mid = (lo+hi)//2
            if contact < self.list[mid]: hi = mid
            else: lo = mid +1
        self.list.insert(lo, contact)
        self.dict[name]=contact
        return lo #This must return the index it inserts at, so we know where to place items in the treeview
        
    def addContact(self, c):
        add(c.name, c.number, c.provider, c.email)
    
class Contact:
    def __init__(self, name, number, provider, email):
        self.name = name
        self.email = email
        self.number = number
        self.provider = provider
        
    def __lt__(self, other):
        return self.name < other.name
        
    def __gt__(self, other):
        return self.name > other.name
        
    def __str__(self):
        return self.name+" : "+self.email+" : "+self.number+" : "+self.provider
    
    
    
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
    
contacts = ContactsList()
