# StepFunction Event Logger Test

This repo serves to demonstrate the raw power of the [StepFunction Event Logger Construct](https://github.com/developmentseed/cdk-seed/tree/seed/stepfunction-event-logger). 

To spin up a stack: 
- `pipenv install --dev`
- `cdk deploy stepfunction-logger-test`

Set `custom_lambda` to `True` in `stack/app.py`, line 11 to see how the stack spins with a "custom" lambda compared to the standard one included in the construct
