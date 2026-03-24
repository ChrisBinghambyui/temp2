from colorama import init, Fore, Back, Style

# Initialize colorama (needed for Windows)
init()

print(Fore.RED + 'This text is red')
print(Back.GREEN + 'This text has a green background')
print("Test")
print(Style.BRIGHT + 'This text is bright' + Style.RESET_ALL)
print("Test")
print('Back to normal')

print(Back.WHITE + Fore.BLACK + Style.BRIGHT + f"\nCannot add die!" + Style.RESET_ALL)

x=5

