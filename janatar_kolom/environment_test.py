import os, platform

def getPlatform():
    environment = platform.uname()

    if (environment.processor == 'x86_64'):
        return "Production"
    else:
        return "Development"