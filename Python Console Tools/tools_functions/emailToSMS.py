import smtplib, sys, os, importlib, getpass
from email.mime.text import MIMEText
from os import path

def emailToSMS(self, args):
    addon = False
    if os.path.exists('tools_functions\\address_book.py'):
        address_book = importlib.__import__('address_book')
        addon = True
    carrierCodes = {
    'sprint': '@messaging.sprintpcs.com',
    'verizon': '@vtext.com',
    't-mobile': '@tmomail.net',
    'at&t': '@txt.att.net',
    'virgin mobile': '@vmobl.com',
    'us cellular': '@email.uscc.net',
    'nextel': '@messaging.nextel.com',
    'boost': '@myboostmobile.com',
    'alltel': '@message.alltel.com'}
    if args[0] == 'contact' and addon:
        if len(args) > 2:
            while len(args) > 2:
                args[1] = args[1] + ' ' + args.pop(2)
        name = args[1]
        info = address_book.export(name,'phone')
        if info == -1:
            print('Error: contact not found')
            return;
        else:
            number, carrier = info
    elif args[0] == 'contact' and not addon:
        print('Error: address_book module not found')
        return;
    else:
        number = args[0]
        carrier = args[1]
    couldFindCarrier = True
    if carrier not in carrierCodes:
        couldFindCarrier = False
        print('Error: unrecognized carrier.')
    else:
        toAddress = number + carrierCodes[carrier]
        fromAddress = input('\'From\' address: ')
        password = getpass.getpass()
        messages = parseTXT(input('Message: '))
        for segment in messages:
            send(self, segment, fromAddress, password, toAddress)

def parseTXT(message):
# split the message into parts smaller than 150 characters, 
# preferably at spaces
    messages = int(len(message)/150)
    messageList = [''] * (messages + 1)
    i = 0
    while len(message) > 150:
        temp = message[:message[:150].rfind(' ')]
        messageList[i] = temp
        message = message[message[:150].rfind(' '):]
        i += 1
    messageList[messages] = message
    return messageList
    
def send(self, msg, fromAddress, password, toAddress):
    # Create a text/plain message
    message = MIMEText(msg)
    message['Subject'] = ''
    message['From'], message['To'] = fromAddress, toAddress
    mailHost = message['From']
    mailHost = mailHost[mailHost.index('@')+1:]
    try:
        s = smtplib.SMTP(serverDict[mailHost][0],serverDict[mailHost][1])
    except KeyError:
        print('Error: could not find server for ' + mailHost)
    s.ehlo()
    s.starttls()
    try:
        if self.simpleDecrypt(self.settingsList['password'][0]) is '':
         try:
            s.login(message['From'], getpass.getpass('password: '))
         except smtplib.SMTPAuthenticationError:
            password = getpass.getpass('Invalid password: ')
            while password != 'quit':
              try:
                s.login(message['From'], password)
                password = 'quit'
              except smtplib.SMTPAuthenticationError:
                password = getpass.getpass('Invalid password: ')
        else:
         try:
            s.login(message['From'], self.simpleDecrypt(self.settingsList['password'][0]))
         except smtplib.SMTPAuthenticationError:
            password = getpass.getpass('Error: unrecognized password in "settings.tool". Password: ')
            while password != 'quit':
              try:
                s.login(message['From'], password)
                password = 'quit'
              except smtplib.SMTPAuthenticationError:
                password = getpass.getpass('Invalid password: ')
        
        s.send_message(message)
    except smtplib.SMTPServerDisconnected:
        print('Connection terminated by server: connection timed out.')
    s.quit()
    
serverDict = {  'gmail.com':('smtp.gmail.com', 587),
                'hotmail.com':('smtp.live.com', 587),
                'yahoo.com':('smtp.mail.yahoo.com', 995),
                'msn.com':('smtp.live.com', 587),
                'live.com':('smtp.live.com', 587)}
func_alias = 'txt'
func_info = (emailToSMS,
             2,
             4,
             'Sends text messages through gmail; txt <number> <carrier>',
             False,
             )
