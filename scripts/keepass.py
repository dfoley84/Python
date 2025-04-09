from pykeepass import PyKeePass
import secrets
import string

def generate_random_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

client = 'TEST'
kp = PyKeePass('Database.kdbx', password='CHANGEME')

with open('test_public_key.pem', 'rb') as key_file:
    public_key_data = key_file.read()

sftp_group = kp.find_groups(name='SFTP', first=True)
random_password = generate_random_password()

entry = kp.add_entry(
    sftp_group,
    title=f'{client} SFTP',
    username=f'{client}_ops',
    password= random_password,
    url='sftp://example.com',
    notes=f'{client} SFTP Credentials'
)
binary_id = kp.add_binary(public_key_data)
print(kp.binaries)
a = entry.add_attachment(binary_id, f'{client}_ops_private_key.pem')
kp.save()
