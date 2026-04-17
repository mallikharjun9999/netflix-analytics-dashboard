"""
Views for the Netflix Analysis application.
"""
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .services.data_loader import get_dataframe
from .services.analysis import get_summary_stats, get_all_chart_data
from .services.recommendation import get_recommendations


def dashboard(request):
    """Main analytics dashboard."""
    stats = get_summary_stats()
    chart_data = get_all_chart_data()
    return render(request, 'analysis_app/dashboard.html', {
        'stats': stats,
        'chart_data_json': json.dumps(chart_data),
    })


def search(request):
    """Search and filter page."""
    df = get_dataframe()

    query = request.GET.get('q', '').strip()
    filter_type = request.GET.get('type', '').strip()
    filter_country = request.GET.get('country', '').strip()
    filter_year = request.GET.get('year', '').strip()
    filter_rating = request.GET.get('rating', '').strip()
    filter_genre = request.GET.get('genre', '').strip()

    results = df.copy()

    if query:
        mask = results['title'].str.lower().str.contains(query.lower(), na=False)
        results = results[mask]

    if filter_type:
        results = results[results['type'] == filter_type]

    if filter_country:
        results = results[results['country'].str.lower().str.contains(filter_country.lower(), na=False)]

    if filter_year:
        try:
            results = results[results['release_year'] == int(filter_year)]
        except ValueError:
            pass

    if filter_rating:
        results = results[results['rating'] == filter_rating]

    if filter_genre:
        results = results[results['listed_in'].str.lower().str.contains(filter_genre.lower(), na=False)]

    # Build filter options
    all_genres = set()
    for g in df['listed_in']:
        all_genres.update([x.strip() for x in g.split(',') if x.strip()])

    result_list = results[['title', 'type', 'director', 'country', 'release_year',
                            'rating', 'listed_in', 'duration', 'description']].head(100).to_dict('records')

    return render(request, 'analysis_app/search.html', {
        'results': result_list,
        'total_results': len(results),
        'query': query,
        'filter_type': filter_type,
        'filter_country': filter_country,
        'filter_year': filter_year,
        'filter_rating': filter_rating,
        'filter_genre': filter_genre,
        'countries': sorted(df[df['country'] != '']['country'].unique().tolist()),
        'ratings': sorted(df[df['rating'] != '']['rating'].unique().tolist()),
        'genres': sorted(list(all_genres)),
        'years': sorted(df[df['release_year'] > 0]['release_year'].unique().tolist(), reverse=True),
    })


def detail(request, show_id):
    """Detail view for a single title."""
    df = get_dataframe()
    row = df[df['show_id'] == show_id]
    if row.empty:
        from django.http import Http404
        raise Http404("Title not found")
    item = row.iloc[0].to_dict()
    recommendations = get_recommendations(item['title'])
    return render(request, 'analysis_app/detail.html', {
        'item': item,
        'recommendations': recommendations,
    })


@require_GET
def api_recommendations(request):
    """AJAX endpoint for recommendations."""
    title = request.GET.get('title', '').strip()
    if not title:
        return JsonResponse({'error': 'title parameter required'}, status=400)
    recs = get_recommendations(title)
    return JsonResponse({'recommendations': recs})


@require_GET
def api_chart_data(request):
    """AJAX endpoint for chart data."""
    chart_data = get_all_chart_data()
    return JsonResponse(chart_data)


@require_GET  
def api_search(request):
    """AJAX endpoint for search."""
    df = get_dataframe()
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})
    
    mask = df['title'].str.lower().str.contains(query.lower(), na=False)
    results = df[mask][['show_id', 'title', 'type', 'release_year', 'rating', 'listed_in']].head(10)
    return JsonResponse({'results': results.to_dict('records')})
