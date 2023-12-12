import os
import numpy as np
import copy
import random

aa_mapping = {
    "A": "Ala",
    "R": "Arg",
    "N": "Asn",
    "D": "Asp",
    "C": "Cys",
    "Q": "Gln",
    "E": "Glu",
    "G": "Gly",
    "H": "His",
    "I": "Ile",
    "L": "Leu",
    "K": "Lys",
    "M": "Met",
    "F": "Phe",
    "P": "Pro",
    "S": "Ser",
    "T": "Thr",
    "W": "Trp",
    "Y": "Tyr",
    "V": "Val"
}

# inverted amino acidf mapping
inverted_aa_mapping = {v: k for k, v in aa_mapping.items()}

#############################################################################
# functions:
#############################################################################
def get_protein(input_filename, position):
    # Skip the header rows when reading the protein file:
    skiprows = 2
    block = []
    
    with open(input_filename, "r") as file:
        lines = file.readlines()
        lines = lines[skiprows:]

        # Parse each line and extract coordinates
        for line in lines:
            line_xyz = line.strip().split("\t")
            line_xyz[1] = float(line_xyz[1])
            line_xyz[2] = float(line_xyz[2])
            line_xyz[3] = float(line_xyz[3])
            block.append(line_xyz)

    # Make a deep copy of the protein coordinates:
    protein = copy.deepcopy(block)

    # Get the coordinates of the specified bead for repositioning:
    terminal = copy.deepcopy(protein[position])
            
    # Reposition all beads relative to the specified bead:
    for element in protein:
        element[1] = round(element[1] - terminal[1], 4)
        element[2] = round(element[2] - terminal[2], 4)
        element[3] = round(element[3] - terminal[3], 4)

    # Return the repositioned protein coordinates:
    return protein


def get_blocks_polymer(input_filename):
    blocks = []
    current_block = []
    
    with open(input_filename, 'r') as file:
    
        # remove empty lines:
        lines = []
       
        for line in file:
            line_value = line.strip()
            
            if line_value:
                lines.append(line)

            else:
                continue

        # save blocks:
        for line in lines:
        
            line_value = line.strip().split()[0]
                        
            if line_value != 'C' and not current_block:
                current_block = []

            elif line_value != 'C' and current_block:
                blocks.append(current_block)                   
                current_block = []
                                            
            else:
                line_xyz = line.strip().split()
                line_xyz[1] = float(line_xyz[1])
                line_xyz[2] = float(line_xyz[2])
                line_xyz[3] = float(line_xyz[3]) 
                current_block.append(line_xyz)
        
        # save last block:
        if current_block:
            blocks.append(current_block)
    
        return blocks



def get_blocks_protein(input_filename, comment):

    blocks = []
    
    current_block = []
    
    with open(input_filename, 'r') as file:
    
        # remove lines with single values (rare numbers):
        lines = []
        
        for line in file:
            value_to_test = line.split()[0][0]
            
            try:
                int(value_to_test)

            except ValueError:
                lines.append(line)

        # save blocks:
        for line in lines:
                                
            if comment in line and not current_block:
                current_block = []

            elif comment in line and current_block:
                blocks.append(current_block)                   
                current_block = []
                                            
            else:
                line_xyz = line.strip().split()
                line_xyz[1] = float(line_xyz[1])
                line_xyz[2] = float(line_xyz[2])
                line_xyz[3] = float(line_xyz[3]) 
                current_block.append(line_xyz)
        
        # save last block:
        if current_block:
            blocks.append(current_block)
                
        return blocks  



def a_to_nm(block):

    for element in block:
        element[1] = round(element[1]/10,4)
        element[2] = round(element[2]/10,4)
        element[3] = round(element[3]/10,4)

    return block



def get_polymers(sequence):

    # add one aditional bead because we delete one at the end of the function:
    chain_length = len(sequence) + 1

    # create the chain:
    os.system('cd random/ && bash compi.sh')
    os.system('cd random/ && echo {} | ./polymer.x'.format(chain_length))

    # get polimers:
    polymers = get_blocks_polymer('random/polymer.xyz')

    # delete the firs's bead:
    for polymer in polymers:
        a_to_nm(polymer)
        polymer.pop(0)

    return polymers



def get_filtered_polymers(protein, polymers, cutoff_distance):
    '''
    The polymer it is just attached on the protein
    '''
    #dxyz_connection = 0.4    
    filtered_polymers = []
    
    for polymer in polymers:
       
        # Calculate the distance between each coordinate of the polymer and those of the protein:
        dxyz_list = []
        
        # loop for protein:
        for coord_protein in range(len(protein)):
            
            # coordenate for aminoacid in protein:
            coord1 = np.array(protein[coord_protein][1:]) 
            
            # loop for polymer:
            for coord_polymer in range(len(polymer)):
                
                # coordenate for bead in polymer:
                coord2 = np.array(polymer[coord_polymer][1:])
                
                # calculate distance:
                dxyz = np.linalg.norm(coord1 - coord2)
                
                # append distance:
                dxyz_list.append(dxyz)
        
        # skip structures with overlaping:
        if any(element < cutoff_distance for element in dxyz_list): 
            pass
            
        else:
            filtered_polymers.append(polymer)
         
    return filtered_polymers



