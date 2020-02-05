# NEAAR

#### NEtwork Analysis in ARangodb

---

## Installation

To install the package, clone the repository and type on your terminal:

```shell
python setup.py install
```

Or, if you want to install in developer mode

```shell
python setup.py develop
```

## Set up

To use the package, is required to have [ArangoDB](https://www.arangodb.com/) installed.

To access the databases you'll be asked for a password: is sufficient to create a file called `confif.json` on the repository with the structure:

```json
{
	"host" : "https://127.0.0.1:8529",
	"username" : "root",
	"password" : "1234"
}
```

port 8529 is the default for ArangoDB.

Now everything is set.

## Authors

* **Alessandro d'Agostino** [git](https://github.com/AlessandrodAgostino/)
* **Mattia Ceccarelli** [git](https://github.com/Mat092)
* **Riccardo Scheda** [git](https://github.com/riccardoscheda)
