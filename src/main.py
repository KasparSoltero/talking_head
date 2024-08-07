from src.controller import HeadController

import time

def main():
    controller = HeadController()
    while True:
        controller.update()
        time.sleep(0.1)

if __name__ == '__main__':
    main()