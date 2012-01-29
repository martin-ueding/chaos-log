# chaos log

Script to parse snapshots of `top` and `sensors` from a server.

## directory structure

It expects the data dirs to have a structure like this: (using RegEx syntax)

	YYYY-MM-DD
		HH.*
			mm-processes.log
			mm-sensors.log

`YYYY` means the four digit year, `MM` the two digit month, `DD` the two digit day. `HH` is 24 hours, `mm` two digit minutes.
