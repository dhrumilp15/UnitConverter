# UnitConverter

Thanks for taking a look at my Unit Converter for CCExtractor!

You can use it in three ways:

- User Prompt: Just call the `main()` method of `UnitConverter` with no method parameters

- From Method Call: Call the `main()` method of `UnitConverter` like so:  `main([number of source units], [source unit], [target unit])`

- From command-line: Include the parameters when using `unitConverter.py` like so: `python unitconverter.py 1 m cm`

## Supports:

If the conversion table includes the required conversions, this unit converter can handle:

- [x] Basic Conversions (Ex: m (meters) -> mm (millimeters))
- [x] Complex Conversions (Ex: m/s (meters per second) -> in/hr (inches per hour))
- [x] Combined Complex Conversions (Ex: W(watts) -> kJ/hr (kiloJoules per hour))

## Testing:

This was the first time I wrote tests for python!

My tests are all in the tests/ folder. I tried to make comprehensive tests but I'd really appreciate it if you could leave feedback on how to make better tests!

I'm using pytest as my test runner, so run `python -m pytest` to run the tests in the tests/ folder!