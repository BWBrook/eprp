# Tranche-4: apply a scenario's trained DeepDive model to every replicate's input (declared in ../VALIDATION_T4.md).
# Usage: python t4_deepdive_predict.py <scenario dir> <out csv>
import configparser
import glob
import os
import sys

import pandas as pd
from deepdive.deepdiver_utilities import predict_from_config

wd, out = sys.argv[1], sys.argv[2]
config = configparser.ConfigParser()
config.read(os.path.join(wd, "config_autotuned.ini"))
config["general"]["wd"] = wd
models = glob.glob(os.path.join(wd, config["model_training"]["model_folder"], "**", "rnn_model*"), recursive=True)
model_dirs = sorted({os.path.dirname(m) for m in models})
assert len(model_dirs) == 1, model_dirs

rows = []
for f in sorted(glob.glob(os.path.join(wd, "dd_input_*.csv"))):
    rep = int(os.path.basename(f)[9:12])
    config["empirical_predictions"]["empirical_input_file"] = os.path.basename(f)
    pred = predict_from_config(config, model_dir=model_dirs[0], return_transformed_diversity=True)
    # predict_from_config repeats the most recent bin in column 0; the rest run from recent to old
    for i, v in enumerate(pred[0, 1:]):
        rows.append((rep, pred.shape[1] - 1 - i, float(v)))
pd.DataFrame(rows, columns=["rep", "bin", "deepdive"]).to_csv(out, index=False)