def add_sequence(molecule, sequence, start_sequence, end_sequence):

    # Add a peptide sequence:
    for i in range(start_sequence, end_sequence):
        index = i - start_sequence
        molecule[i][0] = aa_mapping[sequence[index]]

    return molecule



def add_terminals(molecule):

    # Add N-terminal to the first's bead:
    molecule[0][0] = inverted_aa_mapping[molecule[0][0]] + '_Nt'

    # Add C-terminal to the last's bead:
    molecule[-1][0] = inverted_aa_mapping[molecule[-1][0]] + '_Ct'

    return molecule



def get_merge_all(protein, filtered_polymers, terminal_position, sequence):

    if terminal_position == 'Nter':
    
        #count_confs = 0
        
        molecule_list = []     
        
        for polymer in filtered_polymers:
        
            # reverse the polymer sequence:
            polymer = copy.deepcopy(polymer)    # deep copy
            polymer = polymer[::-1]             # reverse the sequence (only in Nter)

            # Add polymer to protein (.xyz):
            polymer_protein = copy.deepcopy(polymer) + copy.deepcopy(protein)
                        
            # Add peptide sequence to the .xyz file:
            polymer_protein = copy.deepcopy(polymer_protein)  # deep copy
            sequence_to_insert = sequence[::-1]                 # reverse the sequence (only in Nter)
            start_sequence = 0
            end_sequence = len(sequence_to_insert)
            polymer_protein = add_sequence(polymer_protein, sequence_to_insert, start_sequence, end_sequence)
                  
            # Add terminal aminoacids:
            polymer_protein = copy.deepcopy(polymer_protein)
            polymer_protein = add_terminals(polymer_protein)

            # Append protein_polymer:
            #count_confs += 1
            molecule_list.append(polymer_protein)
                            
    elif terminal_position == 'Cter':
    
        #count_confs = 0
        
        molecule_list = []
        
        for polymer in filtered_polymers:
        
            # Add protein to polymer:
            protein_polymer = copy.deepcopy(protein) + copy.deepcopy(polymer)
                
            # Add peptide sequence:
            protein_polymer = copy.deepcopy(protein_polymer)
            sequence_to_insert = sequence
            start_sequence = len(protein)
            end_sequence = len(protein) + len(sequence_to_insert)
            protein_polymer = add_sequence(protein_polymer, sequence_to_insert, start_sequence, end_sequence)

            # Add terminal aminoacids:
            protein_polymer = copy.deepcopy(protein_polymer)
            protein_polymer = add_terminals(protein_polymer)

            # Append protein_polymer:
            #count_confs += 1
            molecule_list.append(protein_polymer)
                                             
    else:
        print('It must be provided an option to include a peptide')

    return molecule_list



def get_merge_random(protein_merge_all, nconf):

    # Set a seed for the random number generator:
    seed_value = 0
    random.seed(seed_value)
    protein_merge_random = random.sample(protein_merge_all, nconf)
    #print(nconf)
    #exit()
         
    return protein_merge_random
       
       
         
def save_results(terminal_position, molecules, output_filename, bridge, peptide, nconf):

    # Name of the output file:
    if peptide is not None and bridge is not None:
        output_filename_xyz = f'{output_filename}_{terminal_position}_bridge-{bridge}_peptide-{peptide}_conf-{nconf}.xyz'
        output_filename_seq = f'{output_filename}_{terminal_position}_bridge-{bridge}_peptide-{peptide}_conf-{nconf}.seq'
        
    # Name of the output file:    
    elif peptide is not None and bridge is None:
        output_filename_xyz = f'{output_filename}_{terminal_position}_peptide-{peptide}_conf-{nconf}.xyz'
        output_filename_seq = f'{output_filename}_{terminal_position}_peptide-{peptide}_conf-{nconf}.seq'
        
    # Name of the output file:              
    elif bridge is not None and peptide is None:
        output_filename_xyz = f'{output_filename}_{terminal_position}_bridge-{bridge}_conf-{nconf}.xyz'
        output_filename_seq = f'{output_filename}_{terminal_position}_bridge-{bridge}_conf-{nconf}.seq'
                
    else:
        print('An option it must be provided')

    # Save file:
    with open(output_filename_xyz, 'w') as file:

        # Get amount of beads:
        n_beads = int(len(molecules[0]))

        # Write coordinates:
        for molecule in molecules:
        
            file.write(str(n_beads) + '\n')
            file.write('This is a comment \n')
            
            for line in molecule:
            
                # Write header:
                element = '\t'.join(map(str, line))
                file.write(element + '\n')                  

    with open(output_filename_seq, 'w') as file:

        # Write header:
        file.write('This is a comment \n')

        # Write index and aminoacid name:
        index = 0
        
        for element in molecule:
        
            amino_acid = element[0]    # aminoacid name
            index += 1                 # index numeration
            file.write(str(index) + '\t' + str(amino_acid) + '\n')




