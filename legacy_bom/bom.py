import os
import shutil
import subprocess
from glob import glob

def run_command(command):
    """Run a shell command and print the output."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

def main():
    # Remove the 'bom' directory if it exists
    if os.path.exists('bom'):
        shutil.rmtree('bom')
    
    # Create the 'bom' directory
    os.mkdir('bom')

    # Find all .kicad_sch files
    kicad_sch_files = glob('*.kicad_sch')
    
    # Export the BOM for each .kicad_sch file
    for kicad_sch_file in kicad_sch_files:
        xml_file = os.path.join('bom', os.path.basename(kicad_sch_file).replace('.kicad_sch', '.xml'))
        run_command(f'kicad-cli sch export python-bom -o {xml_file} {kicad_sch_file}')
    
    # Run the BOM generator on each exported XML file
    xml_files = glob('bom/*.xml')
    for xml_file in xml_files:
        csv_file = os.path.join('bom', os.path.basename(xml_file).replace('.xml', '.csv'))
        run_command(f'python3 bom_generator.py {xml_file} {csv_file}')

if __name__ == "__main__":
    main()