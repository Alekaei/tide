import re

def _process_string(string):
	string = re.sub('\\033\[(?:\d;|\d)+\w', '', string)

def write(x, string, message):
	splits = re.sub('(\\033\[(?:\d;|\d)+\w)', r',\1,', string).split(',')
	msg_splits = re.sub('(\\033\[(?:\d;|\d)+\w)', r',\1,', message).split(',')
	msg_len = len(''.join([msg_splits[x] for x in range(0, len(msg_splits), 2)]))

	line_index = 1

	split_start_index = 0
	start_index = -1
	end_index = -1

	for i in range(0, len(splits), 2):
		if splits[i] == '':
			continue
		line_index += len(splits[i])
		if line_index < x:
			continue
		if start_index == -1:  # ON START INDEX
			split_start_index = i
			start_index = x - (line_index - len(splits[i]))
			end_index = start_index + msg_len + 1
			
			if msg_len < line_index - start_index:  # Account for extra leftover string
				line = splits[i] 
				splits[i] = line[:start_index]
				if i > 0:  # copy color over
					splits.insert(i + 1 if x > 0 else 0, splits[i - 1])
					splits.insert(i + 2 if x > 0 else 1, line[start_index + msg_len:])
				else:
					splits.insert(i + 1 if x > 0 else 0, line[start_index + msg_len:])
				splits.insert(i + 1 if x > 0 else 0, message)
				return ''.join(splits)
			splits[i] = splits[i][:start_index]
		elif end_index > line_index:  # EVERYTHING BETWEEN
			del splits[i]
			del splits[i - 1]
		else:  # ON END INDEX
			splits[i] = splits[i][end_index - line_index:]
	splits.insert(split_start_index + 1 if x > 0 else 0, message)
	return ''.join(splits)
