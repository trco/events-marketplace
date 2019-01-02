from haystack import indexes
from .models import Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    locality = indexes.CharField(model_attr='locality')
    country = indexes.CharField(model_attr='country')

    def get_model(self):
        return Event
