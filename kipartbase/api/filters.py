from django_filters.rest_framework import DjangoFilterBackend

#http://stackoverflow.com/questions/31029792/djangofilterbackend-with-multiple-ids
#http://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend

class CategoryFilterBackend(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filter_class = self.get_filter_class(view, queryset)
        print filter_class
#        if filter_class:
#            return filter_class(request.query_params, queryset=queryset, request=request).qs
        return queryset
