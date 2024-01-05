import re
   
    # &nbsp;

# end model   
 
# 		<div class="row g-1">    

# 			<div class="col-auto"> <!-- chord text segment-->
# 				<div class="chord_segment">
# 					<span class="ChordContainer">
# 						<span class="Chord">C</span>
# 					</span>
# 				</div> <!-- closing chord segment-->
# 				<div class="lyric">What a beautiful day </div>
# 			</div> <!-- closing chord text segment-->

# 			<div class="col-auto"> <!-- next chord text segment-->
# 				<div class="chord_segment">
# 					<span class="ChordContainer">
# 						<span class="Chord">D</span>
# 					</span>
# 				</div> <!-- closing chord segment-->
# 				<div class="lyric"> it is</div>
# 			</div> <!-- closing next chord text segment-->

# 		</div> <!-- closing row -->    


def n_occurrence(match, n):
    global count
    count += 1
    if count == n:
        return '</div><div class="col-6">'
    else:
        return match.group(0)

def Html_columns(html, n):
    count = 0
    modified_html = re.sub(r'<div class="col-6">', lambda match: n_occurrence(match, n), html, count=n)

    final_html = '<div class="row"><div class="col-6">{}</div></div>'.format(modified_html)
    return final_html

    # this function transposes chords to any desired key
    # thischord - is current chord in a form of note letters, considers bimol or sharp too.
    # ori_key - is ankor key from which to transpose
    # transpose - an integer for how much to transpose. step is semitone
def Transpose(thischord, condition, ori_key, transpose):
    
    if ori_key == transpose or transpose == 0:
        match = re.match(r"([A-G])([a-z#]*\d*)", thischord)
        if match:
            root_note = match.group(1)
            chord_type = match.group(2) if len(match.groups()) > 1 else ""
        else:
            return thischord

        # checks if second part has # or b. and if so moves # or b to root_note
        if re.search(r"[#b]", chord_type):
            filtered_string = ''.join(char for char in chord_type if char not in ('#', 'b'))
            remaining_root = ''.join(char for char in chord_type if char in ('#', 'b'))
            root_note = root_note.strip() + remaining_root.strip()
            chord_type = filtered_string
    
        # encase sharp and bimol in sup tags
        if '#' in root_note:
            root_note = f"{root_note[:-1]}<sup>{root_note[-1]}</sup>"
        elif 'b' in root_note:
            root_note = f"{root_note[:-1]}<sup>{root_note[-1]}</sup>"
        
        # encase remaining of chord in sub tags
        if chord_type:
            chord_type = f"<sub>{chord_type}</sub>"
        else:
            chord_type = ""
    
        thischord = root_note + chord_type    
    
        return thischord
    elif thischord is None:
        return "Error"
    else:
        chord_map = {
            1: 'C',
            2: 'C#',
            3: 'D',
            4: 'D#',
            5: 'E',
            6: 'F',
            7: 'F#',
            8: 'G',
            9: 'G#',
            10: 'A',
            11: 'A#',
            12: 'B'
            }
        chord_index = {
            'C': 1,
            'B#': 1,
            'C#': 2,
            'Db': 2,
            'D': 3,
            'D#': 4,
            'Eb': 4,
            'E': 5,
            'E#': 6,
            'Fb': 5,
            'F': 6,
            'F#': 7,
            'Gb': 7,
            'G': 8,
            'G#': 9,
            'Ab': 9,
            'A': 10,
            'A#': 11,
            'Bb': 11,
            'B': 12,
            'Cb': 12
            }

        transposed_chord = ""
        # change int to how much the note should be changed
        f = int(ori_key) - int(transpose)
        
        # Bm#4 splits into B and m#4
        match = re.match(r"([A-G])([a-z#]*\d*)", thischord)
        if match:
            root_note = match.group(1)
            chord_type = match.group(2) if len(match.groups()) > 1 else ""
        else:
            return thischord

        # checks if second part has # or b. and if so moves # or b to root_note
        if re.search(r"[#b]", chord_type):
            filtered_string = ''.join(char for char in chord_type if char not in ('#', 'b'))
            remaining_root = ''.join(char for char in chord_type if char in ('#', 'b'))
            root_note = root_note.strip() + remaining_root.strip()
            chord_type = filtered_string
        int_note = chord_index.get(root_note)

        if int_note is None:
            int_note = 1
            transposed_chord = "(Err: index)"
        # transposes any chord to desired based on difference between original and transposed key
        a = int_note - f
        # if a = 0 then its 12
        if a <= 0:
            a = a + 12
        elif a > 12:
            a = a - 12
        else:
            transposed_chord = "(Err: a is None or Zero)"

        t_l = chord_map.get(a)
        #merge changed letter of a chord into full chord

        # encase sharp and bimol in sup tags
        if '#' in t_l:
            t_l = f"{t_l[:-1]}<sup>{t_l[-1]}</sup>"
        elif 'b' in t_l:
            t_l = f"{t_l[:-1]}<sup>{t_l[-1]}</sup>"
        
        # encase remaining of chord in sub tags
        if chord_type:
            chord_type = f"<sub>{chord_type}</sub>"
        else:
            chord_type = ""

        transposed_chord = t_l + chord_type

        return transposed_chord 
  
