DIR="$( dirname -- "${BASH_SOURCE[0]}"; )";   # Get the directory name
DIR="$( realpath -e -- "$DIR"; )";    # Resolve its full path if need be

dvc stage add -n combine_data \
  -d $DIR/combine_pipeline.py -d $DIR/../../data/original/ \
  -o $DIR/../../data/processed/combined_asag2024.pq \
  python $DIR/combine_pipeline.py
