# BackBlaze Backup

pushes the content of a folder (and all its subdirectories) to [backblaze](https://www.backblaze.com/)

## Set up

install b2upload

`pip install b2upload`

create a `.backblaze` in your home directory
it should contain the following :

```
[backblaze]
accountId = <your-account-id>
applicationKey = <your-application-key>
```


## usage

to upload all files and subfolders of the current directory

`b2upload --bucket <bucket-name>`

to upload all files and subfolders of a specific directory

`b2upload --bucket <bucket-name> --directory <absolute-path-to-dir>`
