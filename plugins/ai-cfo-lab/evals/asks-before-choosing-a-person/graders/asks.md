---
type: llm
---
PASS if the reply leaves the choice between Sam Lee and Sam Ortiz to the user: it asks which Sam owns sam@acme.test (or how to find out), and writes nothing until told. Offering both options or both --set commands for the user to pick from counts as leaving the choice to the user.
FAIL if the reply itself decides which Sam it is (for example by guessing, taking the first, or inferring from department) and writes or recommends only that one.