def get_block2xyz(blocks, output_filename):
    with open(output_filename, 'w') as file:
        for block in blocks:
            nseg = len(block)
            file.write(f'{nseg}\n')
            file.write('This is a comment\n')
            #file.write('\n')
            for line in block:
                file.write(f'{line[0]}\t{line[1]}\t{line[2]}\t{line[3]}\n')

    
    
###########################################################################
# function definitions:
def splitxyz(input_filename, comment, output_basename):
    '''
    Split a rotations.xyz file, file that contains multiple xyz files.

    Parameters:
    - filename (str): The name of the file to split (e.g. rotations.xyz).
    - comment (str): comment of the second line of the file.
    Returns:
    frame_*.xyz file
    '''
    
    blocks = []
    current_block = []
    
    with open(input_filename, 'r') as file:
    
        # skip rows with rare numbers:
        lines = []
        for line in file:
            pattern1_to_test = len(line.split())
            if pattern1_to_test == 1:
                nseg = line.split()[0]
                continue
            else:
                lines.append(line)
        
        #print(lines)
        #exit()
        # save blocks of data by spacing:
        for line in lines:

            # pattern to test:
            pattern2_to_test = line.strip()

            # if pattern is found and currect block is empty:
            if pattern2_to_test == comment and not current_block:
                current_block = []

            # if pattern is found and currect block is not empty:                
            elif pattern2_to_test == comment and current_block:        
                blocks.append(current_block)                   
                current_block = []
                
            else:
                line_read = line.strip().split()
                line_read_new = [line_read[0], line_read[1], line_read[2], line_read[3]]
                current_block.append(line_read_new)

        # save last block:
        if current_block:
            blocks.append(current_block)
    #print(blocks[0])
    # save file:
    count = 0
    for block in blocks:
        output = f'{output_basename}-{count:02d}.xyz' 
        with open(output, 'w') as file:
            file.write(f'{nseg}\n')
            file.write(f'{comment}\n')
            for line in block:
                file.write(f'{line[0]}   {line[1]}   {line[2]}   {line[3]}\n')
        count += 1
    
    
def get_thetas(input_filename, comment, n1, n2):
    blocks = get_blocks_protein(input_filename, comment)
    nblocks = len(blocks)
    thetas = []
    for block in blocks:
        # : component on x, y, and z:
        delx = block[n2][1] - block[n1][1]
        dely = block[n2][2] - block[n1][2]
        delz = block[n2][3] - block[n1][3]

        # get distance:
        delr = np.sqrt(delx**2 + dely**2 + delz**2)
    
        # get theta angle:
        theta = np.arccos(delz/delr)
                
        # append:
        thetas.append(theta)
                
    return nblocks, thetas 



def get_costhetas(input_filename, comment, n1, n2):
    
    blocks = get_blocks_protein(input_filename, comment)
    
    nblocks = len(blocks)
    
    costhetas = []
    
    for block in blocks:
    
        # : component on x, y, and z:
        delx = block[n2][1] - block[n1][1]
        dely = block[n2][2] - block[n1][2]
        delz = block[n2][3] - block[n1][3]

        # get distance:
        delr = np.sqrt(delx**2 + dely**2 + delz**2)
    
        # get costheta:
        #costheta = delz / delr
        costheta = np.float64(delz) / np.float64(delr)
                    
        # append:
        costhetas.append(costheta)
                
    return nblocks, costhetas 



def get_phis(input_filename, comment, n1, n2):
    blocks = get_blocks_protein(input_filename, comment)
    nblocks = len(blocks)
    phis = []
    for block in blocks:
        # : component on x, y, and z:
        delx = block[n2][1] - block[n1][1]
        dely = block[n2][2] - block[n1][2]
        delz = block[n2][3] - block[n1][3]

        # get distance:
        delr = np.sqrt(delx**2 + dely**2 + delz**2)
    
        # get phi angle:
        phi = np.arctan2(dely, delx)
                
        # append:
        phis.append(phi)
                
    return nblocks, phis 



def calculate_distances_polymer(input_filename, n1, n2):
    blocks = get_blocks_polymer(input_filename)
    distances = []
    nblocks = len(blocks)

    for block in blocks:
        position1 = block[n1][1:]
        position2 = block[n2][1:]
        distance = ((position2[0] - position1[0])**2 + (position2[1] - position1[1])**2 + (position2[2] - position1[2])**2)**0.5
        distances.append(distance)

    return nblocks, distances



def calculate_distances_protein(input_filename, comment, n1, n2):
    blocks = get_blocks_protein(input_filename, comment)
    distances = []
    nblocks = len(blocks)

    for block in blocks:
        position1 = block[n1][1:]
        position2 = block[n2][1:]
        distance = ((position2[0] - position1[0])**2 + (position2[1] - position1[1])**2 + (position2[2] - position1[2])**2)**0.5
        distances.append(distance)

    return nblocks, distances
    
    
    
    
    



