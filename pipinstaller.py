try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain

def install(package):
    pipmain(['install', package])

if __name__ == '__main__':
    install('asyncio')
    install('aiohttp')
    install('bs4')
    install('lxml')