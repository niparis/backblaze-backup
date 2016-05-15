B2 upload - a script to backup a folder to BackBlaze
====================================================

b2upload pushes the content of a folder (and all its subdirectories) to backblaze_

It will authenticate you, create the bucket if needed, and push only files that are not already present in the backblaze bucket.

Set up
------

- install b2upload

``pip install b2upload``

- create a ``.backblaze`` in your home directory
it should contain the following::

	[backblaze]
	accountId = <your-account-id>
	applicationKey = <your-application-key>



Usage
-----

- to upload all files and subfolders of the current directory

``b2upload --bucket <bucket-name>``

- to upload all files and subfolders of a specific directory

``b2upload --bucket <bucket-name> --directory <absolute-path-to-dir>``


.. _backblaze: https://www.backblaze.com/
