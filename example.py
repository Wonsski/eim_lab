from eim import Measurement


mes = Measurement("/dev/tty.usbserial-14310")

mes.testConnection()


x = [1,2,3,4]
out = mes.measure(x, "SEM1", "SEM2")

mes.createGraph(x, out, "SEM1 [V]", "SEM2 [V]")