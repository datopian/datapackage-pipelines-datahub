# DataHub Extensions for datapackage-pipelines

## Install

```
# clone the repo and install it wit pip

git clone https://github.com/datahq/datapackage-pipelines-datahub.git
pip install -e .
```

## Usage

You can use datapackage-pipelines-datahub as a plugin for (dpp)[https://github.com/frictionlessdata/datapackage-pipelines#datapackage-pipelines]. In pipeline-spec.yaml it will look like this

```yaml
  ...
  - run: datahub.dump.to_datahub
```
