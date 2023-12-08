import pynput
from pynput.keyboard import Key, Listener
import time

keys = []
start_time = time.time()

def on_press(key):

    end_time = time.time()
    elapsed_time = end_time - start_time
    keys.append((key, elapsed_time))
    write_file(keys)
    
    try:
        print()
        print("--------------------------------------------------")
        print('Key: {0}, Time: {1} seconds'.format(key.char, elapsed_time))
        
    except AttributeError:
        print('Special Key: {0}, Time: {1} seconds'.format(key, elapsed_time))
        
def write_file(keys):

    with open('log.csv', 'w') as f:
        f.write('Name,Key,Time\n')  
        for key, timestamp in keys:
            k = str(key).replace("'", "")
            f.write(f'{user},{k},{timestamp}\n')  
            
def on_release(key):
    #print('{0} released'.format(key)) # key release event
    if key == Key.esc:
        return False

def main():

    global user
    user = input("Enter Your Name: ")
    print()
    print("--- Beginning Keylogger Program (ESC to Exit) ---")
    print()

    with Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()