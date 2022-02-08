This script can be used to implement automatic backup procedure using Snapshots in the IONOS infrastructure.
At the moment only the weekly backup has been implemented and will require this scrip to be set up as daily job.

The script will need as env var:
IONOS_USERNAME
IONOS_PASSWORD

The script needs as paramenters (in this order): Volume_UUID   Datacenter_UUID  Name_Of_The_Server(only alphanumeric char)

Using the 'Volume_UUID', the 'day of the week' and the 'Name_Of_The_Server', the script will be able to identify and delete
all the previous snapshots with the same values.

The script is designed to keep only 7 snapshot online, if you need to retain som eof the smnapshot created I suggest you change the 
Name_Of_The_Server, adding a number.
This action will make the script ignore the snapshot taken with the old name.