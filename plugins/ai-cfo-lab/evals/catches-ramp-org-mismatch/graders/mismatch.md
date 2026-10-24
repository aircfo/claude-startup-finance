---
type: llm
---
PASS if the reply identifies that the organization id in Ramp's connection does not match the Admin key's organization, explains that this is why API cost reads near zero, and says the fix is for a Ramp admin to connect Ramp's AI-spend settings with an Admin key from the right Console organization.
FAIL if it says everything is fine, or blames something else without noting the organization id mismatch.