def Process_chord(segment, condition, key, transpose):
    # strips from square brackets
    temp_chord = segment.strip('[]')
    slash = "/"
    # checks for the dual chord with slash
    if re.search(r'/', temp_chord):
        splitting = re.findall(r"[^/]+", temp_chord)
        if splitting is not None:
            first_chord = splitting[0]
            first = Transpose(first_chord, condition, key, transpose)
            second_chord = splitting[1]
            second = Transpose(second_chord, condition, key, transpose)
            chord = first + slash + second
        else:
            chord = '(Err)'        
    else:
        chord = Transpose(temp_chord, condition, key, transpose)
        
    return chord
    
   
def Chordpro_html(chordpro_text, condition, key, transpose):
    lines = chordpro_text.split('\n')
    html_lines = []
    # condition defines building html with chords or without
    if condition:
        for line in lines:
            # Check if the line contains a chord
            if not line:
                continue
            else:
                if re.search(r'\[[^\]]+\]', line): # yes
                    # Split the line into segments with chords
                    segments = re.split(r'(\[[^\]]+\])', line)
                    html_segments = []
                    # only first in loop must be checked for chord or lyrics                    
                    for index, segment in enumerate(segments):
                        # if line is empty go to next line. 
                        if len(segment) == 0:
                            continue
                        # whether line starts with chord
                        if index == 0:
                            if segment.startswith('['):
                                chord = Process_chord(segment, condition, key, transpose)
                                html_segments.append('<div class="col-auto"><div class="chordpro_segment"><span class="ChordContainer"><span class="Chord">{}&nbsp;</span></span></div>'.format(chord))
                            else:
                                html_segments.append('<div class="col-auto"><div class="chordpro_segment"><span class="ChordContainer"><span class="Chord"></span></span></div>') 
                                if segment.endswith(' '):
                                    html_segments.append('<div class="lyric">{}&nbsp;</div></div>'.format(segment))
                                else:
                                    html_segments.append('<div class="lyric">{}</div></div>'.format(segment))
                            
                        elif index > 0:    
                            # Check if the segment is a chord and is the last in line
                            if re.match(r'\[[^\]]+\]', segment) and index == len(segments) - 1:
                                chord = Process_chord(segment, condition, key, transpose)
                                html_segments.append('<div class="col-auto"><div class="chordpro_segment"><span class="ChordContainer"><span class="Chord">{}&nbsp;</span></span></div><div class="lyric">&nbsp;</div></div>'.format(chord))
                            # Check if the segment is a chord
                            elif re.match(r'\[[^\]]+\]', segment) and index < len(segments) - 1:
                                chord = Process_chord(segment, condition, key, transpose)
                                html_segments.append('<div class="col-auto"><div class="chordpro_segment"><span class="ChordContainer"><span class="Chord">{}&nbsp;</span></span></div>'.format(chord))
                            # eliminate sticking of words     
                            # this logic excludes situations when chord is inside a word
                            else:
                                if segment.endswith(' ') and segment.startswith(' '):
                                    segment = segment[1:-1]
                                    html_segments.append('<div class="lyric">&nbsp;{}&nbsp;</div></div>'.format(segment))
                                elif segment.startswith(' '):
                                    segment = segment[1:]
                                    html_segments.append('<div class="lyric">&nbsp;{}</div></div>'.format(segment))
                                elif segment.endswith(' '):
                                    segment = segment[:-1]
                                    html_segments.append('<div class="lyric">{}&nbsp;</div></div>'.format(segment))
                                else:
                                    html_segments.append('<div class="lyric">{}</div></div>'.format(segment)) #close chord-pre-sergment div

                
                    html_lines.append('<div class="row g-0">{}</div>'.format(''.join(html_segments)))
                
                # searching for chorus verse Bridge and intro. assign section-name class and make it bold.
                # later add logic to add comments using "c:" tag
                # LAST STAGE
                elif re.search(r'\{Chorus\}|\{Verse \d+\}|\{Bridge\}|\{Intro\}|\{Ending\}|\{Retard\}|\{Instrumental\}|\{Pre-Chorus\}|\{end\}', line):
                    section_line = line.replace('{end}', '&nbsp;').replace('{', '').replace('}', '')
                    #section_line = line.strip('{}')
                    html_lines.append('<div class="row g-0"><div class="col-auto"><div class="chordpro_segment"><span class="ChordContainer"><span class="Chord"></span></span></div><div class="lyric_section">{}:</div></div></div>'.format(section_line))
                
                # encase whole line in one div and set a class of a line
                else:
                    html_lines.append('<div class="row g-0"><div class="col-auto"><div class="chordpro_segment"><span class="ChordContainer"><span class="Chord"></span></span></div><div class="lyric">{}</div></div></div>'.format(line))
    # if condition is false then all chords are removed
    else:
        for line in lines:
            line_without_chords = re.sub(r'\[[^\]]+\]', '', line)
            line = line_without_chords.replace('{end}', '&nbsp;').replace('{', '<br>').replace('}', ':').replace('Intro}', '')
            html_lines.append('<div class="row g-0"><div class="lyric">{}</div></div>'.format(''.join(line)))
            
    html_code = ''.join(html_lines)
    return html_code
   