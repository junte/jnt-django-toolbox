from src.jnt_django_toolbox.admin.filters import AutocompleteFilter


class AuthorAutocompleteFilter(AutocompleteFilter):
    title = "Author"
    field_name = "author"


class TagsAutocompleteFilter(AutocompleteFilter):
    title = "Tags"
    field_name = "tags"
    is_multiple = True
