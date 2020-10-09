# JSOB Questions & Answers

The mission is to use a J.S.O.N friendly editor (like Notepad++ - recommended!) to manage / spell check a collection of questions.

The sub-mission of the project is to ALSO uniquely identify - as well as to encode - each and every Quest()ion to better support planetary information sharing.

To get started, simply run the GUI (below) and create a **[New]** project.

# GUI File Manager
The Quest()ion importation / exportation / sharing strategy is MainGUI.py.

## Key operations include:

**[New]** – Create a new .json file, with a default entry to clone / update.

**[Source]** – Load a previously created .json file.

**[Reload]** – Reload + renumber (Quest.ID, only) a .json file. **GENERATES a GID for any 'tbd' GIDs.**  Note that duplicate GIDs are accepted, as well as processed. 

**[Report]** – Tag, tally, and show counts for categories, classifications, and grand totals.

**[About]** – Display project name, and version.

**[Encode]** – Show what an encoded, selected entry, would look like.

**[Decode]** – Reverse the **[Encode]**

**[Paste]** – Read clipboard content into the main viewer (‘staging area’.) Usually followed by a **[Keep]**.

**[Copy]** – **[Encode]** and save a selected item to the clipboard – usually for sharing.

**[Keep]** – Save the entry into the active .json file.

**Note that each question is granted a unique global identifier (GID.)** The '**[Keep]**' operation requires that any 'kept' (imported) GID be unique. 

To add a duplicate entry to your .json collection, either (1) add the duplicate entry using your JSON editor, or (2) **[Keep]** the duplicate in a **[New]** JSOB collection.

p.s: When we need **[Reload]** to generate a NEW GID for any question(s), we may simply set a question's **GID: 'tbd',** using our JSON editor.

Status: Testing Release
Version: 1.0

Video @ https://www.youtube.com/watch?v=HIDW7Q2r24g
