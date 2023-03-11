from networktables import NetworkTables

class visionTable:
    
    targetType={
            "apriltTag": {
                "hue": [83, 120],
                "sat": [112, 255],
                "val": [110, 255],
                "color": (0,0,255), # RGB red
                "image": "opencv/source_real_red.jpeg"
            } ,
            "cone":  {
                "hue":  [121, 180],
                    "sat": [135, 255],
                    "val": [108, 255],
                    "color": ((255, 242, 0)), # RGB yellow
                    "image": "opencv/source_real_red.jpeg"
            },
            "cube":  { #what values do we really want to store for each target type??
                    "hue":  [121, 180],
                    "sat": [135, 255],
                    "val": [108, 255],
                    "color": (255,0,0), # RGB blue
                    "image": "opencv/source_real_blue.jpeg"
                
            
            }
        }
    
    tables={
        "apriltag": ["center_x", "center_y", "rotation", "area", "pose"],
        "cube":[],
        "cone":[],
        "reflective_tape":[]
    }

    def __init__(self, server="roborio-5607-frc.local", tableName="apriltag"):
        self.server=server
        self.tableName=tableName
        NetworkTables.initialize(server)
        self.tableKeys = [label for label in self.tables[tableName] ]
        self.sd = NetworkTables.getTable(self.tableName)
        
       
        # Initialize each key in the table with a -1
        self.tableKV={key: -1 for key in self.tableKeys}
        self.updateTable(self.tableKV)
        #use ntporperty to access NetworkTables vairables like a normal vairable
      #  visionTable = ntproperty('/SmartDashboard/apriltag', self.tableKV)
        
        print("Vision Netwok Table Initialized")

    def updateTable(self,tableKV):
        for key in tableKV:
            self.tableKV[key] = tableKV[key]
            self.sd.putNumber(f'{key}',tableKV[key])