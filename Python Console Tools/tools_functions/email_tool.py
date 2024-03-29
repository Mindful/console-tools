import smtplib, sys, getpass, os, importlib
from email.mime.text import MIMEText

def email_tool(self,args):
    addon = False
    if os.path.exists('tools_functions\\address_book.py'):
        address_book = importlib.__import__('address_book')
        addon = True
    message = input('Enter message body: ')
    msg = MIMEText(message)
    msg['Subject'] = 'Sent from %s' % sys.argv[0]
    if args[0] == 'contact' and addon:
        if len(args) > 2:
            while len(args) > 2:
                args[1] = args[1] + ' ' + args.pop(2)
        name = args[1]
        info = address_book.export(name,'email')
        if info == -1:
            print('Error: contact not found')
            return;
        else:
            msg['To'] = info
    elif args[0] == 'contact' and not addon:
        print('Error: address_book module not found')
        return;
    else:
        msg['To'] = args[0]
    msg['From'] = input('\'From\' address: ')
    mailHost = msg['From']
    mailHost = mailHost[mailHost.index('@')+1:]
    try:
        s = smtplib.SMTP(serverDict[mailHost][0],serverDict[mailHost][1])
    except KeyError:
        print('Error: could not find server for ' + mailHost)
    s.ehlo()
    s.starttls()
    if self.simpleDecrypt(self.settingsList['password'][0]) is '':
     try:
        s.login(msg['From'], getpass.getpass('password:'))
     except smtplib.SMTPAuthenticationError:
        password = getpass.getpass('Invalid password: ')
        while password != 'quit':
          try:
            s.login(msg['From'], password)
            password = 'quit'
          except smtplib.SMTPAuthenticationError:
            password = getpass.getpass('Invalid password: ')
    else:
     try:
        s.login(msg['From'], self.simpleDecrypt(self.settingsList['password'][0]))
     except smtplib.SMTPAuthenticationError:
        password = getpass.getpass('Error: unrecognized password in "settings.tool". Password: ')
        while password != 'quit':
          try:
            s.login(msg['From'], password)
            s.send_message(msg)
            password = 'quit'
          except smtplib.SMTPAuthenticationError:
            password = getpass.getpass('Invalid password: ')
    s.quit()
    
def prompt_pass(prompt):
    print(prompt)
    return getpass.getpass()

    
serverDict = {  'gmail.com':('smtp.gmail.com', 587),
                'hotmail.com':('smtp.live.com', 587),
                'yahoo.com':('smtp.mail.yahoo.com', 995),
                'msn.com':('smtp.live.com', 587)}
#function reference, min args, max args, help info, case sensitive?, function name
func_alias = 'email'
func_info = (email_tool,
             1, 
             1, 
            'email <address> sends an email to the given address.',
            False,
            )
settings = {'subject': ('T', False), 'anonymous': ('F', False),'password':('', True),'toAddress':('WERP', False)}
