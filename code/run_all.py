"""Run the complete final-table-to-figure workflow."""
import argparse,subprocess,sys
from pathlib import Path
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--figures-only",action="store_true")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    code=Path(__file__).resolve().parent
    stages=["05_plot_figures.py"] if args.figures_only else ["01_prepare_analysis.py","02_descriptive.py","03_role_models.py","04_scene_element_models.py","05_plot_figures.py"]
    for stage in stages:
        command=[sys.executable,str(code/stage)]
        if stage=="05_plot_figures.py" and args.output:command+=["--output",str(args.output)]
        subprocess.run(command,cwd=code.parent,check=True)
if __name__=="__main__":main()
