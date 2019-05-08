import json
import logging

from django.shortcuts import render

from .views import breadcrumb_parser
from .stateio import _stateio_prepare_job_hierarchy

logger = logging.getLogger(__name__)


def search(request):
    """
    Global search of Records
    """

    # if search term present, use
    q = request.GET.get('q', None)
    if q:
        search_params = json.dumps({'q': q})
        logger.debug(search_params)
    else:
        search_params = None

    # generate hierarchy_dict
    job_hierarchy = _stateio_prepare_job_hierarchy()

    return render(request, 'core/search.html', {
        'search_string': q,
        'search_params': search_params,
        'job_hierarchy_json': json.dumps(job_hierarchy),
        'breadcrumbs': breadcrumb_parser(request),
        'page_title': ' | Search'
    })
