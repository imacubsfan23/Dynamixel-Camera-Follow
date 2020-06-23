#pseudo-code for programming to servos with protocol 1.0
import dynamixel_sdk

def main():
    print("Please note that bytes are ordered from left-to-right as [0, 1, 2, 3] where Byte 0 is the least significant byte.\n")
    
    send_packet([255,13,2,0,0,0,0,0,0,0,0,0,(13+2+0+0+0+0+0+0+0+0+0)%256])
    readln = _serial.read(13)
    print(readln)
    _serial.close()

if __name__=='__main__':
    main()


    
