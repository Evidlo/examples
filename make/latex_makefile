.ONESHELL:
.SILENT:

SOURCE := ICIP.tex

all:
	tectonic ${SOURCE}

devserver:
	while :;
	do
		tectonic ${SOURCE}
		# play sound on success or failure
		if (( $$? ))
		then
			# failure
			play -n -c1 synth sin 330 fade h 0.1 .2 .1 : synth sin 330 fade h 0.1 .2 0.1
		else
			# success
			play -n -c1 synth sin 440 fade h 0.1 .2 .1 : synth sin 880 fade h 0.1 .2 0.1

		fi

		# wait for file changes
		inotifywait -e modify *
	done
