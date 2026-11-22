# scripts/run_all.sh

Save as `scripts/run_all.sh`

````bash
#!/bin/bash
# Example rotation: each tiny model sits one paper per subject, and every model sits the fusion paper.
# Edit the model names, paper files and notes folders, then run from the folder holding the papers.
# Papers use the format in reference/mock-papers.md; answers go to answers/.
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
A=LFM2.5-1.2B-Instruct-GGUF; B=Llama-3.2-1B-Instruct-GGUF-Q4_K_M; C=Qwen3-0.6B-GGUF
N1=../Course1_Notes; N2=../Course2_Notes          # notes folders
mkdir -p answers
run(){ python "$SKILL/scripts/rag_exam.py" "$1" "$2.md" "$3" "answers/$2__$1.md" >> run.log 2>&1; echo "$2 $1 finished" >> run.log; }
run $A C1_A "$N1"; run $A C2_B "$N2"; run $A FUSION "$N1,$N2"
run $B C1_B "$N1"; run $B C2_A "$N2"; run $B FUSION "$N1,$N2"
run $C C1_C "$N1"; run $C C2_C "$N2"; run $C FUSION "$N1,$N2"
echo ALL DONE >> run.log
````
