import os
import subprocess


class BackupHandler:
    def __init__(self):
        """
            in order to set environment variables.
        """
        try:
            # database related environment variables
            self.__DATABASE_NAME = os.environ.get('DATABASE_NAME') # only nessecery for single db backup.
            self.__DATABASE_USER = os.environ['DATABASE_USER']
            self.__DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
            self.__DATABASE_PORT = os.environ['DATABASE_PORT']
            self.__DATABASE_HOST = os.environ['DATABASE_HOST']
            self.__TEMP_DIR_STORE_FILES = os.environ['TEMP_DIR_STORE_FILES']

            # set PGPASSWORD environment variable to prevent repeating password as an input in terminal for pg_dumpall
            os.environ['PGPASSWORD'] = self.__DATABASE_PASSWORD

        except Exception as none_error:
            print(f'can not continue the process due to : {none_error}')
            exit(0)


    def backup_single_db(self):
        """
            get backup from a single database which its name has been given in environment variables as `DATABASE_NAME`
        """
        try:
            backup_process = subprocess.Popen(
                ['pg_dump',
                 f'--dbname=postgresql://{self.__DATABASE_USER}:{self.__DATABASE_PASSWORD}@{self.__DATABASE_HOST}:{self.__DATABASE_PORT}/{self.__DATABASE_NAME}',
                 '-f', f'{self.__TEMP_DIR_STORE_FILES}/temp_backup.dump'],
                stdout=subprocess.PIPE
            )

            result = backup_process.communicate()[0]
            process_failed = int(backup_process.returncode)!= 0

            if process_failed:
                print(f'command failed. return code : {backup_process.returncode}')
                exit(1)

        except Exception as error:
            print(f'process failed due to : {error}')
            os.remove(f'{self.__TEMP_DIR_STORE_FILES}/temp_backup.dump')
            exit(1)

        except KeyboardInterrupt as intrupt:
            os.remove(f'{self.__TEMP_DIR_STORE_FILES}/temp_backup.dump')
            raise intrupt

        else:
            # set file names & path as environment variable
            os.environ['UPLOADING_FILE_PATH'] = f'{self.__TEMP_DIR_STORE_FILES}/temp_backup.dump'
            return result
    

    def backup_all(self):
        """
            get backup from the entire engine
        """
        try:
            backup_process = subprocess.Popen(
                ['pg_dumpall',
                 f'--dbname=postgresql://{self.__DATABASE_USER}:{self.__DATABASE_PASSWORD}@{self.__DATABASE_HOST}:{self.__DATABASE_PORT}',
                 '-f', f'{self.__TEMP_DIR_STORE_FILES}/temp_backup_all.dump'],
                stdout=subprocess.PIPE
            )

            result = backup_process.communicate()[0]
            process_failed = int(backup_process.returncode)!= 0

            if process_failed:
                print(f'command failed. return code : {backup_process.returncode}')
                exit(1)

        except Exception as error:
            print(f'process failed due to : {error}')
            os.remove(f'{self.__TEMP_DIR_STORE_FILES}/temp_backup_all.dump')
            exit(1)

        except KeyboardInterrupt as intrupt:
            os.remove(f'{self.__TEMP_DIR_STORE_FILES}/temp_backup_all.dump')
            raise intrupt

        else:
            # set file names & path as environment variable
            os.environ['UPLOADING_FILE_PATH'] = f'{self.__TEMP_DIR_STORE_FILES}/temp_backup_all.dump'
            return result
