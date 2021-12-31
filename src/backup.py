import os
import subprocess


class BackupHandler:
    def __init__(self):
        """
            in order to set environment variables.
        """
        try:
            # database related environment variables
            self.DATABASE_NAME = os.environ.get('DATABASE_NAME') # only nessecery for single db backup.
            self.DATABASE_USER = os.environ['DATABASE_USER']
            self.DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
            self.DATABASE_PORT = os.environ['DATABASE_PORT']
            self.DATABASE_HOST = os.environ['DATABASE_HOST']

            # set PGPASSWORD environment variable to prevent repeating password as an input in terminal for pg_dumpall
            os.environ['PGPASSWORD'] = self.DATABASE_PASSWORD

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
                 f'--dbname=postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}',
                 '-f', '.TempBackupFiles/temp_backup.sql'],
                stdout=subprocess.PIPE
            )

            result = backup_process.communicate()[0]
            process_failed = int(backup_process.returncode)!= 0

            if process_failed:
                print(f'command failed. return code : {backup_process.returncode}')
                exit(1)

            return result

        except Exception as error:
            print(f'process failed due to : {error}')
            os.remove('.TempBackupFiles/temp_backup.sql')
            exit(1)

        except KeyboardInterrupt as intrupt:
            os.remove('.TempBackupFiles/temp_backup.sql')
            raise intrupt
    


    def backup_all(self):
        """
            get backup from the entire engine
        """
        try:
            backup_process = subprocess.Popen(
                ['pg_dumpall',
                 f'--dbname=postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}',
                 '-f', '.TempBackupFiles/temp_backup_all.sql'],
                stdout=subprocess.PIPE
            )

            result = backup_process.communicate()[0]
            process_failed = int(backup_process.returncode)!= 0

            if process_failed:
                print(f'command failed. return code : {backup_process.returncode}')
                exit(1)

            return result

        except Exception as error:
            print(f'process failed due to : {error}')
            os.remove('.TempBackupFiles/temp_backup_all.sql')
            exit(1)

        except KeyboardInterrupt as intrupt:
            os.remove('.TempBackupFiles/temp_backup_all.sql')
            raise intrupt
    


if __name__ == '__main__':
    # <temporary> tests
    handler = BackupHandler()
    
    handler.backup_all()
    handler.backup_single_db()