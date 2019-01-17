#!/usr/bin/python3.6
# My first program on Python!369


import time
import socket
import struct
from collections import namedtuple
import crcmod
import array

# Процедура добавления СRC16 Modbus
def AddCRC16(InByteArr):
	crc16 = crcmod.predefined.Crc('modbus')
	crc16.update(InByteArr)
	ResCRC16 = crc16.digest()
	ResCRC16 = ResCRC16[::-1]
	ResBytes = InByteArr + ResCRC16
	return ResBytes
# -------------------------------------



# print(struct.calcsize('<BBBf294sL60sif88siiiiiiiii58sHHH9sBBBBBBB56sih'))

# Определяем процедуру расчета CRC16 для расширения crcmod
#crc16 = crcmod.predefined.Crc('modbus')

# Задаем запрос на получение текущих данных


#ReqBytes = bytes([2,3,0,0,1,61])
ReqBytes = AddCRC16(bytes([2,3,0,0,1,61]))



# crc16.update(ReqBytes)
# ResCRC16 = crc16.digest()
# ResCRC16 = ResCRC16[::-1]
# ReqBytes += ResCRC16


#my_bytes += bytes([133,184])
print(ReqBytes.hex())

quit()

#my_bytes = bytes([2,3,0,0,1,61,133,184])


# print(my_bytes[0:6].hex())

# crc16.update(my_bytes[0:6])
# ResCRC16 = crc16.digest()

# print(ResCRC16)

# ResCRC16 = ResCRC16[::-1]


# print(ResCRC16)
# print(my_bytes[6:8])
# if ResCRC16 == my_bytes[6:8] :
# 	print(True)
# else:
# 	print(False)

# #print(crc16.digest() >> 8)
# #print(crc16.crcValue & 0xFF)


# print("---------------------")

# print(my_bytes[6:8].hex())
# print(my_bytes.hex())


# quit()






conn = socket.socket()

conn.connect( ("10.8.0.22", 36369) )


conn.settimeout(10)
print(conn)






# 'BBBf294sL60sif88siiiiiiiii58sHHH9sBBBBBBB56si2s'

ResCurrent = namedtuple('ResCurrent', [
	'DeviceId',				#B
	'Command',				#B
	'ByteCnt',				#B
	'CurrDischarge', 		#f
	'Unk01',				#294s
	'RegErr',				#L
	'Unk02',				#60s
	'VolumeInt',			#i
	'VolumeFrac',			#f
	'Unk03',				#88s
	'EventCnt',				#i
	'MonthCnt',				#i
	'DayCnt',				#i
	'HourCnt',				#i
	'WorkTimeWOErr',		#i
	'WorkTimeAll',			#i
	'WorkTimeG1MinErr',		#i
	'WorkTimeG1MaxErr',		#i
	'WorkTimeTechErr',		#i
	'Unk04',				#58s
	'DU1',					#H
	'DU2',					#H
	'SysType',				#H
	'Unk05',				#9s
	'Year',					#B
	'Month',				#B
	'Day',					#B
	'DayOfWeek',			#B
	'Hour',					#B
	'Minute',				#B
	'Second',				#B
	'Unk06',				#56s
	'PUNumber',				#i
	'CheckSum1',			#B
	'CheckSum2'				#B
])




print (my_bytes)

conn.send(my_bytes)

data = b""
i = 0

tmp = conn.recv(639)
i += 1
print("len(tmp) = " + str(len(tmp)))
while tmp:
	data += tmp
	tmp = conn.recv(639-len(data))
	i += 1
	print(str(i) + " - len(tmp) = " + str(len(tmp)))
print("end loop")

# Проверка полученного результат
# Проверка №1 по длине результат (длина ответа должна быть равна 639 байт)






#print(struct.calcsize('>BBBf294sL60sif88siiiiiiiii58sHHH9sBBBBBBB56siBB'))


# print(data[0:637].hex())
# crc16.update(data[0:637])
# ResCRC16 = crc16.digest()

# ResCRC16 = ResCRC16[::-1]
# print(ResCRC16.hex())

# print(data[637:639].hex())




Res = ResCurrent._make(struct.unpack('>BBBf294sL60sif88siiiiiiiii58sHHH9sBBBBBBB56siBB', data))


print(Res)
print("--------------------------------------------------")


print(Res.CheckSum)


#print(Res.PUNumber)
#print(data.decode("utf-8"))
conn.close()