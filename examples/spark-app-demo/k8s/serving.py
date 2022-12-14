#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import json

import model_store
from model_store import ModelStore

_MODEL_STORE = ModelStore(model_store.PRODUCTION)
_PETAL_WIDTH = 'petal_width'


def predict(input_json):
    try:
        input_dict = json.loads(input_json)
        model, version = _MODEL_STORE.load_latest_model()
        result = str(model.predict_proba([list(input_dict[_PETAL_WIDTH])])[0][1])
        return json.dumps({"result": result, "version": version})

    except IndexError:
        return 'Failure: the model is not ready yet'

    except Exception as e:
        print(e)
        return 'Failure'


def healthcheck(self):
    return 'Server is up!'


def version(self):
    try:
        model, version = _MODEL_STORE.load_latest_model()
        print(f'version={version}')
        return version
    except Exception as e:
        return e
