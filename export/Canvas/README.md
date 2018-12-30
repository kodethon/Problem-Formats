## Get list of Canvas IDs and emails

### Step 1.

Download the Kodethon grades CSV.

### Step 2.

Click the **Grades** section in your Canvas course

### Step 3.

Export a grades CSV file.

### Step 4.

Right-click and click **Inspect** to access the developer's console. Copy the contents of getCanvasEmails.js into the developer's console.

### Step 5.

```
getIdToEmails()
copy(IdToEmails)
```

### Step 6.

Create **id-to-emails.txt** and paste the data obtained from the previous step into the file.

### Step 7.

Pass three paths to the to-canvas.py script.

```
python to-canvas.py KODETHON_GRADES_CSV id-to-emails.txt CANVAS_GRADES_CSV
```
