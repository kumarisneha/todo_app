
import hashlib

def hashed_func(string):
	m = hashlib.md5()
	hash_update = m.update(str(string))
	hash_str = m.hexdigest()
	return hash_str
