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

# Процедура получения СRC16 Modbus
def GetCRC16(InByteArr):
	crc16 = crcmod.predefined.Crc('modbus')
	crc16.update(InByteArr)
	ResCRC16 = crc16.digest()
	ResCRC16 = ResCRC16[::-1]
	return ResCRC16
# -------------------------------------

# Процедура провекри CRC16 Modbus
def CheckCRC16(InByteArr):
	crc16 = crcmod.predefined.Crc('modbus')
	crc16.update(InByteArr[0:len(InByteArr)-2])
	ResCRC16 = crc16.digest()
	ResCRC16 = ResCRC16[::-1]
	return ResCRC16 == InByteArr[len(InByteArr)-2:len(InByteArr)]
# -------------------------------------

# Процедура формирования запроса на чтение текущих показаний для РСМ 05.05
def GetReqRSM0505(InDeviceId):
	LArr = bytes([InDeviceId,		#Номер адреса RS485
					3,				#Номер команды - чтение Holding Registers
					0,0,			#Номер первого параметра 
					1,61])			#Количество считываемых параметров 
	LArr = AddCRC16(LArr)
	return LArr
# -------------------------------------

# Процедура обмена данными с удаленным устройством
def SendGetData(InRecSGD):
	ResId = None
	ErrorText = None
	LData = b""
	try:
		Conn = socket.socket()
		Conn.connect((InRecSGD.Hostname, InRecSGD.Port))
		Conn.settimeout(InRecSGD.ConnTimeout)
		IConnTry = 0
		for i in range(InRecSGD.ConnTries):
			IConnTry =+ 1
			LData = b""
			Conn.send(InRecSGD.ReqArr)
			if InRecSGD.ResArrCnt > 0:
				try:
					tmp = Conn.recv(InRecSGD.ResArrCnt)
					while tmp:
						LData += tmp
						tmp = Conn.recv(InRecSGD.ResArrCnt-len(LData))
				except Exception as e:
					ResId = 255
					print(str(e))
					ErrorText = str(e)

			else:   #Написать процедуру чтения данных по таймауту
				ResId = 2
				ErrorText = "Не указано количество ожидаемых в ответе байт"
			if (len(LData) == InRecSGD.ResArrCnt):
				if not CheckCRC16(LData):
					ResId = 3
					ErrorText = "Не корректный CRC"
				else:
					break
			else:
				ResId = 4
				ErrorText = "Длина ответа не совпала"
	except Exception as e:
		if e.errno == 111:
			ResId = 1
			ErrorText = "Ошибка подключения к оборудованию"
		else:
			ResId = 255
			ErrorText = str(e)
	else:
		ResId = 0
		ErrorText = None
	finally:
		Conn.close()
	return ResId, ErrorText, LData
# -------------------------------------

# Описание типов (кортежей)

# Кортеж для передачи в процедуру SendGet
RecSendGetData = namedtuple('RecSendGetData', [
				'Hostname',
				'Port',
				'ConnTries',
				'ConnTimeout',
				'ReqArr',
				'ResArrCnt'])
#-------------------
# Кортеж для текущий показаний с РСМ 05.05
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
#--------------------------------------
#-------- Конец блока описания типов (кортежей)-------------

print(crcmod.__file__)




ReqBytes = GetReqRSM0505(2)
print(ReqBytes.hex())

ResId, ErrorText, Response = SendGetData(RecSendGetData("10.8.0.22",
						36369,
						3,
						10,
						ReqBytes,
						
						639))
if ResId != 0:
	print(ErrorText)
else:
	Res = ResCurrent._make(struct.unpack('>BBBf294sL60sif88siiiiiiiii58sHHH9sBBBBBBB56siBB', Response))
	print(Res.PUNumber)
	print(Res.CurrDischarge)
	print(Res.WorkTimeAll)

quit()




# print(struct.calcsize('<BBBf294sL60sif88siiiiiiiii58sHHH9sBBBBBBB56sih'))

# Определяем процедуру расчета CRC16 для расширения crcmod
#crc16 = crcmod.predefined.Crc('modbus')

# Задаем запрос на получение текущих данных


#ReqBytes = bytes([2,3,0,0,1,61])
# ReqBytes = AddCRC16(bytes([2,3,0,0,1,61]))
# print(ReqBytes.hex())
# ReqBytes = GetCRC16(bytes([2,3,0,0,1,61]))
# print(ReqBytes.hex())

#ReqBytes = CheckCRC16(bytes([2,3,0,0,1,61,133,184]))
#print(ReqBytes)




# crc16.update(ReqBytes)
# ResCRC16 = crc16.digest()
# ResCRC16 = ResCRC16[::-1]
# ReqBytes += ResCRC16


#my_bytes += bytes([133,184])




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






# conn = socket.socket()

# conn.connect( ("10.8.0.22", 36369) )


# conn.settimeout(10)
# print(conn)






# 'BBBf294sL60sif88siiiiiiiii58sHHH9sBBBBBBB56si2s'






# print (my_bytes)


# Проверка полученного результат
# Проверка №1 по длине результат (длина ответа должна быть равна 639 байт)






#print(struct.calcsize('>BBBf294sL60sif88siiiiiiiii58sHHH9sBBBBBBB56siBB'))


# print(data[0:637].hex())
# crc16.update(data[0:637])
# ResCRC16 = crc16.digest()

# ResCRC16 = ResCRC16[::-1]
# print(ResCRC16.hex())

# print(data[637:639].hex())




# Res = ResCurrent._make(struct.unpack('>BBBf294sL60sif88siiiiiiiii58sHHH9sBBBBBBB56siBB', data))


# print(Res)
# print("--------------------------------------------------")


# print(Res.CheckSum1)


# #print(Res.PUNumber)
# #print(data.decode("utf-8"))
# conn.close()