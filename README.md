# ~ AI Media Pool Sorter ~
Automatically organizes your Media Pool in DaVinci Resolve!

Based on your clip's file name, it will be sorted into the most fitting bin of your Media Pool.

![MP_Sorter](https://github.com/neezr/AI-Media-Pool-Sorter-for-DaVinci-Resolve/assets/145998491/1ce5a499-a371-484f-b394-eb1e1858443e)


## Usage:
- Import your footage to your Media Pool and create the sub-bins, where you want your footage to be sorted into
	- Tip: For best results, avoid broad categories like "video" and "audio".
- Run this script from DaVinci Resolve's dropdown menu (Workspace > Scripts)
- Every clip in your Media Pool (excluding Timelines) will automatically be sorted into the sub-bin with the most fitting name

## Install:
- Copy the .py-file into the folder "%appdata%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility"
- *Windows Only:* Install Python 3.7+
- Install the python module 'transformers'
	- open 'cmd' on Windows and execute 'pip install transformers' in the command line
	- or: install via requirements.txt with 'pip install -r requirements.txt'

## Acknowledgements

- The classification from file name to sub-bin category is handled by Facebook's *BART (large) MNLI* model
- for more information, see: https://huggingface.co/facebook/bart-large-mnli
