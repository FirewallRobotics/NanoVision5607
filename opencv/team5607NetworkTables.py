from networktables import NetworkTables

class _team5607_NetworkTables:
    def __init__(self, server="roborio-5607-frc.local", tableName="cargo", tableKeys=[]):
        self.server=server
        self.tableName=tableName
        NetworkTables.initialize(server)
        self.sd = NetworkTables.getTable(self.tableName)
        self.tableKeys=tableKeys
        # Initialize each key in the table with a -1
        self.tableKV={key: -1 for key in self.tableKeys}
        self.updateTable(self.tableKV)
    def updateTable(self,tableKV):
        for key in tableKV:
            self.tableKV[key] = tableKV[key]
            self.sd.putNumber(f'{key}',tableKV[key])