# Uploaded poster template  

Meets size requirement  
1 MB 500 dpi resultions file, 24 bit color  
16:9 aspect ratio, 6667 x 3750
PowerPoint export to .jpg format.  
Change registry:  
windows search bar, "regedit"  
HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\PowerPoint
Options subkey  
Edit, New key, 
Select, Edit, Modify -- to rename  
Select, Edit, Modify -- to change value, decimal, 500.  Worked.

If there is no "Options" subkey, I suggest you create one manually, and then following the steps in '
Step 1: Change the export resolution setting' to create ExportBitmapResolution (DWORD (32-bit)).

(Serious problems might occur if you modify the registry incorrectly. Before you modify it, please remember to back up the registry for restoration in case problems occur.)
