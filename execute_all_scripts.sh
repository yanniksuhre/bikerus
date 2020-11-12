#!/bin/sh
#$ -cwd

python python/0_pipeline_data_getting_compressing.py
python python/0.1_pipeline_bike_station_viz.py
python python/1_pipeline_imputing_NAs.py
python python/2_pipeline_preprocessing.py
python python/3_pipeline_train_test_ts.py
python python/4_models.py
python python/5_predict_test_df.py