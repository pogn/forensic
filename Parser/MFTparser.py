import sys
import struct
from time import sleep
from datetime import datetime,timedelta

CLUSTER_SIZE = 0x400
u32 = lambda x:struct.unpack('<L',x)[0]
u64 = lambda x:struct.unpack('<Q',x)[0]

def error(err):
	print "[Error] "+err
	sys.exit(-1)

def parser(mfp):
	for i in xrange(len(mft)/CLUSTER_SIZE):
		baseidx = i*CLUSTER_SIZE + 0x38
		
		header1_size = u32(mft[baseidx + 4: baseidx + 8])

		header2 = baseidx + header1_size
		header2_flag = u32(mft[header2: header2 + 4])
		header2_size = u32(mft[header2 + 4: header2 + 8])
		if header2_flag == 0x20:
			header2 = header2 + header2_size

		header3 = header2
		header3_flag = u32(mft[header3: header3+4])
		if header3_flag != 0x30:
			continue

		us = u64(mfp[header3+0x20: header3+0x20+8])/10.
		created_time = datetime(1601,1,1) + timedelta(microseconds=us)
		file_len = ord(mfp[header3+0x58])
		file_name = str(mfp[header3+0x5a: header3+0x5a+file_len*2]) 

		print "CLUSTER IDX  : "+str(i)
		print "CREATED TIME : "+str(created_time)
		print "FILE NAME    : "+file_name
		sleep(0.5)

if len(sys.argv)<2:
	error("Usage : "+sys.argv[0]+" FILENAME")


if __name__ == '__main__':
	mft_name = sys.argv[1] 
	mft = open(mft_name,'rb').read()
	parser(mft)

