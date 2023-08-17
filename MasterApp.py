from controllers.MasterController import MasterController
from controllers.status.StatusController import StatusController
from model.Status import Status

def main():
  MasterController.getImages()
 #StatusController.update(Status(True,'2023-12-2525'))

if __name__ == "__main__":
    main()
   # Api.app.run(host='0.0.0.0', port=5000)

