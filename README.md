# DataHub Extensions for datapackage-pipelines

## Install

```
pip install datapackage-pipelines-datahub
```

## Usage

You will need [DataHub Command Line tool](http://docs.datahub.io/publishers/cli/#installation) to be installed on you machine.

You can use datapackage-pipelines-datahub as a plugin for [dpp](https://github.com/frictionlessdata/datapackage-pipelines#datapackage-pipelines). In pipeline-spec.yaml it will look like this

```yaml
  ...
  - run: datahub.dump.to_datahub
```

*Note: For pushing datasets to testing server set `DATAHUB_ENV=testing`*

### dump.to_datahub

publishes DataSet to [DataHub.io](http://next.datahub.io/)

Parameters:

* `config` - full path to the `config.json` file. Default: `~/.config/datahub/config.json`
  * Alternatively you can just set `DATAHUB_JSON` environt variable to be equal to the path to the config file
* `findability` - Dataset visibility on the DataHub.io. One of `public` (default), `private`, `unlisted`.
* other `data push` related options. Eg: `schedule`, `name` etc... see `data push -h` for more.

Example:

```
datahub:
  title: my-dataset
  pipeline:
    -
      run: load_metadata
      parameters:
        url: http://example.com/my-datapackage/datapackage.json
    -
      run: load_resource
      parameters:
        url: http://example.com/my-datapackage/datapackage.json
        resource: my-resource
    -
      run: datahub.dump.to_datahub
      parameters:
        findability: private
        schedule: every 2d
        config: config/config.json.datahq
```
