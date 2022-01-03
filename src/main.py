from backup import BackupHandler
from upload import UploadHandler


class Main:
    @staticmethod
    def main():
        # TODO phase2 bunch of codes...

        # initial backup handler 
        backupHandler = BackupHandler()

        # get backup from the entire postgres
        backupHandler.backup_all()

        # initial upload handler
        uploadHandler = UploadHandler()

        # upload backup file to minIO
        uploadHandler.upload_file()

if __name__ == '__main__':
    Main.main()
