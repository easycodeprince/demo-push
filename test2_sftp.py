import pysftp
import os


class Sftp:
    def __init__(self, hostname, username, password, port=22):
        """Constructor Method"""
        self.connection = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port

        # Disable host key checking (only for testing — NOT RECOMMENDED FOR PRODUCTION)
        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None

    def connect(self):
        """Connects to the SFTP server"""
        try:
            self.connection = pysftp.Connection(
                host=self.hostname,
                username=self.username,
                password=self.password,
                port=self.port,
                cnopts=self.cnopts
            )
            print(f"✅ Connected to {self.hostname} as {self.username}.")
        except Exception as err:
            print(f"❌ Connection failed: {err}")
            self.connection = None

    def disconnect(self):
        """Closes the SFTP connection"""
        if self.connection:
            self.connection.close()
            print(f"🔌 Disconnected from host {self.hostname}")
        else:
            print("⚠️ No active connection to close.")


if __name__ == "__main__":
    # Replace with actual values or environment variables
    hostname = 'us-east-1.sftpcloud.io'
    username = '078eb58773ef461590fbfa84b3f71d92'
    password = 'q0PODeEre8bbHG58dSInwnmulzrswTpn'
    port = 22

    sftp_client = Sftp(hostname, username, password, port)
    sftp_client.connect()

    if sftp_client.connection and sftp_client.connection.exists('.'):
        print("✅ SFTP connection is active.")
    else:
        print("❌ SFTP connection failed or not active.")

    # sftp_client.disconnect()


