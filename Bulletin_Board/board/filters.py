from django_filters import FilterSet, ModelChoiceFilter

from .models import Reply, Ads


class AdsFilter(FilterSet):
    post = ModelChoiceFilter(
        empty_label='Все обьявления',
        field_name='post',
        label='Фильтр по обновлениям',
        queryset=Reply.objects.all()
    )

    class Meta:
        model = Reply
        fields = ('post',)

    def __init__(self, *args, **kwargs):
        super(AdsFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Ads.objects.filter(post_author_id=kwargs['request'])
