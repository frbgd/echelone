i = 0
for i in range(20, 30):
    print('  {')
    print('    "name": "test-fwmark-' + str(i + 1) + '",')
    print('    "description": "Метка ' + str(2**i) + '",')
    print('    "type": "Позитивный",\n    "NAME": "test",\n    "NET": "0.0.0.0",\n    "MASK": "255.255.255.0",\n    "VIA": "192.168.1.100",\n    "DEV": "eth0",')
    print('    "FWMARK": "' + str(2**i) + '",')
    print('    "resultNAME": "test",\n    "resultNET": "0.0.0.0",\n    "resultMASK": "255.255.255.0",\n    "resultVIA": "92.168.1.100",\n    "resultDEV": "eth0",')
    print('    "resultFWMARK": "' + str(2**i) + '"')
    print('  },')