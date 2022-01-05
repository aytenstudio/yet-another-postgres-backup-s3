import asyncio
import aiocron
import os
from backup import BackupHandler
from upload import UploadHandler
from asgiref.sync import sync_to_async

class Main:
    def __init__(self):
        try:
            self.__SCHEDULE = os.environ['SCHEDULE']
        
        except Exception as none_error:
            print(f'can not continue the process due to {none_error}')
            exit(1)

    def run(self):
        @aiocron.crontab(f'{self.__SCHEDULE}')
        async def inner_run():

            # initial backup handler 
            backupHandler = BackupHandler()

            # get backup from the entire postgres
            await sync_to_async(backupHandler.backup_all)()

            # initial upload handler
            uploadHandler = UploadHandler()

            # upload backup file to minIO
            await sync_to_async(uploadHandler.upload_file)()

        return asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    Main().run()
