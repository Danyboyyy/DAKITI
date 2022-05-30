import utils

class Memory:
    def __init__(self):
        self.localInt = 1000
        self.localFloat = 2000
        self.localBool = 3000
        self.localString = 4000

        self.globalInt = 5000
        self.globalFloat = 6000
        self.globalBool = 7000
        self.globalString = 8000

        self.constantInt = 9000
        self.constantFloat = 10000
        self.constantBool = 11000
        self.constantString = 12000

        self.tempInt = 13000
        self.tempFloat = 14000
        self.tempBool = 15000
        self.tempString = 16000
        self.tempPointer = 17000

    def freeLocalMemory(self):
        self.localInt = 1000
        self.localFloat = 2000
        self.localBool = 3000
        self.localString = 4000

    def freeTempMemory(self):
        self.tempInt = 13000
        self.tempFloat = 14000
        self.tempBool = 15000
        self.tempString = 16000

    def allocMemory(self, scope, type, size):
        if scope == 'local':
            if type == 'int':
                if self.localInt < 2000:
                    self.localInt = self.localInt + size
                    return self.localInt - size
                else:
                    utils.showError('Ran out of memory for local int variables!')
            elif type == 'float':
                if self.localFloat < 3000:
                    self.localFloat = self.localFloat + size
                    return self.localFloat - size
                else:
                    utils.showError('Ran out of memory for local floal variables!')
            elif type == 'bool':
                if self.localBool < 4000:
                    self.localBool = self.localBool + size
                    return self.localBool - size
                else:
                    utils.showError('Ran out of memory for local bool variables!')
            elif type == 'string':
                if self.localString < 5000:
                    self.localString = self.localString + size
                    return self.localString - size
                else:
                    utils.showError('Ran out of memory for local string variables!')
            else:
                utils.showError('No such specified data type!')
        elif scope == 'global':
            if type == 'int':
                if self.globalInt < 6000:
                    self.globalInt = self.globalInt + size
                    return self.globalInt - size
                else:
                    utils.showError('Ran out of memory for global int variables!')
            elif type == 'float':
                if self.globalFloat < 7000:
                    self.globalFloat = self.globalFloat + size
                    return self.globalFloat - size
                else:
                    utils.showError('Ran out of memory for global floal variables!')
            elif type == 'bool':
                if self.globalBool < 8000:
                    self.globalBool = self.globalBool + size
                    return self.globalBool - size
                else:
                    utils.showError('Ran out of memory for global bool variables!')
            elif type == 'string':
                if self.globalString < 9000:
                    self.globalString = self.globalString + size
                    return self.globalString - size
                else:
                    utils.showError('Ran out of memory for global string variables!')
            else:
                utils.showError('No such specified data type!')
        elif scope == 'constant':
            if type == 'int':
                if self.constantInt < 10000:
                    self.constantInt = self.constantInt + size
                    return self.constantInt - size
                else:
                    utils.showError('Ran out of memory for constant int variables!')
            elif type == 'float':
                if self.constantFloat < 11000:
                    self.constantFloat = self.constantFloat + size
                    return self.constantFloat - size
                else:
                    utils.showError('Ran out of memory for constant floal variables!')
            elif type == 'bool':
                if self.constantBool < 12000:
                    self.constantBool = self.constantBool + size
                    return self.constantBool - size
                else:
                    utils.showError('Ran out of memory for constant bool variables!')
            elif type == 'string':
                if self.constantString < 13000:
                    self.constantString = self.constantString + size
                    return self.constantString - size
                else:
                    utils.showError('Ran out of memory for constant string variables!')
            else:
                utils.showError('No such specified data type!')
        elif scope == 'temp':
            if type == 'int':
                if self.tempInt < 14000:
                    self.tempInt = self.tempInt + size
                    return self.tempInt - size
                else:
                    utils.showError('Ran out of memory for temp int variables!')
            elif type == 'float':
                if self.tempFloat < 15000:
                    self.tempFloat = self.tempFloat + size
                    return self.tempFloat - size
                else:
                    utils.showError('Ran out of memory for temp float variables!')
            elif type == 'bool':
                if self.tempBool < 16000:
                    self.tempBool = self.tempBool + size
                    return self.tempBool - size
                else:
                    utils.showError('Ran out of memory for temp bool variables!')
            elif type == 'string':
                if self.tempString < 17000:
                    self.tempString = self.tempString + size
                    return self.tempString - size
                else:
                    utils.showError('Ran out of memory for temp string variables!')
            elif type == 'pointer':
                if self.tempPointer < 18000:
                    self.tempPointer = self.tempPointer + size
                    return self.tempPointer - size
                else:
                    utils.showError('Ran out of memory for temp string variables!')
            else:
                utils.showError('No such specified data type!')
