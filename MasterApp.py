from controllers.MasterController import MasterController
from controllers.status.StatusController import StatusController
from model.Status import Status
from model.StatusSystem import StatusSystem
from model.StatusSlave import StatusSlave
from model.Raspberry import Raspberry
from util.Parser import Parser




def main():
 MasterController.getStatus()
 # MasterController.getImages()
 #StatusController.update(Status(True,'2023-12-2525'))

if __name__ == "__main__":
    main()
   # Api.app.run(host='0.0.0.0', port=5000)

