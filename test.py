import paramiko

def test_sftp_connection(host, port, username, password):
    transport = None
    sftp = None

    try:
        # Connect to SFTP
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        # Try listing root directory
        files = sftp.listdir('.')
        print("✅ Connected to SFTP successfully.")
        print("Contents of root directory:", files)

        return True
    except Exception as e:
        print(f"❌ Failed to connect to SFTP: {e}")
        return False
    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()


# Example usage
if __name__ == "__main__":
    test_sftp_connection(
        host="your-sftp-host.com",
        port=22,
        username="your-username",
        password="your-password"
    )
