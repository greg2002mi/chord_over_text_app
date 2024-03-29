# ChordPro converter to html

Main function is to read chordpro format text, process chords to desired key and convert to html format.

Small code to convert chordpro format file to html:

Example:
 -- ChordPro format:
[C/Bsus4]What a beautiful day [D]it is 

 -- to:
 
<div class="row g-1">    

	<div class="col-auto">
		<div class="chord_segment">
			<span class="ChordContainer">
				<span class="Chord">C/B<sub>sus4</sub></span>
			</span>
		</div>
		<div class="lyric">What a beautiful day </div>
	</div>

	<div class="col-auto">
		<div class="chord_segment">
			<span class="ChordContainer">
				<span class="Chord">D</span>
			</span>
		</div>
		<div class="lyric">it is</div>
	</div>

</div> <!-- closing row -->

# How to use

Code written in Python and originally developed for Django API, can be used in Flask API or any python based framework.

required:
	Bootstrap
	
Function's name: Chordpro_html(chordpro_text, condition, key, transpose). 
1. chordpro_text - string of chordpro text with chords encased in square brackets
2. condition - boolean, whether to show chords if True, and show only text if False.
3. key - integer, original key of a song, from which to transpose a chord. ( 1: 'C', 2: 'C#', 3: 'D', 4: 'D#', 5: 'E', 6: 'F', 7: 'F#', 8: 'G', 9: 'G#', 10: 'A', 11: 'A#', 12: 'B')
4. transpose - integer, each number is semitone. can be positive or negative.

# Remarks

This code has been written in a rush, thus there might be better solutions, please feel free to contact me if you would like to contribute to this project.
