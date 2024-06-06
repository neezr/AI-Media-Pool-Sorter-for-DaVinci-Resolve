#~ AI Media Pool Sorter ~
#created by nizar / version 1.0
#contact: http://twitter.com/nizarneezR

#Usage:
#Import your footage to your Media Pool and create the sub-bins, where you want your footage to be sorted into
#	Tip: For best results, avoid broad categories like "video" and "audio".
#Run this script from DaVinci Resolve's dropdown menu (Workspace > Scripts)
#Every clip in your Media Pool (excluding Timelines) will automatically be sorted into the sub-bin with the most fitting name

#Install:
#Copy this .py-file into the folder "%appdata%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility"
#Install the python module 'transformers'
#	open cmd and execute 'pip install transformers' in the command line
#	or: install via requirements.txt with 'pip install -r requirements.txt'

import os
import sys
import pickle
import platform
import tkinter

DEBUG_PRINT_LABEL_SCORES = False

def show_error_message(msg_text):
	root_errormsg = tkinter.Tk()
	root_errormsg.wm_title("Nizar's AI Media Pool Sorter for DaVinci Resolve")
	
	l_err_msg = tkinter.Label(root_errormsg, text=msg_text)
	l_err_msg.pack(side=tkinter.TOP, fill="x", pady=10)
	l_ok_button = tkinter.Button(root_errormsg, text="Okay", command=root_errormsg.destroy)
	l_ok_button.pack(side=tkinter.BOTTOM, fill="x", pady=10)
	
	root_errormsg.mainloop()

fusion_stderr = sys.stderr
sys.stderr = open(os.devnull, "w")
print("WARNING: stderr was changed to devnull during import.")
# this is a workaround
# transformers requires flushing, fu_stderr does not allow it though


# load/save classifier from/with pickle

if platform.system() == "Windows":
	pickle_path = os.path.expandvars(r"%USERPROFILE%\.cache\facebook_bart-large-mnli.pickle")
else: # MacOS, Linux and default (= linux)
	pickle_path = os.path.expanduser(r"~/.cache/facebook_bart-large-mnli.pickle")


if os.path.isfile(pickle_path):
	with open(pickle_path, "rb") as fh:
		classifier = pickle.load(fh)
	sys.stderr = fusion_stderr
	print("... stderr was changed back to ", sys.stderr)
else:
	try:
		from transformers import pipeline
		
		show_error_message(f"Thank you for using 'Nizar's AI Media Pool Sorter for DaVinci Resolve'\nBecause this is the first time using this script on this machine, the model will now be downloaded (1.5 GB) in the background.\n\nDepending on your internet speed, this may take some time.\n\n\nYou should find the downloaded file under: '{pickle_path}'")
		
		if not os.path.exists(os.path.dirname(pickle_path)):
			os.makedirs(os.path.dirname(pickle_path))
		
		classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
		with open(pickle_path, "wb") as fh:
			pickle.dump(classifier, fh)
			
		sys.stderr = fusion_stderr
		print("... stderr was changed back to ", sys.stderr)
	except ModuleNotFoundError:
		sys.stderr = fusion_stderr
		print("... stderr was changed back to ", sys.stderr)
		
		show_error_message("Module 'transformers' not found!\n\n'AI Media Pool Sorter' requires the external module 'transformers' for downloading the AI model from Huggingface.\nPlease install transformers by opening the command line interface and running 'pip install transformers'.")
	except Exception as e:
		sys.stderr = fusion_stderr
		print("... stderr was changed back to ", sys.stderr)
		print("unexpected error during import:\n\n", e)

sys.stderr = fusion_stderr
print("... stderr was changed back to ", sys.stderr)



def classify(mp_item_name, subfolders):
	subfolder_labels = [f.GetName() for f in subfolders]
	response = classifier(mp_item_name, subfolder_labels)
	if DEBUG_PRINT_LABEL_SCORES:
		print(response, "\n"*5)
	winning_name = response["labels"][0]
	for f in subfolders:
		if f.GetName() == winning_name:
			return f
	
	
def sort_media_pool():
	mp = resolve.GetProjectManager().GetCurrentProject().GetMediaPool()
	
	active_bin = mp.GetCurrentFolder()
	if not active_bin:
		active_bin = mp.GetRootFolder()
		
	subfolders = active_bin.GetSubFolderList()
	if not subfolders:
		show_error_message("No subfolders found. Add subfolders to the current bin. The AI model will then sort your clips into these bins.")
	else:
		mp_item_list = [item for item in active_bin.GetClipList() if not item.GetClipProperty("Type") == "Timeline"]
		if not mp_item_list:
			show_error_message("No clips found in current Media Pool folder. Add clips and subfolders to the current bin. The AI model will then sort your clips into these bins.")
		for mp_item in mp_item_list:
			mp_item_name = mp_item.GetClipProperty("Clip Name")
			target_folder = classify(mp_item_name, subfolders)
			mp.MoveClips([mp_item], target_folder)
		

if __name__ == "__main__":
	sort_media_pool()
	print("AI Media Pool Sorter is done!")
