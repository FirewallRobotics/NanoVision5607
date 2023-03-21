'''
   
   MIT License
   
   Copyright (c) 2023
   
   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:
   
   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.
   
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
   
   FRC Team Firewall 5607
   - File: team5607NetworkTables.py 
   - CurrentYear:  2023
   - CreationDay: 6 
   - Date: Fri Mar 17 2023 
   - Username: wendydarby 
   
   
'''

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

   

    def updateTable(self,tableKV):
        for key in tableKV:
            self.tableKV[key] = tableKV[key]
            self.sd.putNumber(f'{key}',tableKV[key])

    def __init__(self, server="10.56.7.2", tableName="apriltag"):
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