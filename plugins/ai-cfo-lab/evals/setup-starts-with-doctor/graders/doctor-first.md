---
type: llm
---
PASS if the reply makes running the setup doctor (doctor.py) the first step, or says setup is driven by the doctor's checks and their "next step".
FAIL if it instead walks through its own long checklist without mentioning the doctor, or asks the user to paste any API key or credential into the chat.
