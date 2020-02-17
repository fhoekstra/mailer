from pathlib import Path

def rename01pdf(in_dir=(Path(__file__).resolve().parent / 'Assessment 2 - 2020')):
    """Renames 1.pdf, 2.pdf etc to 01.pdf, 02.pdf in directory in_dir"""
    in_dir = Path(in_dir)
    print(in_dir)
    for pdf in sorted(in_dir.glob('[0-9].pdf')):
        print(f'renaming {pdf.name}')
        pdf.rename(in_dir / ('0'+pdf.name))

def indexchoice(lst):
    print("Index , element:")
    for idx, el in enumerate(lst):
        print(f'{idx}   ,   {el}')
    return int(input('Which index do you want to select?  '))