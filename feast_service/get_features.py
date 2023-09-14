import os
from datetime import datetime
import pandas
from feast import FeatureStore

store = FeatureStore(
    fs_yaml_file=os.path.join(os.path.dirname(__file__), "feature_store", "feature_store.yaml")
)

feature_list=[
    "whcaent_ent:title",
    "whcaent_ent:firstname",
    "whcaent_ent:surname",
    "whcaent_ent:date_of_birth",
    "whcaent_ent:sys_eff_to",
]

historical_features = store.get_historical_features(
    entity_df=pandas.DataFrame.from_dict(
      {
        "entity_no": [1, 2, 999998, 999999],
        "sys_eff_from": datetime(2000, 1, 1, 12, 0)
      }
    ),
    features=feature_list,
).to_df()
print(f"historical_features:\n{historical_features}")

online_features = store.get_online_features(
    entity_rows=[
        {"entity_no": entno}
        for entno in [
            1,
            2,
            999998,
            999999,
        ]
    ],
    features=feature_list,
).to_df()
print(f"\nonline_features:\n{online_features}")
