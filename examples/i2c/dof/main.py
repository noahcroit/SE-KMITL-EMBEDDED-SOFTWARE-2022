from dof import *



qmi8658=QMI8658()
while True:
    xyz=qmi8658.Read_XYZ()
    print("ACC_X={:+.2f} ACC_Y={:+.2f} ACC_Z={:+.2f}".format(xyz[0],xyz[1],xyz[2]))
    print("GYR_X={:+3.2f} GYR_Y={:+3.2f} GYR_Z={:+3.2f} \r\n".format(xyz[3],xyz[4],xyz[5]))
    time.sleep(1)

