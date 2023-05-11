## Command to build exe
```
pyinstaller --onefile --add-data "s3_service.py;." --add-data "random_util.py;." --collect-data "docxcompose" --paths "Lib/site-packages" ui.py
```