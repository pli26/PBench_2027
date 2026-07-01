# inputs=("Agg_NumAgg" "Agg_HavingSel" "Agg_GroupSize" "Agg_MultiLevel" "Join_JoinCard" "Join_JoinSel" "Join_NumJoin" "TopK" "DataFilter" "QueryProv" "SizeProvRes_FixProv")
# inputs=("FPAgg" "FPSAgg" "VPGN" "VPGS" "VPJC" "VPJJ" "VPJJJ" "VPJS")

# inputs=("FPAgg" "FPSAgg" "QAggNum" "QMLAgg" "QTopK" "VPGN" "VPGS" "VPJC" "VPJJ" "VPJJJ" "VPJS")
inputs=("FPAgg" "FPDist" "FPSAgg" "FPSDist" "QAggNum" "QMLAgg" "QTopK" "VPGN" "VPGS" "VPJC" "VPJJ" "VPJJJ" "VPJS")
currpath=$(pwd)
for v in "${inputs[@]}"; do
  cd "${currpath}/${v}"
  python genQ.py
done
