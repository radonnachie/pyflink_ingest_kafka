from feast import (
    Entity,
    FeatureView,
    Field,
    FileSource,
    PushSource,
)
from feast.types import String, UnixTimestamp
from feast.data_format import ParquetFormat

import os
from datetime import timedelta

file_dir = os.path.dirname(__file__)

# You can think of an entity as a primary key used to fetch features.
whcaent_ent = Entity(name="whcaent", join_keys=["entity_no"])

# Define a pushed FeatureView
whcaent_ent_fv = FeatureView(
    name="whcaent_ent",
    entities=[whcaent_ent],
    schema=[
        Field(name="title", dtype=String),
        Field(name="firstname", dtype=String),
        Field(name="surname", dtype=String),
        Field(name="date_of_birth", dtype=UnixTimestamp),
        Field(name="sys_eff_to", dtype=UnixTimestamp),
    ],
    online=True,
    ttl=timedelta(days=1),
    source=PushSource(
        name="whcaent_ent_push_source",
        batch_source=FileSource(
            file_format=ParquetFormat(),
            path=os.path.join(file_dir, "entities.parquet"),
            timestamp_field="sys_eff_from",
        ),
    ),
)
