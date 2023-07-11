Mled = False
TLed = False
LLed = False
if 3 > 2:
	Mled = True

if 2 > 3:
	TLed = True

if 5 > 6:
	LLed = True

if Mled or TLed or LLed:
	print('works')
else:
	print('no')
