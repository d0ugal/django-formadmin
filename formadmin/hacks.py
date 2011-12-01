from django.db.models import Model
from django.db.models.options import Options
from django.db.models.query import EmptyQuerySet


class BaseFakeModel(object):

    key = 1
    value = "two"

    def __init__(self, *args, **kwargs):
        super(BaseFakeModel, self).__init__(*args, **kwargs)
        self._meta.model = self

    @property
    def __class__(self):
        return Model

    def serializable_value(self, attr):
        return 1


class BaseFakeQuerySet(EmptyQuerySet):

    def __init__(self, data):
        self._result_cache = []
        self._iter = False


def fake_model_meta(app_label):

    class Meta:
        pass

    kwargs = {'app_label': app_label, }

    opts = Options(Meta, **kwargs)
    opts.object_name = app_label
    return opts


def fake_model(data=None):

    return type('FakeModel', (BaseFakeModel,), {
        '_meta': fake_model_meta("formadmin"),
        '__name__': 'FakeModel',
    })


def fake_queryset(data):

    data = list(data)

    return type("FakeQuerySet", (BaseFakeQuerySet,), {
        '_meta': fake_model_meta("formadmin"),
    })(data)
