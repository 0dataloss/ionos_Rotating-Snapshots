# IONOS Rotating Snapshot

This script can be used to implement automatic backup procedure using Snapshots in the IONOS infrastructure.
To make the script work you will have to export Username and Password as environment variable as following:

export IONOS_USERNAME="Your@username.com" && export IONOS_PASSWORD="yourpassw0rd"

The parameters needed by the scripts are:
- Datacenter_UUID
- Volume_UUID
- Server Tag (only alphanumeric char)
- Rate of backup:
    D for daily
    W for weekly
    M for monthly
    Q for quarterly
    Y for yearly

The script is designed to "rotate" the snapshots, as example, if you are taking daily backups every week the snapshot taken 7 days ago will be deleted and a new one taken.

# Examples
./rotating-snapshots.py DC_UUID Volume_UUID ServerTag DWMQY