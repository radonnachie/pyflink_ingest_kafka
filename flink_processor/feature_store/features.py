from feast import (
    Entity,
    FeatureView,
    Field,
    FileSource,
    PushSource,
)
from feast.types import String, UnixTimestamp
from feast.data_format import ParquetFormat

# Define an entity for the vitality policy. You can think of an entity as a primary key used to
# fetch features.

whcaent_ent = Entity(name="whcaent", join_keys=["entity_no"])

# Define a push simulacra
whcaent_ent = FeatureView(
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
    source=PushSource(
        name="whcaent_ent_push_source",
        batch_source=FileSource(
            file_format=ParquetFormat(),
            path="entities.parquet",
            timestamp_field="sys_eff_from",
        ),
    ),
)