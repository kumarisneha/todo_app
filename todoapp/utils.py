# working of MD5 (string - hexadecimal)
import hashlib

def hashed_func(string):
	# encoding string using encode() then sending to md5()
	result = hashlib.md5(string.encode())
	# hash_update = m.update(str(string))
	hash_str = result.hexdigest()
	return hash_str