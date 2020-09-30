import sys
import os
import time
import serial

# serial settings
s_con = "COM3"
s_baud = 115200

class att6000:
  # init class att6000 and init uart
  def __init__(self, s_con, s_baud, dbg_print=False, timeout=0.1):
    self.dbg_print = dbg_print
    self.ser = serial.Serial(s_con, s_baud, timeout=0.1)
  
  # write decibel to att6000 after sanity checks
  # the "ATT.exe" only allows values < 32dB in 0.25dB steps
  def set(self, db):
    if(round(abs(db)*4)/4 > 32):
      if self.dbg_print:
        print("FAIL", db)
      return
    # assemble command: (round absolute dB value to quarters) * 100
    cmd = "wv0{:04}\n".format(int((round(abs(db)*4)/4)*100))
    if self.dbg_print:
      print("{:05.2f} >> {}".format(db, cmd.encode()))
    self.ser.write(cmd.encode())
    # device always answers with "ok\r\n", so this is a bit redundant
    r = self.ser.readline().decode()
    if not r.startswith("ok"):
      if self.dbg_print:
        print("FAIL", cmd.encode())
      return 
    else:
      if self.dbg_print:
        print("OK", r.encode())
      
# MAIN TEST
# goes through all dB steps indefinitely
def main():
  while 1:
    for i in range(0, 4000, 7):
      i = i / 100.0
      at.set(i);
    time.sleep(0.5)


if __name__ == '__main__':
  try:
    at = att6000(s_con, s_baud, True)
    main()    
  except KeyboardInterrupt:
    print("KeyboardInterrupt\nexiting...")
    sys.exit(0)
  except SystemExit:
    print("SystemExit\nexiting...")
    os._exit(0)

