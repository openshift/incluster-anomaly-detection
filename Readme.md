This codebase contains sample code to detect anomalies. Below are steps you can perform to run it within a cluster.

### 1. Build container image and push to registry

```
docker build -t quay.io/openshiftanalytics/incluster-anomaly:v1 ./ --platform linux/amd64 --no-cache
docker push  quay.io/openshiftanalytics/incluster-anomaly:v1    
```

### 2. Create required service account/role binding/secret etc into openshift cluster and run anomaly detection program in a pod

#### 2.1 Login into openshift cluster
You can get the login command once you login into openshift cluster, click on profile in the top right corner and click on "Copy login command"
```
oc login --token=*** --server=***
```

#### 2.2 Add prerequisite for anomaly-engin
```
oc apply -f openshift/prerequisite.yaml
```

#### 2.3 Change the namespace
```
oc project osa-anomaly-detection
```

#### 2.4 Run code through cronjob
```
# Add cronjob 
oc process -f openshift/cronjob-template.yaml | oc apply -f -
```


#### 2.5 Cronjob will try to find anomalies and if anything come up it will add anomaly data into CRD storage which can be queried like below. 
```sh
oc get anomalydata -n osa-anomaly-detection
# You can see single anomaly data by executing similar to the below command 
oc describe anomalydata 2023-09-27-08-46-02-etcd-object-namespaces-namespaces -n osa-anomaly-detection
```

Sample command that runs inside the pod to trigger the program
```
python -m src.driver -aq kube_configmap_info
```

## Run Unit Test Cases

Written unit test cases using 'unittest' module. You can run all unit test cases by running the following command.

```bash
python -m unittest discover
```

If you want to run test cases for a single file or specific method, you can do something like below-mentioned examples.

```bash
python -m unittest tests/src/anomaly/test_factory.py
python -m unittest tests/src/anomaly/test_factory.py -k test_factory_get_class_default_param
```

You can check the code coverage by running the following command. This will create a `htmlcov` folder inside your project
where you can check the details of the code coverage.

```bash
pipenv run pytest --cov=src  -vv --cov-report html
```

## Understanding Anomaly Configurations

- Anomaly metric configuration file : `src/data_asset/anomaly_config.yaml`
- Note: This is just a sample file, needs to be configured based on need while publishing changes to any cluster. 

We can set the below-mentioned properties for each metric configuration to detect anomalies.

    Common Parameters
    query                   :: PROMQL Query to detect anomaly for a particular metric or query outcome. 
    name                    :: Display name of Anomaly, if not supplied we are taking key from yaml file as name.  
    description             :: Description of the Query/Amonomaly. 
    have_multi_result_data  :: Does the result set have multiple objects ? The possible value can be True/False. By default it will be True. 
                               Ex : count(kube_configmap_info) -> gives only one object inside resultset. 
                                    max(apiserver_storage_objects) by (resource) -> gives multiple objects inside resultset.
    method                  :: Type of the method to detect anomaly, we have below options to choose for this property. 
                               1) percentage_change: Based on the supplied period_range and step, it downloads the query data and takes Avg of the data except the latest one, once done we will compare the latest value to avg value to detect anomaly. 
                               2) min_max: If the latest value is outside of the given min/max parameters then we are marking it anomaly. 

    Parameters used for "percentage_change"
    percentage_change       :: Absolute change we need to consider for the latest value compared to earlier avg value to mark data as Anomaly 
    period_range            :: Range to get the query data. It's in a minute.
    min_no_of_data_points   :: We require a given minimum no of data points to calculate percentage change, if the query returns fewer data points then we won't proceed to detect anomaly. 
    step                    :: Get the metric data based on the given step. (one sample in each step minutes). It's in a minute.
    
    Parameters used for "min_max"
    min                     :: Min value that can be allowed, if the query returns value < min then we are marking it as Anomaly. 
    max                     :: Max value that can be allowed, if the query returns value > max then we are marking it as Anomaly. 
