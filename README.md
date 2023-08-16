**Images**
----

* **URL**

  /images/

* **Method:**

  `GET` `POST`

* **Example:**
`{
    "id": 1,
    "created_at": "2021-08-31T00:52:13.215966Z",
    "uuid": "9947b368-a47b-4fb1-8334-7bee7725cac1",
    "known": true,
    "name": "messi.png",
    "x1": 50.0,
    "x2": 70.0,
    "y1": 80.0,
    "y2": 88.0,
    "calculated": false
  }`

**Image Details**
----

* **URL**

  /images/<uuid>

* **Method:**

  `GET` `PUT` `DELETE`

* **Example:**
`{
    "id": 1,
    "created_at": "2021-08-31T00:52:13.215966Z",
    "uuid": "9947b368-a47b-4fb1-8334-7bee7725cac1",
    "known": true,
    "name": "messi.png",
    "x1": 50.0,
    "x2": 70.0,
    "y1": 80.0,
    "y2": 88.0,
    "calculated": false
  }`

**Annotators**
----

* **URL**

  /annotators/

* **Method:**

  `GET` `POST`

* **Example:**
`{
    "id": 1,
    "created_at": "2021-08-31T00:52:13.266884Z",
    "uuid": "90147a3f-ae52-48de-95af-c5dd239b97be",
    "name": "yusuf",
    "score": 2.3
  }`

**Annotator Details**
----

* **URL**

  /annotators/<uuid>

* **Method:**

  `GET` `PUT` `DELETE`

* **Example:**
`{
    "id": 1,
    "created_at": "2021-08-31T00:52:13.266884Z",
    "uuid": "90147a3f-ae52-48de-95af-c5dd239b97be",
    "name": "yusuf",
    "score": 2.3}`

**Annotations**
----

* **URL**

  /annotations/

* **Method:**

  `GET` `POST`

* **Example:**
`{
    "id": 2,
    "created_at": "2021-08-31T00:52:13.335380Z",
    "uuid": "23c4167c-3a1b-4f3b-9de6-3ab6adf4193c",
    "x1": 46.0,
    "x2": 71.0,
    "y1": 78.0,
    "y2": 89.0,
    "x1_out": false,
    "x2_out": false,
    "y1_out": false,
    "y2_out": false,
    "spam": false,
    "processed": true,
    "point": 5.818181818181818,
    "annotator": 2,
    "image": 1
  }`

**Annotation Details**
----

* **URL**

  /annotations/<uuid>

* **Method:**

  `GET` `PUT` `DELETE`

* **Example:**
`{
    "id": 2,
    "created_at": "2021-08-31T00:52:13.335380Z",
    "uuid": "23c4167c-3a1b-4f3b-9de6-3ab6adf4193c",
    "x1": 46.0,
    "x2": 71.0,
    "y1": 78.0,
    "y2": 89.0,
    "x1_out": false,
    "x2_out": false,
    "y1_out": false,
    "y2_out": false,
    "spam": false,
    "processed": true,
    "point": 5.818181818181818,
    "annotator": 2,
    "image": 1
  }`

**Consensus**
----

* **URL**

  /consensus/

* **Method:**

  `GET` `POST`

* **Example:**
`{
    "id": 1,
    "created_at": "2021-08-31T00:52:36.764555Z",
    "uuid": "f0df3c70-67a2-45c2-ac91-2cd42a0038d2",
    "score": 437.3663509235745,
    "x1_lower": 41.0,
    "x1_upper": 49.0,
    "x2_lower": 63.125,
    "x2_upper": 76.125,
    "y1_lower": 74.625,
    "y1_upper": 83.625,
    "y2_lower": 78.625,
    "y2_upper": 95.625,
    "annotation_count": 4,
    "spam_count": 1,
    "image": 4,
    "annotators": [
      3,
      4
    ]
  }`

**Calculate Consensus**
----

* **URL**

  /consensus/calculate/

* **Method:**

  `GET` `POST`

* **Example:**
`"Consensus created"`

**Calculate Image Consensus**
----

* **URL**

  /images/calculate/<:uuid>

* **Method:**

  `GET` `POST`

* **Example:**
`"Consensus created"`


![alt text](https://github.com/ethemtunal/consensus_generator/blob/master/tables.png?raw=true)
